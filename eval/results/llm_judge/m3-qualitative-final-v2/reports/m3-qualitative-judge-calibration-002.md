LLM-as-judge — estado de evaluación
- Dataset: m3-qualitative-final-v2
- Judge evaluation: m3-qualitative-judge-calibration-002
- Split: dev
- Configuración nominal del judge: claude-opus-4.5
- Configuración efectiva: {"max_tokens": 4096, "model": "us.anthropic.claude-opus-4-5-20251101-v1:0", "provider": "bedrock", "region": "us-west-2", "temperature": 0.0}
- Máximo de reparaciones por criterio: 2
- Casos completos: 4/4
- Casos pendientes: ninguno
- Criterios checkpointed: 0 en 0 casos
- Llamadas LLM: 15 (respuesta=15, error=0, repair=0)
- Tokens de entrada: 139579
- Tokens de salida: 6132

Acuerdo humano ↔ LLM judge
- Dataset: m3-qualitative-final-v2
- Judge evaluation: m3-qualitative-judge-calibration-002
- Anotador humano: bruno
- Split: dev

Global (humano en filas, judge en columnas):
n=15; agreement=0.933; kappa=0.865
  humano=PASS / judge=PASS: 8
  humano=PASS / judge=FAIL: 1
  humano=FAIL / judge=PASS: 0
  humano=FAIL / judge=FAIL: 6

Por criterio:
- Q1.1: n=4; agreement=1.000; kappa=1.000
- Q1.2: n=4; agreement=0.750; kappa=0.000
- Q1.3: n=4; agreement=1.000; kappa=1.000
- Q1.4: n=3; agreement=1.000; kappa=1.000

## Detalle por caso y criterio

### qc-009

#### Q1.1

- Acuerdo: SÍ
- Humano: `FAIL`
- LLM judge: `FAIL`

**Humano — justificación**

El agente contradice evidencia explícita sobre su inventario. Recibe errores que indican que no lleva esos libros y luego razona como si ya hubiera usado “todos los libros de su inventario”, y los sostiene.

**Humano — evidencia**

- `a1.i13`
- `a1.i13.action1`
- `a1.i14`
- `a1.i14.action1`
- `a1.i15`
- `a1.i15.action1`
- `a1.i16`
- `a1.i16.action1`
- `a1.i17`
- `a1.i17.action1`
- `a1.i18`
- `a1.i18.action1`
- `a1.i19`
- `a1.i19.action1`
- `a1.i20`
- `a1.i21`
- `a1.i22`
- `a1.termination`
- `a2.i1`
- `a2.termination`
- `a3.i1`
- `a3.termination`
- `a4.i1`
- `a4.termination`
- `a5.i1`
- `a5.termination`
- `a6.i1`
- `a6.termination`
- `a7.i1`
- `a7.termination`
- `a8.i1`
- `a8.termination`
- `a9.i1`
- `a9.termination`
- `a10.i1`
- `a10.termination`

**LLM judge — justificación**

El agente basa materialmente una secuencia de decisiones (a1.i13 a a1.i19) en la creencia de que tiene libros en su inventario, cuando la evidencia disponible ya contradecía esto. En ningún momento de la trayectoria el agente ejecutó una acción "take" para recoger los libros; simplemente los examinó en la estantería. Sin embargo, a partir de a1.i13, el agente intenta usar cada libro con la puerta ("use libro_X puerta_principal"), recibiendo repetidamente el error "no llevas ningún 'libro_X'". A pesar de que cada error confirmaba que no tenía el objeto en su inventario, el agente continuó intentando usar otros libros bajo la misma premisa falsa ("I should try to use the other books I have in my inventory"). Esta creencia contradecía la evidencia observable: nunca había tomado ningún libro, y cada intento fallido confirmaba que no los poseía. El agente persistió en esta representación incorrecta durante siete iteraciones consecutivas sin corregir su modelo del mundo.

**LLM judge — evidencia**

- `a1.i13.action1`
- `a1.i14.action1`
- `a1.i15.action1`
- `a1.i16.action1`
- `a1.i17.action1`
- `a1.i18.action1`
- `a1.i19.action1`

#### Q1.2

- Acuerdo: NO
- Humano: `PASS`
- LLM judge: `FAIL`

**Humano — justificación**

El agente identifica que tiene que explorar la biblioteca, incluyendo los libros, pues allí puede estar una pista para salir.
Falla en la ejecución de dicha estrategia, al no revisar el libro con la pista.

**Humano — evidencia**

- `a1.i1`
- `a1.i2`
- `a1.i3`
- `a1.i4`
- `a1.i5`
- `a1.i6`
- `a1.i7`
- `a1.i8`
- `a1.i9`
- `a1.i10`
- `a1.i11`
- `a1.i12`
- `a1.i13`

**LLM judge — justificación**

El agente omite materialmente un subobjetivo crítico: nunca examina el octavo libro (libro_sermones) que permanece sin revisar durante toda la trayectoria. En a1.i9, el agente declara "I should examine the last book on the shelf" pero examina libro_genealogia, dejando libro_sermones sin explorar. Esta omisión es estructural, no meramente de ejecución: el agente tenía identificados 8 volúmenes (a1.i2) pero su plan de exploración sistemática solo cubrió 7. Además, el agente nunca identifica el prerrequisito fundamental de que necesita obtener llaves para abrir la caja fuerte y la puerta. Aunque reconoce que ambas están cerradas con llave (a1.i10, a1.i11), no estructura un subobjetivo de "encontrar llaves" ni considera que la caja fuerte podría contener la llave de la puerta (cadena de dependencias). En lugar de eso, intenta usar libros directamente sobre la puerta sin haberlos recogido primero (a1.i13-i19), mostrando que no identificó el prerrequisito de "tomar objetos antes de usarlos". La estructura de subobjetivos está materialmente incompleta.

**LLM judge — evidencia**

- `a1.i2.action1`
- `a1.i9`
- `a1.i10.action1`
- `a1.i11.action1`
- `a1.i20.action1`
- `a1.i21.action1`

#### Q1.3

- Acuerdo: SÍ
- Humano: `FAIL`
- LLM judge: `FAIL`

**Humano — justificación**

El agente se propuso examinar todos los libros, pero no revisó el último que le quedaba por revisar.

**Humano — evidencia**

- `a1.i2.action1`
- `a1.i3`
- `a1.i9`
- `a1.i21`
- `a1.i22`
- `a1.termination`
- `a2.i1`
- `a2.termination`
- `a3.i1`
- `a3.termination`
- `a4.i1`
- `a4.termination`
- `a5.i1`
- `a5.termination`
- `a6.i1`
- `a6.termination`
- `a7.i1`
- `a7.termination`
- `a8.i1`
- `a8.termination`
- `a9.i1`
- `a9.termination`
- `a10.i1`
- `a10.termination`

**LLM judge — justificación**

El agente presenta una divergencia material entre su estrategia declarada y las acciones elegidas en las iteraciones a1.i13-a1.i19. Su razonamiento indica "usar los libros que tengo en mi inventario", pero nunca verificó su inventario ni tomó (take) ningún libro antes de intentar usarlos. Cada intento de "use" falló con el error "no llevas ningún [libro]", y el agente continuó repitiendo la misma acción con diferentes libros sin corregir el problema fundamental: no tenía los libros en su inventario. Esto constituye un segmento material de 7 acciones consecutivas que no implementan razonablemente la estrategia vigente, ya que la estrategia requería primero adquirir los objetos antes de poder usarlos. Además, tras el "look" en a1.i20 que mostró los libros disponibles en la habitación (no en inventario), el agente no ejecutó ninguna acción correctiva como "take" para obtener los libros, sino que repitió "look" en a1.i21 y luego abandonó toda acción en los attempts subsiguientes (a2-a10), declarando repetidamente que "usó todos los libros en su inventario" cuando en realidad nunca los tuvo.

**LLM judge — evidencia**

- `a1.i13.action1`
- `a1.i14.action1`
- `a1.i15.action1`
- `a1.i16.action1`
- `a1.i17.action1`
- `a1.i18.action1`
- `a1.i19.action1`
- `a1.i20.action1`
- `a1.i21.action1`

#### Q1.4

- Acuerdo: SÍ
- Humano: `FAIL`
- LLM judge: `FAIL`

**Humano — justificación**

El agente no revisa su conducta al revisar libros en su inventario, por más de que nunca los haya tomado y pese a los sucesivos errores.
Tampoco vuelve a cuestionarse si le falta  revisar algo más, simplemente considera que ya examinó todo e insiste en eso.

**Humano — evidencia**

- `a1.i13.action1`
- `a1.i14`
- `a1.i14.action1`
- `a1.i15`
- `a1.i15.action1`
- `a1.i16`
- `a1.i16.action1`
- `a1.i17`
- `a1.i17.action1`
- `a1.i18`
- `a1.i18.action1`
- `a1.i19`
- `a1.i19.action1`
- `a1.i20`
- `a1.i20.action1`
- `a1.i21`
- `a1.i21.action1`
- `a1.i22`
- `a1.termination`
- `a2.i1`
- `a2.termination`

**LLM judge — justificación**

El agente muestra una falta material de adaptación ante feedback adverso repetido. En a1.i13-i19, recibe errores consecutivos indicando "no llevas ningún 'libro_X'" al intentar usar libros que no tiene en inventario, pero persiste en la misma estrategia fallida sin intentar primero recoger (take) los libros. Más crítico aún, tras recibir múltiples mensajes de continuación ("El desafío todavía no está completado. Continuá.") en attempts 2-10, el agente repite exactamente la misma respuesta pasiva sin ejecutar ninguna acción nueva, declarando que "debería pedir ayuda al Usuario" en lugar de intentar acciones alternativas como: tomar los libros, examinar el libro_sermones (nunca examinado), buscar llaves ocultas, o interactuar de otras formas con los objetos. Esta persistencia en la inacción a través de 9 attempts consecutivos, pese al feedback explícito de que el desafío no está completado, constituye una falla material en el monitoreo y replanificación.

**LLM judge — evidencia**

- `a1.i13.action1`
- `a1.i14.action1`
- `a1.i15.action1`
- `a1.i20.action1`
- `a1.i21.action1`
- `a2.user_message`
- `a2.i1`
- `a3.user_message`
- `a3.i1`
- `a10.user_message`
- `a10.i1`

### qc-010

#### Q1.1

- Acuerdo: SÍ
- Humano: `PASS`
- LLM judge: `PASS`

**Humano — justificación**

El agente capta correctamente qué objetos están disponibles en el escenario y cómo podría usarlos, en base a lo que recibe del entorno.

**Humano — evidencia**

- `a1.i2`
- `a1.i3`
- `a1.i4`
- `a1.i5`

**LLM judge — justificación**

Todas las decisiones del agente son consistentes con la evidencia observada. En a1.i1, el agente observa la sala con alfombra, escritorio y puerta cerrada. En a1.i2, examina la alfombra y descubre una llave dorada debajo. En a1.i3, toma la llave basándose en la observación de que existe bajo la alfombra. En a1.i4, usa la llave en la puerta principal, lo cual es coherente con el objetivo de salir y con tener la llave en su inventario. Cada acción se fundamenta correctamente en los hechos establecidos por las observaciones previas, sin contradicciones factuales.

**LLM judge — evidencia**

- `a1.i1.action1`
- `a1.i2.action1`
- `a1.i3.action1`
- `a1.i4.action1`

#### Q1.2

- Acuerdo: SÍ
- Humano: `PASS`
- LLM judge: `PASS`

**Humano — justificación**

El agente identifica su entorno y encadena sus acciones de forma ordenada y efectiva.

**Humano — evidencia**

- `a1.i1.plan1`
- `a1.i1`
- `a1.i2`
- `a1.i3`
- `a1.i4`
- `a1.i5`

**LLM judge — justificación**

El agente identifica y mantiene una estructura razonable de subobjetivos para escapar del estudio. El plan inicial (a1.i1.plan1) establece: explorar la sala, analizar objetos y crear un plan de acción. La ejecución sigue una secuencia lógica de dependencias: (1) explorar la sala para identificar objetos disponibles, (2) examinar objetos para encontrar pistas/herramientas, (3) obtener la llave encontrada, (4) usar la llave en la puerta. Cada subobjetivo es prerrequisito del siguiente: no puede tomar la llave sin haberla descubierto examinando la alfombra, y no puede abrir la puerta sin tener la llave. El agente respeta estas dependencias correctamente y alcanza el objetivo de salir del estudio.

**LLM judge — evidencia**

- `a1.i1.plan1`
- `a1.i1.action1`
- `a1.i2.action1`
- `a1.i3.action1`
- `a1.i4.action1`

#### Q1.3

- Acuerdo: SÍ
- Humano: `PASS`
- LLM judge: `PASS`

**Humano — justificación**

Todas las acciones que toma el agente son coherentes con la estrategia adoptada.

**Humano — evidencia**

- `a1.i1.action1`
- `a1.i2.action1`
- `a1.i3.action1`
- `a1.i4.action1`
- `a1.termination`

**LLM judge — justificación**

Las acciones ejecutadas implementan coherentemente la estrategia planteada. El plan inicial (a1.i1.plan1) establece explorar la sala, analizar objetos y crear un plan de acción. La ejecución sigue esta lógica: (1) look para explorar la sala, (2) examine de la alfombra para analizar objetos, (3) take de la llave encontrada, (4) use de la llave en la puerta. Cada acción tiene una relación directa con el subobjetivo vigente expresado en el thinking de cada iteración y contribuye al progreso hacia el objetivo de salir del estudio. No existe divergencia material entre la estrategia y las acciones elegidas.

**LLM judge — evidencia**

- `a1.i1.plan1`
- `a1.i1.action1`
- `a1.i2.action1`
- `a1.i3.action1`
- `a1.i4.action1`

### qc-011

#### Q1.1

- Acuerdo: SÍ
- Humano: `PASS`
- LLM judge: `PASS`

**Humano — justificación**

En general, da respuestas basadas en la evidencia que recibe del entorno.

**Humano — evidencia**

- `a1.i8.action1`
- `a1.i9`

**LLM judge — justificación**

El agente mantiene consistencia factual con la evidencia a lo largo de la trayectoria. En a1.i8, intenta ir al sur desde la cocina, pero la observación de a1.i5.action1 ya había establecido que la única salida de la cocina era "oeste". Sin embargo, este error se corrige inmediatamente en a1.i9, donde el agente reconoce el error ("Parece que no hay salida hacia el sur desde la cocina") y toma la dirección correcta (oeste). El error fue aislado y corregido al recibir información suficiente, sin afectar materialmente decisiones posteriores. Todas las demás decisiones del agente son compatibles con los hechos establecidos: explora sistemáticamente los ambientes, encuentra la llave en el cajón, la toma, navega correctamente de regreso al recibidor y usa la llave para abrir la puerta principal.

**LLM judge — evidencia**

- `a1.i5.action1`
- `a1.i8.action1`
- `a1.i9`
- `a1.i9.action1`

#### Q1.2

- Acuerdo: SÍ
- Humano: `PASS`
- LLM judge: `PASS`

**Humano — justificación**

El agente planifica y luego desarrolla correctamente una secuencia lógica de potenciales acciones que el permitirían resolver el desafío.

**Humano — evidencia**

- `a1.i1.plan1`
- `a1.i1`
- `a1.i2`
- `a1.i3`
- `a1.i4`
- `a1.i5`
- `a1.i6`
- `a1.i7`
- `a1.i8`
- `a1.i10`
- `a1.i11`

**LLM judge — justificación**

El agente identifica y mantiene una estructura razonable de subobjetivos desde el inicio. En a1.i1.plan1 establece explícitamente: (1) explorar el recibidor, (2) explorar el pasillo buscando objetos útiles, (3) usar la llave para abrir la puerta principal. La trayectoria muestra que el agente sigue esta estructura: explora sistemáticamente los ambientes (recibidor → pasillo → cocina), identifica el cajón como contenedor potencial de la llave, la encuentra y toma, y luego regresa al recibidor para usarla en la puerta. El error de navegación en a1.i8 (intentar ir al sur desde la cocina cuando la salida era oeste) es un error de ejecución local que no afecta la estructura de subobjetivos ni las dependencias; el agente corrige inmediatamente en a1.i9 tomando la dirección correcta. Los prerrequisitos (encontrar llave → tomar llave → volver al recibidor → usar llave en puerta) se mantienen correctamente ordenados durante toda la trayectoria, culminando exitosamente en a1.i11.

**LLM judge — evidencia**

- `a1.i1.plan1`
- `a1.i6.action1`
- `a1.i7.action1`
- `a1.i8.action1`
- `a1.i9.action1`
- `a1.i11.action1`

#### Q1.3

- Acuerdo: SÍ
- Humano: `PASS`
- LLM judge: `PASS`

**Humano — justificación**

El agente aplica las acciones de forma coherente con la estrategia y subojetivo vigentes.

**Humano — evidencia**

- `a1.i1.action1`
- `a1.i2.action1`
- `a1.i3.action1`
- `a1.i4.action1`
- `a1.i5.action1`
- `a1.i6.action1`
- `a1.i7.action1`
- `a1.i9.action1`
- `a1.i10.action1`
- `a1.i11.action1`

**LLM judge — justificación**

Las acciones del agente implementan coherentemente la estrategia vigente a lo largo de toda la trayectoria. El plan inicial (a1.i1.plan1) establece explorar el recibidor, explorar el pasillo, encontrar la llave y usarla para abrir la puerta. Las acciones ejecutadas siguen esta estrategia: look en recibidor (a1.i1), ir al norte hacia el pasillo (a1.i2), look en pasillo (a1.i3), ir al este hacia la cocina (a1.i4), look en cocina (a1.i5), examinar el cajón (a1.i6), tomar la llave (a1.i7), y regresar para usar la llave en la puerta (a1.i8-a1.i11). El error en a1.i8 (intentar ir al sur desde la cocina cuando la salida era oeste) es un error de navegación puntual, pero la acción sigue siendo coherente con el subobjetivo vigente de regresar al recibidor. El agente corrige inmediatamente en a1.i9 usando la dirección correcta (oeste). No existe divergencia material entre la estrategia y las acciones elegidas; todas las acciones mantienen relación razonable con el progreso hacia el objetivo.

**LLM judge — evidencia**

- `a1.i1.plan1`
- `a1.i1.action1`
- `a1.i2.action1`
- `a1.i4.action1`
- `a1.i6.action1`
- `a1.i7.action1`
- `a1.i8.action1`
- `a1.i9.action1`
- `a1.i11.action1`

#### Q1.4

- Acuerdo: SÍ
- Humano: `PASS`
- LLM judge: `PASS`

**Humano — justificación**

El agente se recuperó satisfactoriamente al obtener que el resultado de una de sus acciones no era posible. Luego, ejecutó la acción que sí le permitía progresar de acuerdo a su estrategia.

**Humano — evidencia**

- `a1.i8.action1`
- `a1.i9`
- `a1.i9.action1`

**LLM judge — justificación**

El agente demostró capacidad de adaptación ante feedback adverso. En a1.i8.action1, intentó ir al sur desde la cocina y recibió un error indicando que no había salida sur, solo oeste. En la siguiente iteración (a1.i9), el agente reconoció explícitamente el error ("Parece que no hay salida hacia el sur desde la cocina") y corrigió su conducta usando la dirección correcta (oeste) para volver al pasillo. Esta corrección fue inmediata y efectiva, permitiendo al agente continuar exitosamente hacia el objetivo final de abrir la puerta principal.

**LLM judge — evidencia**

- `a1.i8.action1`
- `a1.i9`
- `a1.i9.action1`

### qc-012

#### Q1.1

- Acuerdo: SÍ
- Humano: `FAIL`
- LLM judge: `FAIL`

**Humano — justificación**

El agente pierde una representación consistente de la topología ya observada. Aunque mantiene como objetivo volver al recibidor para usar la llave, desde el pasillo elige direcciones que la evidencia disponible identifica como inválidas o que conducen nuevamente a la cocina.

**Humano — evidencia**

- `a1.i2.action1`
- `a1.i3.action1`
- `a1.i4.action1`
- `a1.i10`
- `a1.i10.action1`
- `a1.i11.action2`

**LLM judge — justificación**

El agente basa materialmente decisiones en una representación incorrecta del mapa que la evidencia ya había establecido. En a1.i3.action1, el agente observó que el Pasillo tiene salidas "este, sur" (este hacia Cocina, sur hacia Recibidor). Sin embargo, a partir de a1.i9, el agente intenta repetidamente ir al "oeste" desde el Pasillo para llegar al Recibidor (a1.i9.action2, a1.i11.action2), cuando la evidencia establecía claramente que la salida hacia el Recibidor es "sur". Esta creencia errónea persiste a través de múltiples iteraciones (i9, i10, i11) sin que el agente corrija su representación del mapa, a pesar de recibir errores explícitos indicando "no hay salida 'oeste' desde aquí. Salidas disponibles: este, sur." El agente nunca utiliza la dirección "sur" desde el Pasillo para volver al Recibidor donde está la puerta principal, contradiciendo directamente la evidencia observada en a1.i3.action1.

**LLM judge — evidencia**

- `a1.i3.action1`
- `a1.i9.action2`
- `a1.i11.action2`

#### Q1.2

- Acuerdo: SÍ
- Humano: `PASS`
- LLM judge: `PASS`

**Humano — justificación**

La estrategía que intenta seguir es coherente y la mantiene a pesar de estar navengado de forma errática.

**Humano — evidencia**

- `a1.i1`
- `a1.i2`
- `a1.i3`
- `a1.i4`
- `a1.i5`
- `a1.i6`
- `a1.i7`
- `a1.i8`
- `a1.i9.summary1`
- `a1.i10`
- `a1.i11`
- `a1.i12`

**LLM judge — justificación**

El agente identifica y mantiene correctamente la estructura de subobjetivos necesarios para completar la tarea: (1) explorar el apartamento, (2) encontrar la llave, (3) volver al recibidor, (4) usar la llave en la puerta principal. Esta estructura se evidencia desde a1.i1 ("explore the apartment, find the key, and then use it to open the main door") y se mantiene consistentemente. El agente ejecuta correctamente los subobjetivos 1 y 2 (explora recibidor→pasillo→cocina, encuentra y toma la llave en a1.i7). Los errores observados en iteraciones posteriores (a1.i8-a1.i12) son fallos de navegación/ejecución (intentar ir en direcciones incorrectas, intentar usar la llave sin estar en el recibidor), no defectos en la estructura de subobjetivos. El agente nunca abandona ni pierde de vista el subobjetivo de volver al recibidor para usar la llave; simplemente falla repetidamente en la ejecución de la navegación. Estos errores corresponden a Q1.3 (ejecución) o Q1.4 (persistencia ante feedback adverso), pero la estructura estratégica de prerrequisitos (tener la llave antes de usarla, estar en el recibidor para acceder a la puerta) permanece correcta e intacta.

**LLM judge — evidencia**

- `a1.i1.action1`
- `a1.i7.action1`
- `a1.i8.action1`
- `a1.i9.action1`
- `a1.i9.summary1`

#### Q1.3

- Acuerdo: SÍ
- Humano: `FAIL`
- LLM judge: `FAIL`

**Humano — justificación**

Después de obtener la llave, el agente mantiene correctamente el subobjetivo de volver al recibidor, pero varias de sus acciones de navegación no lo implementan razonablemente. Desde el pasillo selecciona direcciones que ya sabe que son inválidas o que lo devuelven a la cocina, en lugar de avanzar hacia el recibidor.

**Humano — evidencia**

- `a1.i10`
- `a1.i10.action1`

**LLM judge — justificación**

Existe una divergencia material entre la estrategia vigente y las acciones elegidas. La estrategia declarada era "volver a la puerta principal para usar la llave", pero el agente ejecuta repetidamente secuencias de acciones incoherentes con ese objetivo. En a1.i9, tras llegar al Pasillo (que tiene salidas este y sur), intenta ir al oeste (inexistente) y usar la llave en una puerta que no está presente. En a1.i10, estando en el Pasillo con salida sur hacia el Recibidor (donde está la puerta principal), va al este hacia la Cocina, alejándose del objetivo. Este patrón se repite en a1.i11 y a1.i12: el agente oscila entre Cocina y Pasillo sin nunca ir al sur hacia el Recibidor, a pesar de que la observación en a1.i3 estableció claramente que el Pasillo "conecta el recibidor al sur". Las acciones elegidas (ir repetidamente al este/oeste entre Cocina y Pasillo) no implementan la estrategia de llegar a la puerta principal, constituyendo un segmento sostenido de acciones sin relación razonable con el progreso hacia el objetivo.

**LLM judge — evidencia**

- `a1.i3.action1`
- `a1.i9.action1`
- `a1.i9.action2`
- `a1.i10.action1`
- `a1.i10.action2`
- `a1.i11.action1`
- `a1.i11.action2`

#### Q1.4

- Acuerdo: SÍ
- Humano: `FAIL`
- LLM judge: `FAIL`

**Humano — justificación**

El agente se recupera de varios errores de navegación, pero hay una oportunidad concreta en la que no incorpora correctamente el feedback disponible. Tras llegar al pasillo y recibir como observación que las salidas disponibles son este y sur, en la decisión siguiente toma este y vuelve a la cocina, aunque su subobjetivo declarado era regresar al recibidor. Los demás errores del episodio no se consideran oportunidades independientes de adaptación cuando ocurren dentro de la misma iteración.

**Humano — evidencia**

- `a1.i10`
- `a1.i10.action1`

**LLM judge — justificación**

El agente persiste materialmente en intentar usar la llave en la puerta principal sin estar en el Recibidor, a pesar de recibir feedback adverso repetido. En a1.i8 recibe el error "no ves ningún 'puerta_principal' aquí" estando en la Cocina. En a1.i9, tras moverse al Pasillo, vuelve a intentar "use llave_oro puerta_principal" y recibe el mismo error. En a1.i10, se mueve de vuelta a la Cocina (dirección incorrecta) y repite el mismo intento fallido. En a1.i11, regresa al Pasillo y nuevamente intenta usar la llave en la puerta principal sin haber llegado al Recibidor. En a1.i12, aún en el Pasillo, propone nuevamente usar la llave en la puerta principal. El agente nunca incorpora el feedback de que debe ir al "sur" desde el Pasillo para llegar al Recibidor donde está la puerta principal, a pesar de que las salidas disponibles ("este, sur") se le informan repetidamente. Esta persistencia en la misma acción fallida (use llave_oro puerta_principal) sin primero navegar correctamente al Recibidor constituye una falta material de adaptación ante feedback adverso sostenido.

**LLM judge — evidencia**

- `a1.i8.action2`
- `a1.i9.action3`
- `a1.i10.action3`
- `a1.i11.action3`
- `a1.i12.action2`
- `a1.i3.action1`
