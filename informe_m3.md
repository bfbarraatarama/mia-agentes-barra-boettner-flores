# Informe M3 — Evaluación de agentes autónomos en escape rooms

## Introducción

Este informe describe el trabajo realizado durante el Milestone 3 (M3) del proyecto integrador de Agentes Autónomos. El objetivo central de M3 es evaluar sistemáticamente el agente desarrollado en los milestones anteriores, comparar variantes de configuración y extraer conclusiones sobre sus capacidades y limitaciones.

Para ello se construyó una infraestructura de evaluación reproducible que permite ejecutar y persistir experimentos sobre múltiples escenarios de escape room, verificar el cumplimiento de los objetivos sobre el estado real del entorno y analizar el desempeño desde distintas dimensiones: éxito, errores, consumo, eficiencia, presión de contexto y calidad de planificación.

Las secciones siguientes describen la implementación del agente, la arquitectura de evaluación, el ground truth utilizado, las métricas calculadas, los experimentos corridos y los resultados obtenidos.

---

## 1. Implementación y configuraciones del agente

### 1.1 Base heredada de M1/M2

El agente base es `MyAgent`, implementado en `student_framework/agent.py`. El baseline inicial de M3 conserva el loop ReAct desarrollado en M1/M2, utilizando la misma lógica de interacción LLM–tools y la misma semántica de finalización. Sobre esta base se incorporan posteriormente mecanismos opcionales —como reparación de tool calls y gestión de contexto— y una variante PlannerAgent, lo que permite evaluar cada extensión respecto de una referencia común.

Los parámetros heredados relevantes son:

- **`max_iterations`**: tope de iteraciones del loop. Si el agente no llega a una respuesta final antes de agotarlo, el run termina con error.
- **`max_history_messages`**: introducido en M2, limita la cantidad de mensajes que se envían al LLM en cada llamada. Cuando el historial supera ese límite, los mensajes más antiguos se descartan (política de eliminación plana de M2) o se compactan (estrategia de M3, ver §1.3).
- **`register_tool(tool, schema)`**: registra una herramienta callable junto a su esquema. Las herramientas del mundo se inyectan de esta forma antes de cada run.
- **`_structured_call_with_repair()`**: mecanismo heredado para realizar llamadas estructuradas al LLM, validar la respuesta contra un schema y realizar intentos de reparación cuando la salida no es válida. En M3 se reutiliza esta infraestructura para nuevas funcionalidades, como la generación estructurada del plan y la compactación del historial mediante LLM.

### 1.2 Configuración del sistema e integración con el entorno M3

Para M3 se separó explícitamente la configuración del agente de la configuración del modelo de lenguaje. Las variantes de comportamiento del agente se definen mediante `agent_config`, mientras que la selección y los parámetros del LLM se especifican de forma independiente mediante `llm_config`. Esta separación permite combinar una misma implementación del agente con distintos modelos, o mantener fijo el LLM y modificar únicamente el comportamiento del agente, facilitando comparaciones experimentales controladas.

Las configuraciones de los modelos se definen en `eval/configs/llm_configs.py`. Durante M3 se utilizaron tres modelos:

| Nombre | Proveedor | Modelo | Contexto |
|---|---|---|---|
| `llama3.1` | Ollama (local) | `llama3.1` | 32 768 tokens |
| `qwen2.5:7b` | Ollama (local) | `qwen2.5:7b` | 32 768 tokens |
| `nova-lite` | AWS Bedrock | `amazon.nova-lite-v1:0` | — |

Los modelos locales se ejecutan vía Ollama; `nova-lite` se accede a través de Amazon Bedrock. En todos los casos la temperatura se fija en `0.2` mediante `_ConfiguredLLMClient`, que sobreescribe el parámetro en cada llamada para garantizar resultados reproducibles independientemente del default del proveedor.

**Integración de las herramientas del mundo**

El framework desarrollado en M1/M2 incluía herramientas generales como `calculator`, `distance_converter`, `file_reader`. Estas herramientas no forman parte del dominio de las escape rooms y podrían introducir capacidades ajenas al entorno evaluado. Por este motivo, las configuraciones utilizadas en M3 establecen `register_default_tools=False`, evitando su registro automático.

En su lugar, para cada trial se construye una nueva instancia de World y se generan sus herramientas mediante:

`make_world_tools(world)`

Estas herramientas se incorporan al agente reutilizando la interfaz existente:

`agent.register_tool(tool, schema)`

De esta forma, no fue necesario modificar el mecanismo de registro de herramientas desarrollado en los milestones anteriores: M3 reutiliza la misma interfaz para conectar el agente con un nuevo dominio.

Las herramientas expuestas por mia_world permiten al agente observar y modificar el entorno mediante acciones como `look`, `examine`, `take`, `use`y, en los escenarios que incluyen navegación, `go`. Cada herramienta queda vinculada a la instancia de World correspondiente al trial en curso, por lo que sus ejecuciones modifican directamente el estado del entorno.

El estado resultante del World constituye posteriormente la fuente de verdad utilizada por el evaluador para determinar si el agente alcanzó el objetivo del escenario, como se describe en la sección de ground truth.

### 1.3 Reparación de tool calls

Como una de las primeras variantes evaluadas en M3, se habilitó la reparación de tool calls malformados mediante el parámetro `tool_call_repair_max_attempts`. Con valor `0`, una llamada inválida no activa intentos de reparación; con un valor positivo, el agente puede realizar nuevos intentos incorporando información sobre el error producido.

Esta variante no modifica la estrategia de razonamiento del agente, sino su capacidad de recuperarse ante errores de formato o schema en la invocación de herramientas. Esto permite evaluar por separado cuánto del desempeño del baseline está limitado por errores de tool calling y cuánto responde a problemas de planificación, navegación u otras capacidades.

### 1.4 Agente planificador (`PlannerAgent`)

`PlannerAgent`, implementado en `student_framework/planner_agent.py`, extiende `MyAgent` con una fase de planificación explícita que ocurre antes de entrar al loop ReAct.

Al recibir el primer mensaje del usuario, `PlannerAgent` llama a `_structured_call_with_repair()` con `purpose="planning"` para que el LLM genere un `Plan` estructurado. El `Plan` (definido en `student_framework/plan.py`) contiene entre 1 y 12 instancias de `PlanStep`, cada una con una descripción de la acción a realizar. Si el LLM devuelve un plan inválido (por ejemplo, con cero pasos), se reintenta hasta `planning_repair_max_attempts` veces.

Una vez generado el plan, su contenido se serializa como texto numerado y se inyecta en el mensaje inicial antes de llamar al loop ReAct de `MyAgent`:

```
{user_message}

Plan de acción:
1. {step_1}
2. {step_2}
...

{plan_guidance}
```

El parámetro `plan_guidance` permite configurar cómo el agente debe interpretar el plan (por defecto, como una guía flexible adaptable a las observaciones del entorno).

La planificación es, por diseño, estática: el plan se genera al comienzo y no existe un mecanismo de replanning durante el loop ReAct. Aunque el agente puede apartarse de la guía inicial a partir de nueva evidencia, el planificador no vuelve a invocarse cuando las observaciones contradicen o vuelven obsoleta la estrategia original.

A nivel de implementación, el flag `_initial_plan_generated` garantiza que la planificación ocurre solo en el primer turno. En intentos subsiguientes del mismo trial, el agente reutiliza el plan ya inyectado en el historial y entra directamente al loop ReAct. Los tokens consumidos durante la planificación se acumulan en el `AgentResult` final vía un `response_callback`.

### 1.5 Gestión de contexto

En M2, `max_history_messages` limitaba el historial enviado al modelo mediante eliminación de mensajes pertenecientes a turnos anteriores. En escenarios M3 de horizonte largo apareció un caso no cubierto: un único turno podía acumular numerosas rondas ReAct hasta superar el presupuesto, sin existir todavía un turno cerrado que pudiera eliminarse de forma segura. Para tratar esta presión de contexto intra-turno se incorporó un mecanismo opcional de compactación.

Para experimentos de horizonte largo, `MyAgent` acepta un `history_compactor`: un callable que recibe los mensajes que serían descartados por `max_history_messages` y devuelve un resumen en texto que los reemplaza. Cuando no se configura compactor, se aplica la política M2 de eliminación plana.

La compactación ocurre intra-turno: cuando el historial supera el límite, se compactan las rondas más antiguas preservando las últimas `compaction_keep_recent_rounds` rondas completas en crudo. Las rondas se preservan completas (assistant + tool results) para no dejar mensajes de tool huérfanos.

Se implementaron dos estrategias en `student_framework/context/summarizer.py`:

**Compactación determinística (`deterministic_history_compactor`)**

Esta estrategia construye una representación compacta de las rondas seleccionadas sin realizar llamadas adicionales al LLM. Las acciones y sus observaciones se representan de forma reducida, siguiendo una estructura del tipo `acción → resultado`, y las observaciones extensas se truncan para controlar el tamaño final.

La deduplicación se determina utilizando las observaciones completas y no sus versiones truncadas. Esto evita que dos resultados diferentes sean tratados como una misma observación únicamente porque comparten el mismo prefijo. Si dos observaciones distintas producen la misma representación después del truncamiento, se conservan completas para preservar la diferencia entre ambas.

Además de las acciones solicitadas, se conserva el contenido textual relevante de los mensajes del  `assistant` cuando estos contienen simultáneamente texto y `tool_calls`, evitando perder información únicamente por la estructura de la respuesta del modelo.

La estrategia es deliberadamente lossy: no busca preservar toda la trayectoria, sino reducir su tamaño mediante reglas determinísticas, sin costo adicional de inferencia y sin introducir un segundo proceso de interpretación mediante LLM.

**Compactación por LLM (`make_llm_history_compactor()`)**
La segunda estrategia utiliza el propio LLM del agente para producir una representación semántica de la trayectoria compactada. A diferencia de la estrategia determinística, el objetivo no es reducir mecánicamente cada observación, sino identificar y estructurar la información que puede resultar relevante para continuar resolviendo el escenario.

El resumen sigue el esquema `TrajectorySummary`, que organiza la información en cuatro categorías: hechos descubiertos (`discovered_facts`), acciones ya intentadas (`attempted_actions`), subobjetivos pendientes (`open_subgoals`) y callejones sin salida (`dead_ends`). El prompt solicita además preservar de forma textual información especialmente sensible a pérdidas durante el resumen, como códigos, combinaciones, identificadores y mensajes de error.

La generación del resumen utiliza una llamada estructurada con`purpose="history_compaction"` y admite reparación cuando la salida no satisface el esquema esperado. Las llamadas y tokens utilizados por este proceso se contabilizan en el `AgentResult`, de forma que el costo adicional introducido por la estrategia pueda distinguirse del consumo correspondiente al loop principal del agente.

Cuando la presión de contexto vuelve a aparecer, el resumen generado previamente se incorpora al nuevo rango de compactación junto con la trayectoria posterior. De esta forma, los resúmenes se fusionan progresivamente en lugar de acumularse como mensajes independientes, evitando que los propios resúmenes terminen generando nuevamente presión sobre el historial.

El mecanismo contempla además fallos durante la compactación. Cuando es posible, se mantiene la política previa de eliminación sobre historial cerrado. Sin embargo, durante la compactación del turno activo no se eliminan arbitrariamente mensajes si esto implica fragmentar una ronda de herramientas. Si no puede obtenerse una representación que satisfaga el presupuesto manteniendo estas garantías, la ejecución termina de forma controlada.

---

## 2. Arquitectura de evaluación

La infraestructura de evaluación se diseñó para separar la **ejecución del agente**, la **persistencia de la evidencia experimental** y el **cálculo posterior de métricas y análisis**. Esta separación permite reutilizar los mismos resultados para distintos análisis sin necesidad de volver a ejecutar los modelos.

La unidad lógica de evaluación se organiza jerárquicamente de la siguiente manera:

```text
Evaluation
└── Run
    └── Case
        └── Trial
            └── Attempt
                └── Iteraciones ReAct / acciones
```

Un **case** representa una condición experimental determinada por la combinación de escenario, configuración del agente, configuración del LLM y configuración del trial. Cada case se repite mediante varios **trials independientes**. A su vez, cada trial puede contener uno o más **attempts** consecutivos sobre el mismo agente y el mismo estado del mundo.

Esta distinción es importante porque un attempt no constituye una nueva repetición experimental: los attempts de un mismo trial comparten el progreso acumulado. La unidad utilizada posteriormente para calcular la tasa de éxito es el **trial**.

### 2.1 Ejecución de casos, trials y attempts


`eval/experiment.py` contiene la lógica de ejecución de una condición experimental y provee las funciones `run_trial()` y `run_case()`, además de un punto de entrada por CLI (`main()`) para realizar ejecuciones individuales durante el desarrollo.

`run_trial()` ejecuta una repetición independiente de un caso. Al comienzo del trial se crea una nueva instancia del mundo a partir del escenario, se construye el agente con la configuración correspondiente y se registran las herramientas generadas mediante `make_world_tools(world)`.

Dentro del trial pueden ejecutarse uno o más attempts, según la `trial_config`. Después de cada attempt se llama a `check_goal()` sobre el estado real del mundo para determinar si el objetivo fue alcanzado. Si el objetivo se cumple, el trial finaliza exitosamente. Si el agente termina con un error que impide continuar, el trial también se cierra. En caso contrario, y mientras queden attempts disponibles, se envía al mismo agente el `continuation_message` configurado y se inicia un nuevo attempt.

Los attempts de un mismo trial **no reinician el entorno ni el agente**. Por lo tanto, conservan el estado del mundo, el inventario, las modificaciones realizadas sobre los objetos y el historial conversacional acumulado. Esto permite estudiar si el agente puede continuar una trayectoria incompleta sin perder el progreso alcanzado.

`run_case()` repite este procedimiento para ejecutar la cantidad de trials requerida para una misma condición experimental. A diferencia de los attempts, cada nuevo trial reconstruye el mundo y el agente desde cero, evitando contaminación de estado entre repeticiones.

La CLI de `eval/experiment.py` permite ejecutar un caso específico y obtener su resultado directamente, sin utilizar la capa de persistencia de corridas completas. Su objetivo principal es facilitar pruebas y desarrollo, mientras que las evaluaciones reproducibles utilizan el pipeline descripto en las secciones siguientes.

### 2.2 Configuraciones de trial

Las políticas que determinan cuántas oportunidades de continuación tiene el agente se definen en `eval/configs/trial_configs.py`.

| Configuración | `max_attempts` | Comportamiento |
|---|---:|---|
| `single_attempt` | 1 | Una única ejecución del agente |
| `single_continuation` | 2 | Un attempt inicial y una oportunidad de continuación |
| `multi_attempt` | 10 | Hasta diez attempts consecutivos sobre el mismo trial |

Cuando corresponde continuar, se utiliza el mensaje:

```text
El desafío todavía no está completado. Continuá.
```

La separación entre trial y attempt permite distinguir dos preguntas experimentales diferentes. Los **trials** capturan la variabilidad entre ejecuciones independientes de una misma condición, mientras que los **attempts** permiten estudiar la capacidad del agente para continuar desde un estado parcialmente resuelto.

Por esta razón, varios attempts dentro de un mismo trial no se contabilizan como muestras independientes al calcular las métricas de desempeño.

### 2.3 Evidencia generada durante la ejecución

Además de determinar si el escenario fue resuelto, la infraestructura captura información detallada de cada ejecución. Esta evidencia permite reconstruir posteriormente qué hizo el agente y constituye la base para las métricas y análisis desarrollados en M3.

Para cada trial y sus attempts se conserva información como:

- respuesta y resultado del agente;
- secuencia de pasos ejecutados;
- llamadas al LLM;
- tool calls realizados y resultados devueltos por las herramientas;
- errores y retries;
- consumo de tokens;
- propósito (`purpose`) asociado a las distintas llamadas al modelo;
- estado de finalización de cada attempt;
- resultado de `check_goal()`, incluyendo `goal_achieved` y `goal_reason`;
- eventos necesarios para reconstruir la trayectoria seguida en el mundo.

La identificación del `purpose` permite atribuir el consumo del LLM a distintos componentes del sistema. De esta manera es posible distinguir, por ejemplo, el costo correspondiente al loop principal del agente del introducido por planificación, reparación de llamadas estructuradas o compactación del historial.

La evidencia capturada en este nivel no constituye todavía una métrica. Su función es preservar la información necesaria para que los análisis posteriores puedan calcularse sin volver a ejecutar al agente.

### 2.4 Corridas, persistencia y reanudación

Las ejecuciones destinadas a evaluación se organizan en **runs** persistidos. `eval/run_execution.py` coordina este proceso mediante `start_run()` y `resume_run()`.

Una run representa una unidad física de evidencia experimental: contiene los resultados obtenidos al ejecutar un conjunto previamente definido de sistemas, escenarios y trials.

`start_run()` inicializa una nueva corrida, mientras que `resume_run()` permite continuar una corrida previamente interrumpida. Ambas utilizan la lógica de `_execute_pending_trials()`, que compara el plan de ejecución de la corrida con los resultados ya disponibles y ejecuta únicamente los trials que todavía están pendientes.

La capa de persistencia mantiene separados dos tipos principales de artefactos:

- **`{run_id}.manifest.json`**: registra las condiciones bajo las cuales se creó la corrida, incluyendo sistemas, escenarios, trial configs y configuraciones efectivas, junto con información de trazabilidad del repositorio.

- **`{run_id}.json`**: contiene la evidencia experimental acumulada durante la ejecución, organizada por case, trial y attempt.

El manifest se conserva como registro de las condiciones originales del experimento y no se modifica retroactivamente para incorporar información que no hubiera sido persistida al momento de la corrida.

El archivo de resultados se actualiza progresivamente después de completar cada trial. La persistencia utiliza escritura atómica: el nuevo contenido se escribe primero en un archivo temporal y luego reemplaza al archivo anterior. De esta manera se reduce el riesgo de dejar resultados parcialmente escritos ante una interrupción.

La combinación de persistencia incremental y `resume_run()` permite detener y continuar corridas largas sin volver a ejecutar los trials ya completados.

Los **runs persistidos se consideran evidencia experimental primaria**. Una vez generados, los análisis posteriores se realizan sobre estos artefactos sin modificar sus resultados originales.

### 2.5 Evaluación y combinación de múltiples runs

Una vez disponibles los runs, `eval/evaluation.py` permite construir una **evaluation** mediante `start_evaluation()`.

A diferencia de una run, una evaluation es un **artefacto derivado**: no ejecuta nuevamente al agente, sino que consume la evidencia persistida y calcula sobre ella las métricas y análisis seleccionados.

La evaluación puede utilizar uno o varios runs. Para ello, `_group_cases()` agrupa los trials correspondientes a una misma condición experimental lógica, identificada por la combinación:

```text
(agent_config, llm_config, trial_config, scenario)
```

Esto permite combinar evidencia obtenida en distintos momentos. Por ejemplo, si una misma condición experimental fue ejecutada en dos runs independientes con 10 trials cada una, la evaluación puede agrupar los 20 trials dentro del mismo case lógico.

```text
Run A ── 10 trials ──┐
                     ├──→ mismo case → 20 trials
Run B ── 10 trials ──┘
```

De esta manera es posible reutilizar un baseline previamente ejecutado al compararlo con una nueva configuración, sin necesidad de volver a consumir recursos ejecutando nuevamente el modelo.

Para mantener la trazabilidad, los resultados conservan información sobre el run de origen de cada trial. Las evaluaciones se almacenan separadamente de los runs junto con su propio manifest, manteniendo diferenciada la evidencia experimental primaria de los resultados derivados.

### 2.6 Métricas y análisis derivados

Una vez agrupados los trials, la evaluación aplica las métricas y análisis configurados sobre la evidencia persistida.

Entre los análisis implementados se encuentran:

- `success_rate`, para cuantificar la proporción de trials exitosos;
- `error_analysis`, para caracterizar los modos de fallo;
- `tool_call_repair_analysis`, para estudiar la activación y el comportamiento de la reparación de tool calls;
- `efficiency_analysis`, para analizar consumo de tokens, llamadas al LLM, steps, herramientas y costo relativo por éxito;
- `context_analysis`, para estudiar la presión de contexto y el comportamiento de las estrategias de compactación.
- `Evaluación cualitativa mediante LLM-as-judge`: evalúa la calidad de la planificación a partir de la trayectoria completa del trial utilizando la rúbrica `planning-quality-v1`. La evaluación considera dimensiones como la consistencia factual del razonamiento, la identificación de subobjetivos y dependencias, la coherencia entre estrategia y ejecución, y la capacidad de monitorear el progreso y adaptar la estrategia. Para desacoplar el juicio de la identidad del sistema evaluado, las trayectorias se presentan como casos ciegos y se acompañan de referencias canónicas a la evidencia necesaria para aplicar la rúbrica de manera consistente.

Estos análisis operan exclusivamente sobre la evidencia persistida: no modifican los runs ni requieren volver a ejecutar los modelos. Esto permite incorporar nuevas métricas o modificar la forma de analizar los resultados y regenerar una evaluation a partir de la misma evidencia experimental.

La definición, metodología e interpretación de cada una de estas métricas se desarrolla en la Sección 4.

### 2.7 Reporting y artefactos de salida

La capa de reporting transforma los resultados estructurados de la evaluación en artefactos destinados a facilitar su inspección e interpretación.

A partir de una evaluation se generan salidas estructuradas y reportes legibles, incluyendo, según el análisis realizado:

- resultados de métricas y análisis en formato estructurado;
- reportes Markdown;
- tablas comparativas;
- gráficos de `success_rate`;
- desgloses de eficiencia, consumo y presión de contexto.

Es importante distinguir estos reportes de la evidencia experimental original. Los archivos de una run contienen los resultados observados durante la ejecución del agente, mientras que los reportes son **representaciones derivadas** que pueden regenerarse cuando cambia una métrica, un análisis o una forma de visualización.

Por lo tanto, el flujo de información puede resumirse como:

```text
Ejecución
    ↓
Run
(evidencia primaria)
    ↓
Evaluation
(métricas y análisis)
    ↓
Reportes
(representación e interpretación)
```

### 2.8 Orquestación del pipeline

`eval/run.py` funciona como punto de entrada del pipeline completo de evaluación. Su función es coordinar las distintas capas: iniciar o retomar una corrida, ejecutar los trials pendientes, construir la evaluación correspondiente sobre los runs seleccionados y generar los artefactos derivados.

El flujo end-to-end queda representado de la siguiente manera:

```text
Configuraciones
 agent / LLM / trial / evaluación
              ↓
           run.py
              ↓
      run_execution.py
              ↓
        experiment.py
              ↓
      Agent + World + Tools
              ↓
       Trials / Attempts
              ↓
        Persistencia
              ↓
            RUN
     evidencia primaria
              ↓
       evaluation.py
              ↓
     Métricas y análisis
              ↓
        EVALUATION
      artefacto derivado
              ↓
          Reporting
              ↓
   Markdown / tablas / gráficos
```

Esta arquitectura desacopla la **generación de evidencia** de su **análisis posterior**. Como consecuencia, las ejecuciones costosas de los modelos pueden persistirse una única vez y reutilizarse posteriormente para comparar sistemas, incorporar nuevas métricas o regenerar reportes sin alterar la evidencia original.

---

## 3. Ground truth

La evaluación utiliza como ground truth el **estado real del mundo simulado**, definido por cada escenario, en lugar de basarse en la respuesta textual del agente. De esta forma, un trial se considera exitoso únicamente cuando las acciones ejecutadas producen efectivamente el estado objetivo.

La verificación se realiza mediante `check_goal()` (`mia_world/goals.py`), que evalúa condiciones sobre el estado del `World`, como la apertura de un objeto, la ubicación del agente o la presencia de un ítem en el inventario. También permite combinar condiciones (`all_of`, `any_of`) y verificar secuencias de acciones mediante el `event_log`.

Cada escenario, definido declarativamente en `scenarios/`, especifica su **estado inicial, objetivo y condición de éxito**. Al finalizar cada attempt, `run_trial()` ejecuta `check_goal()` y persiste tanto el resultado (`goal_achieved`) como la razón de la evaluación (`goal_reason`).

Esta infraestructura, provista como parte del framework base, se utilizó sin modificar su lógica para evaluar de manera uniforme todas las configuraciones y experimentos de M3.

