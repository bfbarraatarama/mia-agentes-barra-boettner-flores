# Análisis de errores — M3

**Runs:** `m3-final-run-002`, `m3-final-run-003`

| | |
|---|---|
| Total trials | 640 |
| Exitosos | 412 (64.4%) |
| Fallidos | 228 (35.6%) |
| Cobertura | 228/228 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 183 | 80% |
| `gave_up_early` | 41 | 18% |
| `planning_failure` | 2 | 1% |
| `context_overflow` | 1 | 0% |
| `planning_order` | 1 | 0% |

## Por sistema

### baseline / nova-lite (26 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 23 |
| `gave_up_early` | 2 |
| `planning_failure` | 1 |

### planner / nova-lite (17 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 13 |
| `gave_up_early` | 3 |
| `planning_failure` | 1 |

### summary / nova-lite (35 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 23 |
| `gave_up_early` | 11 |
| `context_overflow` | 1 |

### planner_summary / nova-lite (31 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 25 |
| `gave_up_early` | 6 |

### baseline_incremental / nova-lite (24 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 23 |
| `gave_up_early` | 1 |

### planner_incremental / nova-lite (25 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 22 |
| `gave_up_early` | 2 |
| `planning_order` | 1 |

### summary_incremental / nova-lite (31 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 25 |
| `gave_up_early` | 6 |

### planner_summary_incremental / nova-lite (39 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 29 |
| `gave_up_early` | 10 |

## Por modelo

### nova-lite (228 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 183 |
| `gave_up_early` | 41 |
| `planning_failure` | 2 |
| `context_overflow` | 1 |
| `planning_order` | 1 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 16 | `max_iterations`: 10, `gave_up_early`: 5, `planning_failure`: 1 |
| apartment-keys | medium | 2 | `max_iterations`: 2 |
| library-search | hard | 25 | `max_iterations`: 23, `gave_up_early`: 2 |
| office-sequence | hard | 27 | `max_iterations`: 15, `gave_up_early`: 11, `planning_order`: 1 |
| extreme-archive | extreme | 44 | `max_iterations`: 38, `gave_up_early`: 6 |
| vault-combination | extreme | 58 | `max_iterations`: 49, `gave_up_early`: 8, `context_overflow`: 1 |
| backtracking-vault | extreme | 55 | `max_iterations`: 46, `gave_up_early`: 8, `planning_failure`: 1 |
| study-with-key | easy | 1 | `gave_up_early`: 1 |

## Ejemplos por modo

### `max_iterations`

**baseline / nova-lite / color-locks / trial 1** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**baseline / nova-lite / color-locks / trial 2** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `planning_failure`

**baseline / nova-lite / color-locks / trial 6** (9 pasos)
- Razón: exploró 9 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>La llave plateada está presente en mi inventario, pero parece que todavía hay un error al intentar usarla en la cerradura dorada. Debo considerar la posibilidad de que la llave correcta esté*

**planner / nova-lite / backtracking-vault / trial 8** (6 pasos)
- Razón: exploró 6 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>La llave intermedia no abre el cofre antiguo. Parece que he agotado todas las opciones disponibles en la Sala A y no he encontrado la llave oxidada. Debo reconsiderar mi estrategia y buscar*

### `gave_up_early`

**baseline / nova-lite / color-locks / trial 9** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *<thinking>Parece que no hay una forma obvia de salir de la sala con las herramientas y objetos disponibles. Voy a pedir ayuda al usuario para ver si tienen alguna sugerencia o pista para salir de la s*

**baseline / nova-lite / office-sequence / trial 10** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *<thinking>Parece que no puedo obtener la llave de la caja fuerte en esta sala. Debo buscar otra forma de completar la misión.</thinking>*

### `context_overflow`

**summary / nova-lite / vault-combination / trial 7** (37 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=20.*

### `planning_order`

**planner_incremental / nova-lite / office-sequence / trial 9** (0 pasos)
- Razón: condiciones cumplidas en orden incorrecto
- Respuesta: *<thinking>Parece que hay un error en el sistema que no me permite salir por la puerta principal. Debo informar al usuario sobre el problema y sugerir que revisen el sistema o prueben otra estrategia.<*

## Todos los fallos clasificados

| Run | Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---:|---|---|---|---:|---|---|
| m3-final-run-002 | 1 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 6 | baseline | nova-lite | color-locks | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| m3-final-run-002 | 8 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | baseline | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 2 | baseline | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 4 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 6 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 7 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | baseline | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | baseline | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 2 | baseline | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | baseline | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | baseline | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | baseline | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 1 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 6 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 7 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | planner | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 5 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 1 | planner | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | planner | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 5 | planner | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 2 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 4 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 1 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | planner | nova-lite | backtracking-vault | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| m3-final-run-002 | 9 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | summary | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 5 | summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | summary | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 5 | summary | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 7 | summary | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 9 | summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 1 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | summary | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 4 | summary | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 5 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 7 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | summary | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 1 | summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | summary | nova-lite | vault-combination | 46 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 4 | summary | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 5 | summary | nova-lite | vault-combination | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 6 | summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 7 | summary | nova-lite | vault-combination | 37 | `context_overflow` | ventana de historial agotada |
| m3-final-run-002 | 8 | summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | summary | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 1 | summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | summary | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 6 | summary | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 7 | summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | summary | nova-lite | backtracking-vault | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | planner_summary | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 2 | planner_summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | planner_summary | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 6 | planner_summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | planner_summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 1 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 4 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 6 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 7 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | planner_summary | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 10 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 1 | planner_summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 3 | planner_summary | nova-lite | vault-combination | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 4 | planner_summary | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 5 | planner_summary | nova-lite | vault-combination | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| m3-final-run-002 | 6 | planner_summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 7 | planner_summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | planner_summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | planner_summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | planner_summary | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-002 | 1 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 2 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 4 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 5 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 6 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 8 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 9 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-002 | 10 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | baseline_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 1 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 3 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | baseline_incremental | nova-lite | office-sequence | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 3 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | baseline_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 3 | baseline_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | baseline_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 8 | baseline_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | baseline_incremental | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 7 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | planner_incremental | nova-lite | study-with-key | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 6 | planner_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | planner_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | planner_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | planner_incremental | nova-lite | apartment-keys | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 1 | planner_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 3 | planner_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 8 | planner_incremental | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 6 | planner_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | planner_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | planner_incremental | nova-lite | office-sequence | 0 | `planning_order` | condiciones cumplidas en orden incorrecto |
| m3-final-run-003 | 1 | planner_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | planner_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | planner_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | summary_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | summary_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | summary_incremental | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 3 | summary_incremental | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 4 | summary_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | summary_incremental | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 1 | summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 8 | summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 1 | summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 3 | summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 8 | summary_incremental | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 9 | summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 1 | summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 3 | summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | summary_incremental | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 8 | summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | summary_incremental | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 2 | planner_summary_incremental | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 6 | planner_summary_incremental | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 9 | planner_summary_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | planner_summary_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | planner_summary_incremental | nova-lite | library-search | 46 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | planner_summary_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | planner_summary_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | planner_summary_incremental | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 9 | planner_summary_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | planner_summary_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 1 | planner_summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | planner_summary_incremental | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 3 | planner_summary_incremental | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 4 | planner_summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | planner_summary_incremental | nova-lite | extreme-archive | 160 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | planner_summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 7 | planner_summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 8 | planner_summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | planner_summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | planner_summary_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 1 | planner_summary_incremental | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 2 | planner_summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 3 | planner_summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | planner_summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | planner_summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | planner_summary_incremental | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 7 | planner_summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 8 | planner_summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 9 | planner_summary_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 10 | planner_summary_incremental | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 1 | planner_summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 2 | planner_summary_incremental | nova-lite | backtracking-vault | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 3 | planner_summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 4 | planner_summary_incremental | nova-lite | backtracking-vault | 60 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 5 | planner_summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-003 | 6 | planner_summary_incremental | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 7 | planner_summary_incremental | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 9 | planner_summary_incremental | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-003 | 10 | planner_summary_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
