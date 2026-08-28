# Análisis de errores — M3

**Runs:** `m3-final-run-001`, `m3-final-run-002`

| | |
|---|---|
| Total trials | 640 |
| Exitosos | 384 (60.0%) |
| Fallidos | 256 (40.0%) |
| Cobertura | 256/256 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 156 | 61% |
| `context_overflow` | 71 | 28% |
| `gave_up_early` | 27 | 11% |
| `planning_failure` | 2 | 1% |

## Por sistema

### baseline / nova-lite (47 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 42 |
| `gave_up_early` | 4 |
| `planning_failure` | 1 |

### planner / nova-lite (39 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 31 |
| `gave_up_early` | 5 |
| `context_overflow` | 2 |
| `planning_failure` | 1 |

### summary / nova-lite (88 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 42 |
| `context_overflow` | 34 |
| `gave_up_early` | 12 |

### planner_summary / nova-lite (82 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 41 |
| `context_overflow` | 35 |
| `gave_up_early` | 6 |

## Por modelo

### nova-lite (256 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 156 |
| `context_overflow` | 71 |
| `gave_up_early` | 27 |
| `planning_failure` | 2 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 34 | `max_iterations`: 19, `context_overflow`: 10, `gave_up_early`: 4, `planning_failure`: 1 |
| library-search | hard | 30 | `max_iterations`: 21, `context_overflow`: 5, `gave_up_early`: 4 |
| office-sequence | hard | 31 | `context_overflow`: 14, `max_iterations`: 10, `gave_up_early`: 7 |
| vault-combination | extreme | 56 | `max_iterations`: 37, `context_overflow`: 14, `gave_up_early`: 5 |
| backtracking-vault | extreme | 60 | `max_iterations`: 39, `context_overflow`: 17, `gave_up_early`: 3, `planning_failure`: 1 |
| apartment-keys | medium | 8 | `context_overflow`: 6, `max_iterations`: 2 |
| extreme-archive | extreme | 36 | `max_iterations`: 28, `context_overflow`: 4, `gave_up_early`: 4 |
| study-with-key | easy | 1 | `context_overflow`: 1 |

## Ejemplos por modo

### `max_iterations`

**baseline / nova-lite / color-locks / trial 3** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**baseline / nova-lite / color-locks / trial 4** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `gave_up_early`

**baseline / nova-lite / library-search / trial 3** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *<thinking>I have examined all the objects in the room and used all the books I have in my inventory, but I still can't find a way to unlock the door or the safe. I should try to ask the User for help.*

**baseline / nova-lite / library-search / trial 9** (4 pasos)
- Razón: terminó voluntariamente en 4 pasos
- Respuesta: *<thinking>The desk is empty, and I've already examined the volumes on the shelf and the main door multiple times. I don't have any other tools or information to help me unlock the door or the safe. I'*

### `context_overflow`

**planner / nova-lite / library-search / trial 2** (67 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

**planner / nova-lite / vault-combination / trial 7** (76 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

### `planning_failure`

**baseline / nova-lite / color-locks / trial 6** (9 pasos)
- Razón: exploró 9 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>La llave plateada está presente en mi inventario, pero parece que todavía hay un error al intentar usarla en la cerradura dorada. Debo considerar la posibilidad de que la llave correcta esté*

**planner / nova-lite / backtracking-vault / trial 8** (6 pasos)
- Razón: exploró 6 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>La llave intermedia no abre el cofre antiguo. Parece que he agotado todas las opciones disponibles en la Sala A y no he encontrado la llave oxidada. Debo reconsiderar mi estrategia y buscar*

## Todos los fallos clasificados

| Run | Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---:|---|---|---|---:|---|---|
| m3-final-run-001 | 3 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 4 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 5 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 10 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 2 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 3 | baseline | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-001 | 9 | baseline | nova-lite | library-search | 4 | `gave_up_early` | terminó voluntariamente en 4 pasos |
| m3-final-run-001 | 2 | baseline | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 4 | baseline | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 2 | baseline | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 5 | baseline | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 6 | baseline | nova-lite | vault-combination | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | baseline | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 10 | baseline | nova-lite | vault-combination | 45 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 2 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 3 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 4 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 5 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 1 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 4 | planner | nova-lite | color-locks | 55 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 5 | planner | nova-lite | color-locks | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | planner | nova-lite | color-locks | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 9 | planner | nova-lite | color-locks | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 10 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 9 | planner | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 1 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 2 | planner | nova-lite | library-search | 67 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 3 | planner | nova-lite | library-search | 4 | `gave_up_early` | terminó voluntariamente en 4 pasos |
| m3-final-run-001 | 5 | planner | nova-lite | library-search | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 6 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 1 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 3 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | planner | nova-lite | vault-combination | 76 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 1 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 2 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 4 | planner | nova-lite | backtracking-vault | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| m3-final-run-001 | 6 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | planner | nova-lite | backtracking-vault | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 3 | summary | nova-lite | color-locks | 11 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 5 | summary | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-001 | 6 | summary | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | summary | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 9 | summary | nova-lite | color-locks | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | summary | nova-lite | color-locks | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 2 | summary | nova-lite | apartment-keys | 18 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 3 | summary | nova-lite | apartment-keys | 25 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 5 | summary | nova-lite | apartment-keys | 24 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | summary | nova-lite | apartment-keys | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 3 | summary | nova-lite | library-search | 46 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 5 | summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 6 | summary | nova-lite | library-search | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 7 | summary | nova-lite | library-search | 46 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | summary | nova-lite | library-search | 24 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 1 | summary | nova-lite | office-sequence | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 2 | summary | nova-lite | office-sequence | 10 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 3 | summary | nova-lite | office-sequence | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 4 | summary | nova-lite | office-sequence | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 6 | summary | nova-lite | office-sequence | 29 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 7 | summary | nova-lite | office-sequence | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 8 | summary | nova-lite | office-sequence | 23 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | summary | nova-lite | office-sequence | 23 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | summary | nova-lite | office-sequence | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 1 | summary | nova-lite | extreme-archive | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 2 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 3 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 4 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 6 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | summary | nova-lite | extreme-archive | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 8 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 10 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 1 | summary | nova-lite | vault-combination | 50 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 2 | summary | nova-lite | vault-combination | 63 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 3 | summary | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 4 | summary | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 5 | summary | nova-lite | vault-combination | 17 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 6 | summary | nova-lite | vault-combination | 23 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 7 | summary | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | summary | nova-lite | vault-combination | 15 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | summary | nova-lite | vault-combination | 38 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | summary | nova-lite | vault-combination | 24 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 1 | summary | nova-lite | backtracking-vault | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 2 | summary | nova-lite | backtracking-vault | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 3 | summary | nova-lite | backtracking-vault | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 4 | summary | nova-lite | backtracking-vault | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 5 | summary | nova-lite | backtracking-vault | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 6 | summary | nova-lite | backtracking-vault | 38 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 7 | summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | summary | nova-lite | backtracking-vault | 24 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | summary | nova-lite | backtracking-vault | 23 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | summary | nova-lite | backtracking-vault | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 2 | planner_summary | nova-lite | study-with-key | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 1 | planner_summary | nova-lite | color-locks | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 2 | planner_summary | nova-lite | color-locks | 37 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 4 | planner_summary | nova-lite | color-locks | 35 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 5 | planner_summary | nova-lite | color-locks | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 6 | planner_summary | nova-lite | color-locks | 19 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 7 | planner_summary | nova-lite | color-locks | 13 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | planner_summary | nova-lite | color-locks | 37 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | planner_summary | nova-lite | color-locks | 11 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | planner_summary | nova-lite | apartment-keys | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | planner_summary | nova-lite | apartment-keys | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 3 | planner_summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 5 | planner_summary | nova-lite | library-search | 47 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | planner_summary | nova-lite | library-search | 17 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 8 | planner_summary | nova-lite | library-search | 20 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 2 | planner_summary | nova-lite | office-sequence | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 4 | planner_summary | nova-lite | office-sequence | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 5 | planner_summary | nova-lite | office-sequence | 47 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 6 | planner_summary | nova-lite | office-sequence | 37 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 7 | planner_summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | planner_summary | nova-lite | office-sequence | 30 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | planner_summary | nova-lite | office-sequence | 18 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 1 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 2 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 3 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 4 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 6 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | planner_summary | nova-lite | extreme-archive | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | planner_summary | nova-lite | extreme-archive | 2 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 1 | planner_summary | nova-lite | vault-combination | 31 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 2 | planner_summary | nova-lite | vault-combination | 46 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 3 | planner_summary | nova-lite | vault-combination | 23 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 4 | planner_summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 5 | planner_summary | nova-lite | vault-combination | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 6 | planner_summary | nova-lite | vault-combination | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 7 | planner_summary | nova-lite | vault-combination | 48 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 8 | planner_summary | nova-lite | vault-combination | 16 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | planner_summary | nova-lite | vault-combination | 39 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 10 | planner_summary | nova-lite | vault-combination | 37 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 1 | planner_summary | nova-lite | backtracking-vault | 9 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 2 | planner_summary | nova-lite | backtracking-vault | 30 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 3 | planner_summary | nova-lite | backtracking-vault | 23 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 4 | planner_summary | nova-lite | backtracking-vault | 23 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 5 | planner_summary | nova-lite | backtracking-vault | 37 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 6 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 7 | planner_summary | nova-lite | backtracking-vault | 18 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 8 | planner_summary | nova-lite | backtracking-vault | 23 | `context_overflow` | ventana de historial agotada |
| m3-final-run-001 | 9 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-001 | 10 | planner_summary | nova-lite | backtracking-vault | 17 | `context_overflow` | ventana de historial agotada |
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
