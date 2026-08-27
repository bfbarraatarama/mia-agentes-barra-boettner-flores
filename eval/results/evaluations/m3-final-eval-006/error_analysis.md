# Análisis de errores — M3

**Runs:** `m3-final-run-002`, `m3-final-run-006`

| | |
|---|---|
| Total trials | 480 |
| Exitosos | 309 (64.4%) |
| Fallidos | 171 (35.6%) |
| Cobertura | 171/171 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 138 | 81% |
| `gave_up_early` | 30 | 18% |
| `planning_failure` | 2 | 1% |
| `context_overflow` | 1 | 1% |

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

### summary_token_trigger / nova-lite (29 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 25 |
| `gave_up_early` | 4 |

### planner_summary_token_trigger / nova-lite (33 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 29 |
| `gave_up_early` | 4 |

## Por modelo

### nova-lite (171 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 138 |
| `gave_up_early` | 30 |
| `planning_failure` | 2 |
| `context_overflow` | 1 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 20 | `max_iterations`: 15, `gave_up_early`: 4, `planning_failure`: 1 |
| apartment-keys | medium | 3 | `max_iterations`: 3 |
| library-search | hard | 18 | `max_iterations`: 17, `gave_up_early`: 1 |
| office-sequence | hard | 19 | `max_iterations`: 10, `gave_up_early`: 9 |
| extreme-archive | extreme | 37 | `max_iterations`: 28, `gave_up_early`: 9 |
| vault-combination | extreme | 40 | `max_iterations`: 34, `gave_up_early`: 5, `context_overflow`: 1 |
| backtracking-vault | extreme | 34 | `max_iterations`: 31, `gave_up_early`: 2, `planning_failure`: 1 |

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
| m3-final-run-006 | 2 | summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 3 | summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 4 | summary_token_trigger | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-006 | 5 | summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 9 | summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 10 | summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 4 | summary_token_trigger | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 7 | summary_token_trigger | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 1 | summary_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 6 | summary_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 10 | summary_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 5 | summary_token_trigger | nova-lite | office-sequence | 2 | `gave_up_early` | terminó voluntariamente en 2 pasos |
| m3-final-run-006 | 8 | summary_token_trigger | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 1 | summary_token_trigger | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-006 | 2 | summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 3 | summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 5 | summary_token_trigger | nova-lite | extreme-archive | 90 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 6 | summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 7 | summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 8 | summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 9 | summary_token_trigger | nova-lite | extreme-archive | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| m3-final-run-006 | 10 | summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 4 | summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 5 | summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 6 | summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 7 | summary_token_trigger | nova-lite | vault-combination | 3 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 9 | summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 3 | summary_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 7 | summary_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 5 | planner_summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 6 | planner_summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 7 | planner_summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 9 | planner_summary_token_trigger | nova-lite | color-locks | 115 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 10 | planner_summary_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 1 | planner_summary_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 3 | planner_summary_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 5 | planner_summary_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 1 | planner_summary_token_trigger | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 3 | planner_summary_token_trigger | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 7 | planner_summary_token_trigger | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-006 | 9 | planner_summary_token_trigger | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 1 | planner_summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 2 | planner_summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 3 | planner_summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 4 | planner_summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 5 | planner_summary_token_trigger | nova-lite | extreme-archive | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| m3-final-run-006 | 6 | planner_summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 7 | planner_summary_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 8 | planner_summary_token_trigger | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-006 | 9 | planner_summary_token_trigger | nova-lite | extreme-archive | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| m3-final-run-006 | 2 | planner_summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 3 | planner_summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 4 | planner_summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 5 | planner_summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 6 | planner_summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 7 | planner_summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 8 | planner_summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 10 | planner_summary_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 2 | planner_summary_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 4 | planner_summary_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 5 | planner_summary_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-006 | 9 | planner_summary_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
