# Análisis de errores — M3

**Runs:** `m3-tool-repair-comparison-run-002`, `m3-nova-tool-repair-comparison-run-003`

| | |
|---|---|
| Total trials | 480 |
| Exitosos | 169 (35.2%) |
| Fallidos | 311 (64.8%) |
| Cobertura | 311/311 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `planning_failure` | 134 | 43% |
| `max_iterations` | 66 | 21% |
| `hallucination` | 60 | 19% |
| `context_overflow` | 27 | 9% |
| `wrong_tool_use` | 18 | 6% |
| `navigation_error` | 4 | 1% |
| `gave_up_early` | 2 | 1% |

## Por sistema

### minimal / llama3.1 (79 fallos)

| Modo | Trials |
|---|---:|
| `hallucination` | 30 |
| `wrong_tool_use` | 16 |
| `planning_failure` | 13 |
| `context_overflow` | 13 |
| `max_iterations` | 7 |

### minimal / qwen2.5:7b (55 fallos)

| Modo | Trials |
|---|---:|
| `planning_failure` | 48 |
| `max_iterations` | 2 |
| `wrong_tool_use` | 2 |
| `navigation_error` | 2 |
| `gave_up_early` | 1 |

### minimal / nova-lite (15 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 13 |
| `context_overflow` | 2 |

### minimal_tool_repair / llama3.1 (77 fallos)

| Modo | Trials |
|---|---:|
| `hallucination` | 30 |
| `planning_failure` | 19 |
| `max_iterations` | 15 |
| `context_overflow` | 12 |
| `gave_up_early` | 1 |

### minimal_tool_repair / qwen2.5:7b (58 fallos)

| Modo | Trials |
|---|---:|
| `planning_failure` | 50 |
| `max_iterations` | 6 |
| `navigation_error` | 2 |

### minimal_tool_repair / nova-lite (27 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 23 |
| `planning_failure` | 4 |

## Por modelo

### llama3.1 (156 fallos)

| Modo | Trials |
|---|---:|
| `hallucination` | 60 |
| `planning_failure` | 32 |
| `context_overflow` | 25 |
| `max_iterations` | 22 |
| `wrong_tool_use` | 16 |
| `gave_up_early` | 1 |

### qwen2.5:7b (113 fallos)

| Modo | Trials |
|---|---:|
| `planning_failure` | 98 |
| `max_iterations` | 8 |
| `navigation_error` | 4 |
| `wrong_tool_use` | 2 |
| `gave_up_early` | 1 |

### nova-lite (42 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 36 |
| `planning_failure` | 4 |
| `context_overflow` | 2 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| study-with-key | easy | 18 | `hallucination`: 15, `planning_failure`: 2, `wrong_tool_use`: 1 |
| color-locks | medium | 36 | `planning_failure`: 13, `max_iterations`: 10, `context_overflow`: 8, `hallucination`: 4, `wrong_tool_use`: 1 |
| apartment-keys | medium | 32 | `planning_failure`: 20, `max_iterations`: 9, `wrong_tool_use`: 2, `hallucination`: 1 |
| library-search | hard | 44 | `planning_failure`: 29, `hallucination`: 8, `max_iterations`: 6, `wrong_tool_use`: 1 |
| office-sequence | hard | 46 | `planning_failure`: 21, `context_overflow`: 17, `max_iterations`: 7, `wrong_tool_use`: 1 |
| extreme-archive | extreme | 37 | `hallucination`: 18, `planning_failure`: 15, `max_iterations`: 3, `gave_up_early`: 1 |
| vault-combination | extreme | 54 | `planning_failure`: 21, `max_iterations`: 18, `hallucination`: 6, `wrong_tool_use`: 6, `context_overflow`: 2, `gave_up_early`: 1 |
| backtracking-vault | extreme | 44 | `max_iterations`: 13, `planning_failure`: 13, `hallucination`: 8, `wrong_tool_use`: 6, `navigation_error`: 4 |

## Ejemplos por modo

### `hallucination`

**minimal / llama3.1 / study-with-key / trial 1** (4 pasos)
- Razón: narró tool calls como texto en vez de ejecutarlas
- Respuesta: *No puedes tomar la alfombra, ya que es un objeto fijo en el suelo.  {"name": "examine", "parameters": {"target":"puerta_principal"}}*

**minimal / llama3.1 / study-with-key / trial 2** (2 pasos)
- Razón: narró tool calls como texto en vez de ejecutarlas
- Respuesta: *La puerta principal está cerrada. No hay ninguna marca de cerradura visible, pero hay un pequeño mecanismo en la parte inferior que parece ser una ranura para una llave.  Ves:   - alfombra [id: alfomb*

### `planning_failure`

**minimal / llama3.1 / study-with-key / trial 3** (10 pasos)
- Razón: exploró 10 pasos sin alcanzar el objetivo
- Respuesta: *La respuesta es que debemos buscar una llave dorada para abrir la puerta principal. Al examinar el escritorio, encontramos un libro con una nota que dice "La llave se encuentra en un lugar donde no la*

**minimal / llama3.1 / color-locks / trial 2** (14 pasos)
- Razón: exploró 14 pasos sin alcanzar el objetivo
- Respuesta: *La llave plateada está sobre una repisa baja. El cofre azul está cerrado con llave, pero la llave para abrirlo es el mismo color que la cerradura del cofre. Al examinar el cofre rojo se ve que tiene u*

### `wrong_tool_use`

**minimal / llama3.1 / study-with-key / trial 6** (2 pasos)
- Razón: _make_examine.<locals>.examine_impl() got an unexpected keyword argument 'obj'
- Respuesta: *La puerta principal está cerrada. Hay un cerrojo en el centro de la puerta. Ves:   - alfombra [id: alfombra]   - escritorio [id: escritorio]   - cerrojo [id: cerrojo] (cerrado)   - puerta principal [i*

**minimal / llama3.1 / color-locks / trial 5** (32 pasos)
- Razón: _make_take.<locals>.take_impl() got an unexpected keyword argument 'target'
- Respuesta: *La llave plateada está sobre una repisa baja, la puerta principal está cerrada con una cerradura dorada y los cofres están pintados de colores distintos. Al examinar el cofre azul, se encuentra que es*

### `context_overflow`

**minimal / llama3.1 / color-locks / trial 3** (59 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

**minimal / llama3.1 / color-locks / trial 7** (66 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

### `max_iterations`

**minimal / llama3.1 / apartment-keys / trial 1** (51 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**minimal / llama3.1 / apartment-keys / trial 4** (45 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `gave_up_early`

**minimal_tool_repair / llama3.1 / vault-combination / trial 1** (4 pasos)
- Razón: terminó voluntariamente en 4 pasos
- Respuesta: *Para encontrar los tres núcleos de energía, necesito explorar la instalación y buscarlos en las salas correspondientes. Primero, voy a mirar alrededor del vestíbulo para ver si hay alguna pista o obje*

**minimal / qwen2.5:7b / extreme-archive / trial 3** (4 pasos)
- Razón: terminó voluntariamente en 4 pasos
- Respuesta: *El expediente 1387 contiene un memorándum interno sobre la redistribución de despachos en el ala oeste del edificio Cervantes. Aunque no parece contener información directamente relacionada con abrir*

### `navigation_error`

**minimal / qwen2.5:7b / backtracking-vault / trial 3** (16 pasos)
- Razón: no usó go en escenario multi-sala
- Respuesta: *Vamos a intentar tomar la llave oxidada del cofre antiguo nuevamente para asegurarnos de que está en nuestro inventario. Si no lo está, es posible que necesitemos explorar más.  Primero, vamos a usar*

**minimal / qwen2.5:7b / backtracking-vault / trial 5** (33 pasos)
- Razón: no usó go en escenario multi-sala
- Respuesta: *Vamos a intentar usar la técnica de "interactuar" con el cofre nuevamente, esperando que pueda proporcionarnos una forma de interactuar con él o revelar información oculta.  Primero, vamos a examinar*

## Todos los fallos clasificados

| Run | Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---:|---|---|---|---:|---|---|
| m3-tool-repair-comparison-run-002 | 1 | minimal | llama3.1 | study-with-key | 4 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 2 | minimal | llama3.1 | study-with-key | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 3 | minimal | llama3.1 | study-with-key | 10 | `planning_failure` | exploró 10 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal | llama3.1 | study-with-key | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 5 | minimal | llama3.1 | study-with-key | 4 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 6 | minimal | llama3.1 | study-with-key | 2 | `wrong_tool_use` | _make_examine.<locals>.examine_impl() got an unexpected keyw |
| m3-tool-repair-comparison-run-002 | 7 | minimal | llama3.1 | study-with-key | 4 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 9 | minimal | llama3.1 | study-with-key | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 10 | minimal | llama3.1 | study-with-key | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 1 | minimal | llama3.1 | color-locks | 5 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 2 | minimal | llama3.1 | color-locks | 14 | `planning_failure` | exploró 14 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal | llama3.1 | color-locks | 59 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 4 | minimal | llama3.1 | color-locks | 11 | `planning_failure` | exploró 11 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal | llama3.1 | color-locks | 32 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 6 | minimal | llama3.1 | color-locks | 19 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 7 | minimal | llama3.1 | color-locks | 66 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 8 | minimal | llama3.1 | color-locks | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 9 | minimal | llama3.1 | color-locks | 66 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 10 | minimal | llama3.1 | color-locks | 66 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 1 | minimal | llama3.1 | apartment-keys | 51 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 2 | minimal | llama3.1 | apartment-keys | 8 | `wrong_tool_use` | _make_look.<locals>.look_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 3 | minimal | llama3.1 | apartment-keys | 38 | `planning_failure` | exploró 38 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal | llama3.1 | apartment-keys | 45 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 5 | minimal | llama3.1 | apartment-keys | 39 | `planning_failure` | exploró 39 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal | llama3.1 | apartment-keys | 35 | `planning_failure` | exploró 35 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal | llama3.1 | apartment-keys | 8 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 8 | minimal | llama3.1 | apartment-keys | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 9 | minimal | llama3.1 | apartment-keys | 45 | `wrong_tool_use` | _make_look.<locals>.look_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 10 | minimal | llama3.1 | apartment-keys | 8 | `planning_failure` | exploró 8 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal | llama3.1 | library-search | 7 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 3 | minimal | llama3.1 | library-search | 5 | `planning_failure` | exploró 5 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal | llama3.1 | library-search | 5 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 7 | minimal | llama3.1 | library-search | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 8 | minimal | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal | llama3.1 | library-search | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 10 | minimal | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal | llama3.1 | office-sequence | 73 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 2 | minimal | llama3.1 | office-sequence | 66 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 3 | minimal | llama3.1 | office-sequence | 65 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 4 | minimal | llama3.1 | office-sequence | 67 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 5 | minimal | llama3.1 | office-sequence | 67 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 6 | minimal | llama3.1 | office-sequence | 60 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 7 | minimal | llama3.1 | office-sequence | 63 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 8 | minimal | llama3.1 | office-sequence | 51 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 9 | minimal | llama3.1 | office-sequence | 68 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 10 | minimal | llama3.1 | office-sequence | 68 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 1 | minimal | llama3.1 | extreme-archive | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 2 | minimal | llama3.1 | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 3 | minimal | llama3.1 | extreme-archive | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 4 | minimal | llama3.1 | extreme-archive | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 5 | minimal | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 6 | minimal | llama3.1 | extreme-archive | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 7 | minimal | llama3.1 | extreme-archive | 3 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 8 | minimal | llama3.1 | extreme-archive | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 9 | minimal | llama3.1 | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 10 | minimal | llama3.1 | extreme-archive | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 1 | minimal | llama3.1 | vault-combination | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 2 | minimal | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 3 | minimal | llama3.1 | vault-combination | 22 | `wrong_tool_use` | _make_go.<locals>.go_impl() got an unexpected keyword argume |
| m3-tool-repair-comparison-run-002 | 4 | minimal | llama3.1 | vault-combination | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 5 | minimal | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_examine.<locals>.examine_impl() got an unexpected keyw |
| m3-tool-repair-comparison-run-002 | 6 | minimal | llama3.1 | vault-combination | 2 | `hallucination` | declaró éxito cuando el objetivo no estaba cumplido |
| m3-tool-repair-comparison-run-002 | 7 | minimal | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 8 | minimal | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 9 | minimal | llama3.1 | vault-combination | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 10 | minimal | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 1 | minimal | llama3.1 | backtracking-vault | 6 | `wrong_tool_use` | _make_go.<locals>.go_impl() got an unexpected keyword argume |
| m3-tool-repair-comparison-run-002 | 2 | minimal | llama3.1 | backtracking-vault | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 3 | minimal | llama3.1 | backtracking-vault | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 4 | minimal | llama3.1 | backtracking-vault | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 5 | minimal | llama3.1 | backtracking-vault | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 6 | minimal | llama3.1 | backtracking-vault | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 7 | minimal | llama3.1 | backtracking-vault | 6 | `wrong_tool_use` | _make_go.<locals>.go_impl() got an unexpected keyword argume |
| m3-tool-repair-comparison-run-002 | 8 | minimal | llama3.1 | backtracking-vault | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 9 | minimal | llama3.1 | backtracking-vault | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 10 | minimal | llama3.1 | backtracking-vault | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | llama3.1 | study-with-key | 3 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | llama3.1 | study-with-key | 3 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | llama3.1 | study-with-key | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | llama3.1 | study-with-key | 4 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | llama3.1 | study-with-key | 5 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | llama3.1 | study-with-key | 8 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | llama3.1 | study-with-key | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | llama3.1 | study-with-key | 3 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | llama3.1 | study-with-key | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | llama3.1 | color-locks | 11 | `planning_failure` | exploró 11 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | llama3.1 | color-locks | 25 | `planning_failure` | exploró 25 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | llama3.1 | color-locks | 65 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | llama3.1 | color-locks | 60 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | llama3.1 | color-locks | 12 | `planning_failure` | exploró 12 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | llama3.1 | color-locks | 18 | `planning_failure` | exploró 18 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | llama3.1 | color-locks | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | llama3.1 | color-locks | 66 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | llama3.1 | color-locks | 65 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | llama3.1 | color-locks | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | llama3.1 | apartment-keys | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | llama3.1 | apartment-keys | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | llama3.1 | apartment-keys | 13 | `planning_failure` | exploró 13 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | llama3.1 | apartment-keys | 35 | `planning_failure` | exploró 35 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | llama3.1 | apartment-keys | 26 | `planning_failure` | exploró 26 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | llama3.1 | apartment-keys | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | llama3.1 | apartment-keys | 27 | `planning_failure` | exploró 27 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | llama3.1 | apartment-keys | 27 | `planning_failure` | exploró 27 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | llama3.1 | library-search | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | llama3.1 | library-search | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | llama3.1 | library-search | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | llama3.1 | library-search | 5 | `planning_failure` | exploró 5 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | llama3.1 | library-search | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | llama3.1 | office-sequence | 66 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | llama3.1 | office-sequence | 81 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | llama3.1 | office-sequence | 49 | `planning_failure` | exploró 49 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | llama3.1 | office-sequence | 69 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | llama3.1 | office-sequence | 67 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | llama3.1 | office-sequence | 64 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | llama3.1 | office-sequence | 68 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | llama3.1 | office-sequence | 70 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | llama3.1 | office-sequence | 62 | `context_overflow` | ventana de historial agotada |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | llama3.1 | office-sequence | 62 | `planning_failure` | exploró 62 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | llama3.1 | vault-combination | 4 | `gave_up_early` | terminó voluntariamente en 4 pasos |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | llama3.1 | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | llama3.1 | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | llama3.1 | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | llama3.1 | vault-combination | 16 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | llama3.1 | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | llama3.1 | vault-combination | 15 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | llama3.1 | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | llama3.1 | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | llama3.1 | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | llama3.1 | backtracking-vault | 25 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | llama3.1 | backtracking-vault | 16 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | llama3.1 | backtracking-vault | 45 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | llama3.1 | backtracking-vault | 22 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | llama3.1 | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | llama3.1 | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | llama3.1 | backtracking-vault | 27 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | llama3.1 | backtracking-vault | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | llama3.1 | backtracking-vault | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | llama3.1 | backtracking-vault | 3 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| m3-tool-repair-comparison-run-002 | 1 | minimal | qwen2.5:7b | color-locks | 18 | `planning_failure` | exploró 18 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal | qwen2.5:7b | color-locks | 14 | `planning_failure` | exploró 14 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal | qwen2.5:7b | color-locks | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal | qwen2.5:7b | apartment-keys | 21 | `planning_failure` | exploró 21 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal | qwen2.5:7b | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 4 | minimal | qwen2.5:7b | apartment-keys | 17 | `planning_failure` | exploró 17 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal | qwen2.5:7b | apartment-keys | 13 | `planning_failure` | exploró 13 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal | qwen2.5:7b | apartment-keys | 26 | `planning_failure` | exploró 26 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal | qwen2.5:7b | apartment-keys | 34 | `planning_failure` | exploró 34 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal | qwen2.5:7b | library-search | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal | qwen2.5:7b | library-search | 13 | `wrong_tool_use` | _make_look.<locals>.look_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 4 | minimal | qwen2.5:7b | library-search | 20 | `planning_failure` | exploró 20 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal | qwen2.5:7b | library-search | 16 | `planning_failure` | exploró 16 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal | qwen2.5:7b | library-search | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal | qwen2.5:7b | library-search | 24 | `planning_failure` | exploró 24 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal | qwen2.5:7b | library-search | 26 | `planning_failure` | exploró 26 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal | qwen2.5:7b | library-search | 8 | `planning_failure` | exploró 8 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal | qwen2.5:7b | library-search | 19 | `planning_failure` | exploró 19 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal | qwen2.5:7b | office-sequence | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal | qwen2.5:7b | office-sequence | 12 | `planning_failure` | exploró 12 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal | qwen2.5:7b | office-sequence | 13 | `wrong_tool_use` | _make_look.<locals>.look_impl() got an unexpected keyword ar |
| m3-tool-repair-comparison-run-002 | 4 | minimal | qwen2.5:7b | office-sequence | 22 | `planning_failure` | exploró 22 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal | qwen2.5:7b | office-sequence | 25 | `planning_failure` | exploró 25 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal | qwen2.5:7b | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 7 | minimal | qwen2.5:7b | office-sequence | 11 | `planning_failure` | exploró 11 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal | qwen2.5:7b | office-sequence | 17 | `planning_failure` | exploró 17 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal | qwen2.5:7b | office-sequence | 10 | `planning_failure` | exploró 10 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal | qwen2.5:7b | office-sequence | 33 | `planning_failure` | exploró 33 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal | qwen2.5:7b | extreme-archive | 4 | `gave_up_early` | terminó voluntariamente en 4 pasos |
| m3-tool-repair-comparison-run-002 | 4 | minimal | qwen2.5:7b | extreme-archive | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal | qwen2.5:7b | extreme-archive | 10 | `planning_failure` | exploró 10 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal | qwen2.5:7b | extreme-archive | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal | qwen2.5:7b | extreme-archive | 5 | `planning_failure` | exploró 5 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal | qwen2.5:7b | extreme-archive | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal | qwen2.5:7b | extreme-archive | 24 | `planning_failure` | exploró 24 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal | qwen2.5:7b | vault-combination | 17 | `planning_failure` | exploró 17 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal | qwen2.5:7b | vault-combination | 12 | `planning_failure` | exploró 12 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal | qwen2.5:7b | vault-combination | 19 | `planning_failure` | exploró 19 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal | qwen2.5:7b | vault-combination | 21 | `planning_failure` | exploró 21 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal | qwen2.5:7b | vault-combination | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal | qwen2.5:7b | vault-combination | 22 | `planning_failure` | exploró 22 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal | qwen2.5:7b | vault-combination | 8 | `planning_failure` | exploró 8 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal | qwen2.5:7b | vault-combination | 13 | `planning_failure` | exploró 13 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal | qwen2.5:7b | vault-combination | 19 | `planning_failure` | exploró 19 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal | qwen2.5:7b | vault-combination | 17 | `planning_failure` | exploró 17 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal | qwen2.5:7b | backtracking-vault | 11 | `planning_failure` | exploró 11 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal | qwen2.5:7b | backtracking-vault | 8 | `planning_failure` | exploró 8 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal | qwen2.5:7b | backtracking-vault | 16 | `navigation_error` | no usó go en escenario multi-sala |
| m3-tool-repair-comparison-run-002 | 4 | minimal | qwen2.5:7b | backtracking-vault | 10 | `planning_failure` | exploró 10 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal | qwen2.5:7b | backtracking-vault | 33 | `navigation_error` | no usó go en escenario multi-sala |
| m3-tool-repair-comparison-run-002 | 6 | minimal | qwen2.5:7b | backtracking-vault | 16 | `planning_failure` | exploró 16 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal | qwen2.5:7b | backtracking-vault | 22 | `planning_failure` | exploró 22 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal | qwen2.5:7b | backtracking-vault | 24 | `planning_failure` | exploró 24 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal | qwen2.5:7b | backtracking-vault | 27 | `planning_failure` | exploró 27 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal | qwen2.5:7b | backtracking-vault | 38 | `planning_failure` | exploró 38 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | qwen2.5:7b | color-locks | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | qwen2.5:7b | color-locks | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | qwen2.5:7b | color-locks | 22 | `planning_failure` | exploró 22 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | qwen2.5:7b | apartment-keys | 18 | `planning_failure` | exploró 18 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | qwen2.5:7b | apartment-keys | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | qwen2.5:7b | apartment-keys | 26 | `planning_failure` | exploró 26 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | qwen2.5:7b | apartment-keys | 19 | `planning_failure` | exploró 19 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | qwen2.5:7b | apartment-keys | 22 | `planning_failure` | exploró 22 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | qwen2.5:7b | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | qwen2.5:7b | apartment-keys | 18 | `planning_failure` | exploró 18 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | qwen2.5:7b | library-search | 17 | `planning_failure` | exploró 17 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | qwen2.5:7b | library-search | 17 | `planning_failure` | exploró 17 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | qwen2.5:7b | library-search | 13 | `planning_failure` | exploró 13 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | qwen2.5:7b | library-search | 13 | `planning_failure` | exploró 13 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | qwen2.5:7b | library-search | 10 | `planning_failure` | exploró 10 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | qwen2.5:7b | library-search | 23 | `planning_failure` | exploró 23 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | qwen2.5:7b | library-search | 31 | `planning_failure` | exploró 31 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | qwen2.5:7b | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | qwen2.5:7b | library-search | 19 | `planning_failure` | exploró 19 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | qwen2.5:7b | library-search | 11 | `planning_failure` | exploró 11 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | qwen2.5:7b | office-sequence | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | qwen2.5:7b | office-sequence | 19 | `planning_failure` | exploró 19 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | qwen2.5:7b | office-sequence | 12 | `planning_failure` | exploró 12 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | qwen2.5:7b | office-sequence | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | qwen2.5:7b | office-sequence | 32 | `planning_failure` | exploró 32 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | qwen2.5:7b | office-sequence | 11 | `planning_failure` | exploró 11 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | qwen2.5:7b | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | qwen2.5:7b | office-sequence | 24 | `planning_failure` | exploró 24 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | qwen2.5:7b | office-sequence | 27 | `planning_failure` | exploró 27 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | qwen2.5:7b | office-sequence | 27 | `planning_failure` | exploró 27 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | qwen2.5:7b | extreme-archive | 16 | `planning_failure` | exploró 16 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | qwen2.5:7b | extreme-archive | 10 | `planning_failure` | exploró 10 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | qwen2.5:7b | extreme-archive | 27 | `planning_failure` | exploró 27 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | qwen2.5:7b | extreme-archive | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | qwen2.5:7b | extreme-archive | 18 | `planning_failure` | exploró 18 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | qwen2.5:7b | extreme-archive | 19 | `planning_failure` | exploró 19 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | qwen2.5:7b | extreme-archive | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | qwen2.5:7b | extreme-archive | 12 | `planning_failure` | exploró 12 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | qwen2.5:7b | vault-combination | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | qwen2.5:7b | vault-combination | 26 | `planning_failure` | exploró 26 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | qwen2.5:7b | vault-combination | 10 | `planning_failure` | exploró 10 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | qwen2.5:7b | vault-combination | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | qwen2.5:7b | vault-combination | 16 | `planning_failure` | exploró 16 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | qwen2.5:7b | vault-combination | 14 | `planning_failure` | exploró 14 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | qwen2.5:7b | vault-combination | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | qwen2.5:7b | vault-combination | 32 | `planning_failure` | exploró 32 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | qwen2.5:7b | vault-combination | 10 | `planning_failure` | exploró 10 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | qwen2.5:7b | vault-combination | 8 | `planning_failure` | exploró 8 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 1 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 17 | `planning_failure` | exploró 17 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 2 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 26 | `navigation_error` | no usó go en escenario multi-sala |
| m3-tool-repair-comparison-run-002 | 3 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 4 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 21 | `planning_failure` | exploró 21 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 5 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 28 | `planning_failure` | exploró 28 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 6 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 7 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 13 | `planning_failure` | exploró 13 pasos sin alcanzar el objetivo |
| m3-tool-repair-comparison-run-002 | 8 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 9 | `navigation_error` | no usó go en escenario multi-sala |
| m3-tool-repair-comparison-run-002 | 9 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-tool-repair-comparison-run-002 | 10 | minimal_tool_repair | qwen2.5:7b | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 3 | minimal | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 4 | minimal | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 7 | minimal | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 8 | minimal | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 8 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 4 | minimal | nova-lite | office-sequence | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 5 | minimal | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 9 | minimal | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 1 | minimal | nova-lite | vault-combination | 70 | `context_overflow` | ventana de historial agotada |
| m3-nova-tool-repair-comparison-run-003 | 4 | minimal | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 5 | minimal | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 7 | minimal | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 8 | minimal | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 9 | minimal | nova-lite | vault-combination | 68 | `context_overflow` | ventana de historial agotada |
| m3-nova-tool-repair-comparison-run-003 | 9 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 3 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 4 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 5 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 7 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 8 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 10 | minimal_tool_repair | nova-lite | color-locks | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 7 | minimal_tool_repair | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 7 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 8 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 9 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 10 | minimal_tool_repair | nova-lite | library-search | 47 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 4 | minimal_tool_repair | nova-lite | office-sequence | 18 | `planning_failure` | exploró 18 pasos sin alcanzar el objetivo |
| m3-nova-tool-repair-comparison-run-003 | 5 | minimal_tool_repair | nova-lite | office-sequence | 13 | `planning_failure` | exploró 13 pasos sin alcanzar el objetivo |
| m3-nova-tool-repair-comparison-run-003 | 9 | minimal_tool_repair | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 2 | minimal_tool_repair | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 5 | minimal_tool_repair | nova-lite | extreme-archive | 21 | `planning_failure` | exploró 21 pasos sin alcanzar el objetivo |
| m3-nova-tool-repair-comparison-run-003 | 1 | minimal_tool_repair | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 2 | minimal_tool_repair | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 4 | minimal_tool_repair | nova-lite | vault-combination | 52 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 5 | minimal_tool_repair | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 6 | minimal_tool_repair | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 7 | minimal_tool_repair | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 8 | minimal_tool_repair | nova-lite | vault-combination | 27 | `planning_failure` | exploró 27 pasos sin alcanzar el objetivo |
| m3-nova-tool-repair-comparison-run-003 | 9 | minimal_tool_repair | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 3 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 7 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-tool-repair-comparison-run-003 | 8 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
