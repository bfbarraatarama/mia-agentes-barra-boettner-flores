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
- **`max_history_messages`**: introducido en M2, limita la cantidad de mensajes que se envían al LLM en cada llamada. Cuando el historial supera ese límite, los mensajes más antiguos se descartan (política de eliminación plana de M2) o se compactan (estrategia de M3, ver §1.5).
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

### 1.5 Gestión de contexto y estrategia de summarization

#### 1.5.1 El problema que M2 no cubría

En M2, `max_history_messages` limitaba el historial enviado al modelo eliminando mensajes pertenecientes a **turnos ya cerrados**: dado un presupuesto de mensajes, la política descartaba trazas intermedias completas de turnos anteriores y, si no alcanzaba, mensajes `user` y respuestas finales viejas. Esa política asume que el exceso de contexto proviene de la acumulación de turnos.

En los escenarios de horizonte largo de M3 apareció un caso que esa asunción no contempla: **un único turno puede agotar el presupuesto por sí solo**. Un trial de `vault-combination` o `backtracking-vault` ejecuta decenas de rondas ReAct dentro del mismo turno, y cada ronda agrega al historial un mensaje `assistant` más un mensaje `tool` por cada tool call. Cuando todo el historial pertenece al turno activo, no hay ningún turno cerrado que se pueda descartar de forma segura, y el run muere por presupuesto de contexto sin haber cometido ningún error de razonamiento.

La evidencia confirma que el problema es real y no hipotético, y que aparece incluso sin forzarlo. En la comparación histórica de tres modelos (`m3-three-model-repair-comparison-eval-003`) `context_overflow` explica **27 de 311 trials fallidos (9%)** con la ventana por defecto de 100 mensajes. En el run final, las variantes que corren a ventana 100 igualmente registran terminaciones por presupuesto tras 19 a 31 iteraciones ReAct. Y en todos los casos la terminación ocurre en el `attempt_index` 1: es presión **intra-turno**, no acumulación de turnos. (El 48% de `context_overflow` del run final no sirve como motivación, porque proviene sobre todo de las variantes cuya ventana se redujo deliberadamente para activar el mecanismo; ver §1.5.5.)

Para tratar esta presión **intra-turno** se incorporó un mecanismo opcional de compactación: `MyAgent` acepta un `history_compactor`, un callable que recibe los mensajes que serían descartados y devuelve un texto que los reemplaza. Cuando no se configura compactor, el agente mantiene exactamente la política de eliminación plana de M2, de modo que el baseline de M3 sigue siendo comparable con M2.

#### 1.5.2 Decisiones de diseño transversales a ambas estrategias

Las siguientes decisiones son independientes de cómo se genere el resumen y se implementan en `student_framework/agent.py`.

**La unidad de compactación es la ronda de herramientas completa, no el mensaje.** `_closed_tool_rounds()` identifica rangos `[assistant con tool_calls, sus mensajes tool)` y la compactación reemplaza siempre rondas enteras. La alternativa —cortar por cantidad de mensajes— era más simple pero producía historiales inválidos: un mensaje `tool` sin su `assistant` correspondiente queda huérfano y las APIs de tool calling lo rechazan, y una respuesta con varios tool calls partida a la mitad deja llamadas sin resultado. Preferimos perder un poco de granularidad antes que emitir historiales que el proveedor pueda rechazar.

**Se conservan en crudo las últimas `compaction_keep_recent_rounds` rondas.** El resumen es, por definición, una pérdida de información; las observaciones más recientes son las que el agente necesita con más detalle para decidir la próxima acción. Fijamos el valor en 2 para todas las configuraciones evaluadas: suficiente para que el modelo vea el resultado de su última acción y el de la anterior, sin volver el mecanismo inútil por conservar demasiado.

**Si conservar esas rondas no alcanza, una segunda pasada compacta todas.** `_compact_active_turn()` itera sobre `(compaction_keep_recent_rounds, 0)`. La alternativa era fallar directamente cuando el presupuesto no se satisface conservando las rondas recientes, pero eso convertía el parámetro en una causa de muerte del run. Degradar la calidad del contexto es preferible a terminar la ejecución.

**El resumen se inyecta como mensaje con rol `user`, no `assistant`.** Un `assistant` sin `tool_calls` es, para la política de trimming heredada, la "respuesta final" de un turno, y es justamente lo que la segunda pasada elimina primero: el resumen sería el primer candidato a ser borrado. Con rol `user` el resumen sobrevive al mismo mecanismo que lo creó. Los resúmenes se prefijan (`[Resumen de contexto previo]` y `[Resumen de progreso del intento actual]`) para que el modelo distinga contexto reconstruido de observación directa del mundo, y `_merge_adjacent_user_messages()` fusiona mensajes `user` contiguos antes de la llamada, evitando que la inyección produzca secuencias de `user` consecutivos que algunos proveedores rechazan.

**Los resúmenes se fusionan en lugar de acumularse.** Cuando vuelve a aparecer presión de contexto, el rango a compactar arranca en el primer mensaje posterior al `user` del turno, de modo que el resumen anterior queda **incluido** en el nuevo rango y es reemplazado por uno solo. La alternativa —resumir sólo lo nuevo y dejar el resumen viejo intacto— hacía que los propios resúmenes se acumularan como mensajes independientes y volvieran a generar la presión que venían a resolver.

**El fallo del compactor no aborta el run por excepción.** `_compact_messages()` captura cualquier error, lo registra en la traza como evento `history_compaction` con su error y devuelve `None`; quien llama decide el fallback. En la eviction de historial cerrado el fallback es la eliminación plana de M2, que siempre está disponible. En la compactación intra-turno **no hay fallback seguro**: eliminar mensajes arbitrariamente fragmentaría rondas, así que el turno termina de forma controlada y el trial queda clasificado como `context_overflow`. La decisión fue preferir una terminación explícita y clasificable a un historial silenciosamente corrupto. Esto importa para leer los resultados: en el run final se registraron **518 eventos de compactación y 88 fallas**, y esas fallas son parte de por qué las variantes con resumen terminan por presupuesto.

**El compactor recibe una copia de los mensajes.** `_compact_messages()` pasa un `deepcopy` del rango. Un compactor que mutara los mensajes que recibe —o, en la variante por LLM, un error en medio de la construcción del transcript— no puede dejar el historial del agente en un estado intermedio.

**Guarda de terminación.** La compactación sólo se aplica cuando el rango tiene al menos 2 mensajes (`end - start >= 2`). Reemplazar un único mensaje por un resumen no reduce la longitud del historial, y el bucle de trimming no terminaría nunca.

**La estrategia se declara con un string, no con un callable.** `build_agent` acepta `history_compaction: "deterministic" | "llm"` (además de un callable, que usan los tests). El motivo es de infraestructura de evaluación: las `agent_config` de `eval/` se persisten tal cual en el manifest del run, y un callable no es serializable. Con un string, el manifest documenta con precisión qué estrategia produjo cada resultado.

**El compactor por LLM se inyecta después de construir el agente.** `make_llm_history_compactor(agent)` necesita el agente para reusar su cliente LLM, y el agente necesita el compactor: la dependencia es circular. `set_history_compactor()` resuelve el ciclo en dos pasos en lugar de mover la construcción del cliente afuera del agente.

#### 1.5.3 Estrategia A — compactación determinística

`deterministic_history_compactor` (`student_framework/context/summarizer.py`) construye una representación compacta de las rondas seleccionadas **sin realizar llamadas adicionales al LLM**. Cada acción se plega en una línea `acción → resultado`, y las observaciones extensas se truncan a 200 caracteres.

Existe deliberadamente como **control experimental**: aísla cuánto del efecto de la gestión de contexto se explica por *comprimir* la trayectoria y cuánto requiere *resumirla con abstracción*. Su costo de inferencia es cero y no introduce modos de falla nuevos (no puede alucinar, no puede fallar el schema, no puede agotar el rate limit). Si esta estrategia bastara, la compactación por LLM no se justificaría.

Dos decisiones específicas:

**La deduplicación usa las observaciones completas, no las truncadas.** Las líneas se generan dos veces —una completa y una truncada— y se deduplica por la versión completa. Si se deduplicara por la truncada, dos observaciones distintas que comparten los primeros 200 caracteres (algo habitual en `extreme-archive`, donde veinte expedientes arrancan con la misma prosa burocrática) se fusionarían en una sola y el agente perdería justamente la diferencia que estaba buscando.

**Cuando dos observaciones distintas colisionan al truncarse, ambas se conservan completas.** La representación truncada sólo se usa si es inequívoca; si varias líneas completas distintas caen en la misma línea truncada, se emiten completas. El resumen crece, pero no miente. Las repeticiones exactas se colapsan con un sufijo `(xN)`, que además le informa al modelo que estuvo repitiendo la misma acción.

La estrategia es explícitamente *lossy*: no busca preservar la trayectoria, sino reducir su tamaño con reglas determinísticas y sin introducir un segundo proceso de interpretación.

#### 1.5.4 Estrategia B — summarization por LLM

`make_llm_history_compactor()` usa el propio LLM del agente para producir una representación semántica de la trayectoria compactada. El objetivo no es comprimir mecánicamente cada observación, sino **identificar qué información sigue siendo relevante para continuar resolviendo el escenario**.

**El resumen es estructurado, no prosa libre.** Se pide un `TrajectorySummary` con cuatro campos:

| Campo | Contenido |
|---|---|
| `discovered_facts` | Hechos del mundo: objetos, ubicaciones, relaciones, códigos y combinaciones |
| `attempted_actions` | Acciones ya intentadas y su resultado, incluidas las fallidas |
| `open_subgoals` | Subobjetivos pendientes o plan parcial |
| `dead_ends` | Caminos que ya se sabe que no funcionan, y por qué |

La elección de estos cuatro campos responde a los modos de falla que observamos en el baseline. `discovered_facts` y `open_subgoals` sostienen la continuidad del plan. `attempted_actions` y `dead_ends` atacan un problema medido: el **32% de las acciones ejecutadas son repeticiones intra-trial** de una acción con la misma herramienta, los mismos argumentos y el mismo resultado. Un resumen que sólo preservara el estado del mundo, sin registrar qué ya se intentó y qué ya se descartó, invitaría al agente a re-explorar lo mismo con el contexto recién liberado. Un esquema cerrado además obliga al modelo a poblar las cuatro categorías en lugar de escribir un párrafo narrativo del que después hay que inferir el estado.

**Se piden literales textuales.** El prompt exige copiar textualmente códigos, claves, combinaciones y mensajes de error, y prohíbe inventar información ausente del fragmento. El modo de falla propio de un resumidor no es escribir de más: es **omitir o parafrasear el dato que después resulta clave**. En estos escenarios una llave de color, una combinación de tres núcleos o el texto exacto de un error de cerradura son irrecuperables si el resumen los abstrae a "encontré una pista".

**El transcript que ve el resumidor se trunca más largo que en la estrategia determinística**: 1.000 caracteres por observación, contra 200. La asimetría es intencional. En la estrategia determinística el truncado *es* el resultado final y va directo al historial, así que hay que ser agresivo; acá es sólo la entrada del resumidor, y darle más material mejora lo que puede extraer sin costo en el historial resultante, porque la salida está acotada por el esquema.

**Reusa `_structured_call_with_repair()` con `purpose="history_compaction"`.** Esto trae tres cosas sin código nuevo: validación de la salida contra el esquema con reparación cuando no valida (`history_compaction_repair_max_attempts`), y —crítico— esa maquinaria **arma su propio contexto y no toca `agent._history`**, por lo que es seguro invocarla desde adentro del propio trimming del historial. Un resumidor que construyera su llamada sobre el historial del agente sería reentrante sobre la estructura que está modificando.

**Los tokens del resumidor se contabilizan en el `AgentResult`.** El compactor corre dentro del trimming, donde no puede recibir por parámetro la clausura de acumulación de tokens del run; se expone como `agent._run_response_callback` para que su consumo no quede fuera de la medición. Sin esto, la estrategia más costosa aparecería como la más barata. Con `purpose` se separa el consumo del loop principal del introducido por el resumen: en el run final, `summary` gasta **48.691 tokens/trial en `agent` y 7.618 en `history_compaction`** (3,4 llamadas de compactación por trial), es decir, el resumen agrega ~16% sobre el consumo del loop.

#### 1.5.5 Consecuencias observadas

Ambas estrategias se evaluaron contra un control barato —subir el presupuesto de mensajes sin compactar nada— para separar "el mecanismo aporta" de "el problema era simplemente falta de ventana". La evidencia disponible viene de dos contrastes, y ninguno de los dos permite atribuir el efecto de forma limpia. Conviene explicitar por qué.

**Contraste a ventana 100** (`eval/results/historic/evaluations/m3-context-comparison-eval-008`, nova-lite, `multi_attempt`, 80 trials por sistema):

| Sistema | Ventana | Compactación | Éxito | Compactaciones (eventos / fallas) |
|---|---:|---|---:|---:|
| `minimal` | 100 | — | 69% | 0 / 0 |
| `minimal_history_200` | 200 | — | **75%** | 0 / 0 |
| `minimal_compaction` | 100 | determinística | 68% | 8 / 0 |
| `minimal_summary` | 100 | por LLM | 62% | 13 / 4 |

El problema de este contraste es visible en la última columna: **con ventana 100 el mecanismo casi no se dispara** (8 y 13 activaciones en 80 trials). Las diferencias de éxito no son atribuibles a una compactación que apenas ocurrió. Lo único que este contraste sí muestra con claridad es que el control barato gana: **subir el presupuesto a 200 mensajes (75%) supera a las tres variantes**, incluido el baseline.

**Contraste a ventana 20** (`m3-final-eval-001`, nova-lite, `multi_attempt`, 80 trials por sistema). La reducción de la ventana fue una decisión deliberada, precisamente para forzar que el mecanismo se active de manera observable:

| Sistema | Ventana | Compactación | Éxito | Compactaciones | `context_overflow` |
|---|---:|---|---:|---:|---:|
| `baseline` | 100 | — | **74%** | 0 | 0 |
| `planner` | 100 | — | 72% | 0 | 2 |
| `summary` | 20 | por LLM | 34% | 253 / 41 fallas | 33 |
| `planner_summary` | 20 | por LLM | 36% | 265 / 47 fallas | 35 |

Acá el mecanismo sí opera (518 eventos de compactación en total, con 88 fallas), pero la comparación mezcla dos cambios: el resumen y un presupuesto cinco veces menor. Lo que se puede afirmar es que **el resumen no compensa la reducción de ventana**: `context_overflow` sigue siendo el modo de falla dominante en las variantes con resumen (33 y 35 trials, contra 0 y 2 en las de ventana 100), y una de cada seis compactaciones falla, lo que por diseño termina el turno de forma controlada.

**El brazo que falta.** Para atribuir el efecto al mecanismo haría falta un control a **ventana 20 sin compactación**. Ese brazo no existe en ninguno de los dos runs, y no es una omisión menor: sin él, la caída de 74% a 34% no se puede repartir entre "la ventana chica lastima" y "el resumen pierde información necesaria". La hipótesis que la evidencia sugiere —pero no prueba— es que domina lo primero, ya que a ventana 20 el baseline tampoco tendría de dónde recortar.

**Balance.** Sobre este dataset no encontramos una configuración en la que la summarization por LLM se pague: donde el mecanismo no hace falta no cambia nada, y donde hace falta no alcanza. El costo adicional está acotado y es medible (~16% de tokens sobre el loop principal, ~3,4 llamadas por trial), así que el problema no es el precio sino el beneficio. Para este dominio, el resultado práctico es que **conviene gastar el presupuesto en ventana antes que en resumir**; la summarization recién se justificaría en un régimen donde ampliar la ventana no sea una opción.

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

---

## 4. Métricas y análisis

Los análisis de M3 operan exclusivamente sobre la evidencia persistida por los runs y se invocan desde `eval/evaluation.py`. El conjunto de análisis aplicados a cada evaluation se configura en `eval/configs/evaluation_configs.py`.

### 4.1 Tasa de éxito (`success_rate`)

La métrica principal de evaluación cuantitativa es `success_rate`, definida en `eval/metrics.py`.

\[
\text{success rate} =
\frac{\text{trials exitosos}}
{\text{trials totales}}
\]

La unidad de medición es el **trial**: un trial es exitoso si `goal_achieved` es `True` en al menos uno de sus attempts. Los attempts adicionales dentro de un mismo trial no se contabilizan como unidades independientes, ya que comparten el estado del mundo y el agente.

La tasa de éxito se calcula por case (combinación de `agent_config`, `llm_config`, `trial_config`, escenario). Los resultados comparativos entre sistemas se obtienen agregando los trials de todos los cases de un mismo sistema, o agrupando por escenario para identificar casos de dificultad diferenciada.

### 4.2 Análisis de errores

`analyze_errors()` en `eval/analyses/error_analysis.py` clasifica los trials fallidos a partir de la evidencia del último attempt de cada trial.

La taxonomía cubre ocho modos de fallo:

| Modo | Descripción |
|---|---|
| `context_overflow` | El historial superó `max_history_messages` y la ejecución terminó por presupuesto de contexto |
| `max_iterations` | El agente agotó el presupuesto de pasos sin alcanzar el objetivo |
| `hallucination` | El agente narró tool calls como texto en lugar de ejecutarlas, o declaró éxito cuando el objetivo no se cumplió |
| `wrong_tool_use` | Algún paso devolvió un error de herramienta |
| `gave_up_early` | El agente terminó voluntariamente en cuatro pasos o menos sin error |
| `planning_order` | En escenarios con goal de secuencia, las condiciones se cumplieron en orden incorrecto |
| `navigation_error` | En escenarios multi-sala, el agente no utilizó la herramienta `go` |
| `planning_failure` | El agente exploró múltiples pasos sin alcanzar el objetivo (modo residual) |

La clasificación se determina a partir del contenido del `agent_result` del último attempt: error del agente, respuesta final, pasos ejecutados y `goal_reason`. La asignación es secuencial: el primer criterio que se satisface determina el modo. `planning_failure` funciona como categoría residual para los trials que no encajan en ningún modo anterior.

El análisis permite obtener la distribución de fallos por modelo, sistema y escenario, facilitando la identificación de patrones que no resultan visibles únicamente a partir de `success_rate`.

### 4.3 Análisis de reparación de tool calls

`analyze_tool_call_repair()` en `eval/analyses/tool_call_repair_analysis.py` cuantifica la activación del mecanismo de reparación implementado con `tool_call_repair_max_attempts`.

El análisis opera sobre los eventos de traza de tipo `llm_call` con `purpose="tool_call_repair"`. Para cada sistema reporta:

- cantidad de trials en los que se activó al menos una reparación;
- total de llamadas físicas al LLM destinadas a reparación;
- respuestas recibidas y errores producidos durante esas llamadas;
- tokens de entrada y salida consumidos por las llamadas de reparación;
- cobertura de uso de tokens: si todas las llamadas de reparación devolvieron información de tokens completa.

La identificación de estas llamadas mediante su `purpose` permite separar el consumo introducido por la reparación del correspondiente al loop principal del agente, utilizando únicamente la evidencia persistida durante la ejecución.

### 4.4 Análisis de eficiencia y consumo

`analyze_efficiency()` en `eval/analyses/efficiency_analysis.py` produce un resumen cuantitativo del consumo de recursos por sistema, agrupando por la tripla `(agent_config, llm_config, trial_config)`.

Las métricas agregadas incluyen:

- **por trial**: attempts, retries, llamadas al LLM, ejecuciones de herramientas, steps, tokens de entrada, tokens de salida, tokens totales;
- **por éxito**: mismas métricas condicionadas a los trials en que se alcanzó el objetivo, para cuantificar el costo efectivo de resolver el escenario.

Las métricas de llamadas al LLM y de tokens se desglosan además por **`purpose`**. Esto permite distinguir el consumo del loop principal del agente (`"agent"`) del introducido por planificación (`"planning"`), reparación de tool calls (`"tool_call_repair"`) y compactación del historial (`"history_compaction"`).

Las ejecuciones de herramientas se desglosan por nombre de herramienta, ordenadas por frecuencia. La comparación entre sistemas con y sin una funcionalidad adicional —como reparación o planificación— puede realizarse sobre estas métricas sin ejecutar nuevamente los modelos.

### 4.5 Análisis de presión de contexto

`analyze_context()` en `eval/analyses/context_analysis.py` caracteriza la relación entre el tamaño del historial y el desempeño del agente, comparando estrategias de gestión de contexto.

El análisis mide las siguientes dimensiones:

**Terminaciones por presupuesto**: trials y attempts que terminaron porque el historial superó `max_history_messages` y no pudo obtenerse una representación que satisficiera el presupuesto. Se reporta en qué attempt_index ocurrió la terminación y cuántas iteraciones ReAct había ejecutado el agente al momento de la terminación.

**Presión estructural**: distribución de la cantidad de tool calls por iteración. Dado que cada iteración agrega al historial al menos un mensaje del assistant y un resultado por cada tool call, las iteraciones con múltiples tool calls ejercen una presión desproporcionada sobre el presupuesto disponible.

**Acciones repetidas intra-trial**: proporción de acciones cuya combinación de herramienta, argumentos y resultado ya había aparecido anteriormente en el mismo trial. La clave de comparación es estructural para argumentos JSON y literal para el resto, con la misma semántica que utiliza el LLM judge en `eval/llm_judge/cases.py`. Un ratio elevado indica que el agente está re-ejecutando acciones sin obtener nueva información.

**Re-derivación entre attempts**: de las acciones ejecutadas a partir del segundo attempt, qué proporción ya había sido ejecutada con el mismo resultado en attempts anteriores del mismo trial. Este indicador refleja si el agente reutiliza el progreso acumulado o vuelve a derivar información ya disponible en el historial.

**Ocupación de la ventana**: máximo de mensajes enviados al LLM en una única llamada y cantidad de llamadas realizadas estando la ventana en su límite máximo.

**Costo del compactor**: cuando está activa una estrategia de compactación, el análisis reporta la cantidad de eventos de compactación, la cantidad de fallos de compactación y los tokens de entrada y salida consumidos por el proceso, distinguibles en la traza por `purpose="history_compaction"`.

Los resultados se agregan por sistema (`agent_config` × `llm_config`) y por case completo, lo que permite comparar directamente el comportamiento de distintas estrategias de contexto ante los mismos escenarios.

### 4.6 Evaluación cualitativa mediante LLM-as-judge

Además de las métricas cuantitativas, M3 incluye una evaluación cualitativa de la calidad de planificación del agente sobre trayectorias seleccionadas. La infraestructura correspondiente se encuentra en `eval/llm_judge/`.

**Rúbrica**

La evaluación utiliza la rúbrica `planning-quality-v1` (definida en `eval/llm_judge/rubric.py`), que cubre una única dimensión:

**Q1 — Calidad de la planificación durante la trayectoria**: evalúa la capacidad del agente para construir y mantener una estrategia orientada al objetivo, fundamentarla en la información obtenida, traducirla en acciones coherentes y revisarla cuando nueva evidencia lo requiere.

La dimensión se evalúa mediante cuatro criterios:

| Criterio | Nombre | Aplicabilidad |
|---|---|---|
| Q1.1 | Consistencia factual con la evidencia | Siempre |
| Q1.2 | Estructuración de subobjetivos y dependencias | Siempre |
| Q1.3 | Consistencia de la ejecución con la estrategia | Siempre |
| Q1.4 | Monitoreo y replanificación | Condicional |

Q1.4 es el único criterio condicional: sólo aplica cuando la trayectoria contiene una oportunidad observable de monitorear el resultado de una conducta y, cuando corresponde, revisar el curso de acción. Tres triggers determinísticos activan la evaluabilidad de este criterio: la presencia de más de un attempt en el trial, la existencia de una observación marcada como error —ya sea porque el paso persistido contiene un error o porque el contenido de la observación comienza con `"Error:"`— seguida de una iteración posterior, o la repetición de una acción con idéntica herramienta, argumentos y resultado. Si ninguno de estos triggers está presente, el criterio se registra como N/A porque la trayectoria no permite observar capacidad de replanificación.

Cada criterio se evalúa con un veredicto binario PASS/FAIL. La rúbrica establece reglas de evidencia sobre qué constituye evidencia primaria (las acciones ejecutadas y las observaciones del mundo prevalecen sobre las verbalizaciones del agente), y una regla de materialidad que impide que un error aislado y corregido produzca automáticamente un FAIL.

**Protocolo de evaluación**

Para desacoplar el juicio de la identidad del sistema evaluado, las trayectorias se presentan como **casos ciegos**: la información que permitiría identificar la configuración del agente o el modelo utilizado no se incluye en la presentación.

Los casos se preparan mediante `eval/llm_judge/prepare_dataset.py` y se gestionan a través de las funciones de persistencia en `eval/llm_judge/persistence.py`. La interfaz de revisión, disponible en `eval/llm_judge/reviewer.py`, acompaña la presentación de cada caso con referencias canónicas a la evidencia de la trayectoria necesaria para aplicar la rúbrica de manera consistente.

Las anotaciones se registran por criterio y se distingue entre casos completados (todos los criterios aplicables anotados), en progreso y pendientes.

