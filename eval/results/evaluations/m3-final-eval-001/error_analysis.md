# Análisis de errores — M3

**Run:** `m3-final-run-001`

| | |
|---|---|
| Total trials | 320 |
| Exitosos | 173 (54.1%) |
| Fallidos | 147 (45.9%) |
| Cobertura | 147/147 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 72 | 49% |
| `context_overflow` | 70 | 48% |
| `gave_up_early` | 5 | 3% |

## Por sistema

### baseline / nova-lite (21 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 19 |
| `gave_up_early` | 2 |

### planner / nova-lite (22 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 18 |
| `context_overflow` | 2 |
| `gave_up_early` | 2 |

### summary / nova-lite (53 fallos)

| Modo | Trials |
|---|---:|
| `context_overflow` | 33 |
| `max_iterations` | 19 |
| `gave_up_early` | 1 |

### planner_summary / nova-lite (51 fallos)

| Modo | Trials |
|---|---:|
| `context_overflow` | 35 |
| `max_iterations` | 16 |

## Por modelo

### nova-lite (147 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 72 |
| `context_overflow` | 70 |
| `gave_up_early` | 5 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 25 | `max_iterations`: 14, `context_overflow`: 10, `gave_up_early`: 1 |
| library-search | hard | 18 | `max_iterations`: 10, `context_overflow`: 5, `gave_up_early`: 3 |
| office-sequence | hard | 18 | `context_overflow`: 14, `max_iterations`: 4 |
| vault-combination | extreme | 29 | `max_iterations`: 16, `context_overflow`: 13 |
| backtracking-vault | extreme | 32 | `context_overflow`: 17, `max_iterations`: 14, `gave_up_early`: 1 |
| apartment-keys | medium | 7 | `context_overflow`: 6, `max_iterations`: 1 |
| extreme-archive | extreme | 17 | `max_iterations`: 13, `context_overflow`: 4 |
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

## Todos los fallos clasificados

| Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---|---|---|---:|---|---|
| 3 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | baseline | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | baseline | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | baseline | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 9 | baseline | nova-lite | library-search | 4 | `gave_up_early` | terminó voluntariamente en 4 pasos |
| 2 | baseline | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | baseline | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | baseline | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| 5 | baseline | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| 6 | baseline | nova-lite | vault-combination | 44 | `max_iterations` | presupuesto de pasos agotado |
| 7 | baseline | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| 10 | baseline | nova-lite | vault-combination | 45 | `max_iterations` | presupuesto de pasos agotado |
| 2 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | baseline | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner | nova-lite | color-locks | 55 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner | nova-lite | color-locks | 43 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner | nova-lite | color-locks | 42 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner | nova-lite | color-locks | 44 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner | nova-lite | library-search | 67 | `context_overflow` | ventana de historial agotada |
| 3 | planner | nova-lite | library-search | 4 | `gave_up_early` | terminó voluntariamente en 4 pasos |
| 5 | planner | nova-lite | library-search | 43 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner | nova-lite | vault-combination | 76 | `context_overflow` | ventana de historial agotada |
| 10 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner | nova-lite | backtracking-vault | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| 6 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner | nova-lite | backtracking-vault | 41 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | summary | nova-lite | color-locks | 11 | `context_overflow` | ventana de historial agotada |
| 5 | summary | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 6 | summary | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary | nova-lite | color-locks | 9 | `context_overflow` | ventana de historial agotada |
| 10 | summary | nova-lite | color-locks | 42 | `max_iterations` | presupuesto de pasos agotado |
| 2 | summary | nova-lite | apartment-keys | 18 | `context_overflow` | ventana de historial agotada |
| 3 | summary | nova-lite | apartment-keys | 25 | `context_overflow` | ventana de historial agotada |
| 5 | summary | nova-lite | apartment-keys | 24 | `context_overflow` | ventana de historial agotada |
| 9 | summary | nova-lite | apartment-keys | 9 | `context_overflow` | ventana de historial agotada |
| 3 | summary | nova-lite | library-search | 46 | `max_iterations` | presupuesto de pasos agotado |
| 5 | summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | summary | nova-lite | library-search | 16 | `context_overflow` | ventana de historial agotada |
| 7 | summary | nova-lite | library-search | 46 | `max_iterations` | presupuesto de pasos agotado |
| 8 | summary | nova-lite | library-search | 24 | `context_overflow` | ventana de historial agotada |
| 9 | summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | summary | nova-lite | office-sequence | 16 | `context_overflow` | ventana de historial agotada |
| 2 | summary | nova-lite | office-sequence | 10 | `context_overflow` | ventana de historial agotada |
| 3 | summary | nova-lite | office-sequence | 9 | `context_overflow` | ventana de historial agotada |
| 4 | summary | nova-lite | office-sequence | 16 | `context_overflow` | ventana de historial agotada |
| 6 | summary | nova-lite | office-sequence | 29 | `context_overflow` | ventana de historial agotada |
| 7 | summary | nova-lite | office-sequence | 9 | `context_overflow` | ventana de historial agotada |
| 8 | summary | nova-lite | office-sequence | 23 | `context_overflow` | ventana de historial agotada |
| 9 | summary | nova-lite | office-sequence | 23 | `context_overflow` | ventana de historial agotada |
| 10 | summary | nova-lite | office-sequence | 9 | `context_overflow` | ventana de historial agotada |
| 1 | summary | nova-lite | extreme-archive | 9 | `context_overflow` | ventana de historial agotada |
| 2 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary | nova-lite | extreme-archive | 9 | `context_overflow` | ventana de historial agotada |
| 8 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | summary | nova-lite | vault-combination | 50 | `max_iterations` | presupuesto de pasos agotado |
| 2 | summary | nova-lite | vault-combination | 63 | `max_iterations` | presupuesto de pasos agotado |
| 3 | summary | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| 4 | summary | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| 5 | summary | nova-lite | vault-combination | 17 | `context_overflow` | ventana de historial agotada |
| 6 | summary | nova-lite | vault-combination | 23 | `context_overflow` | ventana de historial agotada |
| 7 | summary | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| 8 | summary | nova-lite | vault-combination | 15 | `context_overflow` | ventana de historial agotada |
| 9 | summary | nova-lite | vault-combination | 38 | `context_overflow` | ventana de historial agotada |
| 10 | summary | nova-lite | vault-combination | 24 | `context_overflow` | ventana de historial agotada |
| 1 | summary | nova-lite | backtracking-vault | 16 | `context_overflow` | ventana de historial agotada |
| 2 | summary | nova-lite | backtracking-vault | 16 | `context_overflow` | ventana de historial agotada |
| 3 | summary | nova-lite | backtracking-vault | 9 | `context_overflow` | ventana de historial agotada |
| 4 | summary | nova-lite | backtracking-vault | 9 | `context_overflow` | ventana de historial agotada |
| 5 | summary | nova-lite | backtracking-vault | 16 | `context_overflow` | ventana de historial agotada |
| 6 | summary | nova-lite | backtracking-vault | 38 | `context_overflow` | ventana de historial agotada |
| 7 | summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | summary | nova-lite | backtracking-vault | 24 | `context_overflow` | ventana de historial agotada |
| 9 | summary | nova-lite | backtracking-vault | 23 | `context_overflow` | ventana de historial agotada |
| 10 | summary | nova-lite | backtracking-vault | 9 | `context_overflow` | ventana de historial agotada |
| 2 | planner_summary | nova-lite | study-with-key | 16 | `context_overflow` | ventana de historial agotada |
| 1 | planner_summary | nova-lite | color-locks | 16 | `context_overflow` | ventana de historial agotada |
| 2 | planner_summary | nova-lite | color-locks | 37 | `context_overflow` | ventana de historial agotada |
| 4 | planner_summary | nova-lite | color-locks | 35 | `context_overflow` | ventana de historial agotada |
| 5 | planner_summary | nova-lite | color-locks | 9 | `context_overflow` | ventana de historial agotada |
| 6 | planner_summary | nova-lite | color-locks | 19 | `context_overflow` | ventana de historial agotada |
| 7 | planner_summary | nova-lite | color-locks | 13 | `context_overflow` | ventana de historial agotada |
| 9 | planner_summary | nova-lite | color-locks | 37 | `context_overflow` | ventana de historial agotada |
| 10 | planner_summary | nova-lite | color-locks | 11 | `context_overflow` | ventana de historial agotada |
| 9 | planner_summary | nova-lite | apartment-keys | 9 | `context_overflow` | ventana de historial agotada |
| 10 | planner_summary | nova-lite | apartment-keys | 9 | `context_overflow` | ventana de historial agotada |
| 3 | planner_summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary | nova-lite | library-search | 47 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_summary | nova-lite | library-search | 17 | `context_overflow` | ventana de historial agotada |
| 8 | planner_summary | nova-lite | library-search | 20 | `context_overflow` | ventana de historial agotada |
| 2 | planner_summary | nova-lite | office-sequence | 16 | `context_overflow` | ventana de historial agotada |
| 4 | planner_summary | nova-lite | office-sequence | 16 | `context_overflow` | ventana de historial agotada |
| 5 | planner_summary | nova-lite | office-sequence | 47 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary | nova-lite | office-sequence | 37 | `context_overflow` | ventana de historial agotada |
| 7 | planner_summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary | nova-lite | office-sequence | 30 | `context_overflow` | ventana de historial agotada |
| 9 | planner_summary | nova-lite | office-sequence | 18 | `context_overflow` | ventana de historial agotada |
| 1 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary | nova-lite | extreme-archive | 9 | `context_overflow` | ventana de historial agotada |
| 9 | planner_summary | nova-lite | extreme-archive | 2 | `context_overflow` | ventana de historial agotada |
| 10 | planner_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner_summary | nova-lite | vault-combination | 31 | `context_overflow` | ventana de historial agotada |
| 2 | planner_summary | nova-lite | vault-combination | 46 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary | nova-lite | vault-combination | 23 | `context_overflow` | ventana de historial agotada |
| 4 | planner_summary | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary | nova-lite | vault-combination | 16 | `context_overflow` | ventana de historial agotada |
| 6 | planner_summary | nova-lite | vault-combination | 16 | `context_overflow` | ventana de historial agotada |
| 7 | planner_summary | nova-lite | vault-combination | 48 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary | nova-lite | vault-combination | 16 | `context_overflow` | ventana de historial agotada |
| 9 | planner_summary | nova-lite | vault-combination | 39 | `context_overflow` | ventana de historial agotada |
| 10 | planner_summary | nova-lite | vault-combination | 37 | `context_overflow` | ventana de historial agotada |
| 1 | planner_summary | nova-lite | backtracking-vault | 9 | `context_overflow` | ventana de historial agotada |
| 2 | planner_summary | nova-lite | backtracking-vault | 30 | `context_overflow` | ventana de historial agotada |
| 3 | planner_summary | nova-lite | backtracking-vault | 23 | `context_overflow` | ventana de historial agotada |
| 4 | planner_summary | nova-lite | backtracking-vault | 23 | `context_overflow` | ventana de historial agotada |
| 5 | planner_summary | nova-lite | backtracking-vault | 37 | `context_overflow` | ventana de historial agotada |
| 6 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_summary | nova-lite | backtracking-vault | 18 | `context_overflow` | ventana de historial agotada |
| 8 | planner_summary | nova-lite | backtracking-vault | 23 | `context_overflow` | ventana de historial agotada |
| 9 | planner_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner_summary | nova-lite | backtracking-vault | 17 | `context_overflow` | ventana de historial agotada |
