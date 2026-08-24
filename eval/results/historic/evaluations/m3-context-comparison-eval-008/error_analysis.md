# Análisis de errores — M3

**Runs:** `m3-nova-multi-attempt-run-004`, `m3-context-comparison-run-005`

| | |
|---|---|
| Total trials | 400 |
| Exitosos | 275 (68.8%) |
| Fallidos | 125 (31.2%) |
| Cobertura | 125/125 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 110 | 88% |
| `gave_up_early` | 7 | 6% |
| `context_overflow` | 7 | 6% |
| `planning_failure` | 1 | 1% |

## Por sistema

### minimal / nova-lite (25 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 20 |
| `gave_up_early` | 3 |
| `context_overflow` | 2 |

### minimal_tool_repair / nova-lite (24 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 23 |
| `context_overflow` | 1 |

### minimal_history_200 / nova-lite (20 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 17 |
| `gave_up_early` | 2 |
| `context_overflow` | 1 |

### minimal_compaction / nova-lite (26 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 23 |
| `gave_up_early` | 2 |
| `planning_failure` | 1 |

### minimal_summary / nova-lite (30 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 27 |
| `context_overflow` | 3 |

## Por modelo

### nova-lite (125 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 110 |
| `gave_up_early` | 7 |
| `context_overflow` | 7 |
| `planning_failure` | 1 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 19 | `max_iterations`: 16, `gave_up_early`: 3 |
| apartment-keys | medium | 5 | `max_iterations`: 4, `context_overflow`: 1 |
| library-search | hard | 25 | `max_iterations`: 23, `planning_failure`: 1, `gave_up_early`: 1 |
| office-sequence | hard | 19 | `max_iterations`: 15, `gave_up_early`: 3, `context_overflow`: 1 |
| extreme-archive | extreme | 7 | `max_iterations`: 6, `context_overflow`: 1 |
| vault-combination | extreme | 30 | `max_iterations`: 26, `context_overflow`: 4 |
| backtracking-vault | extreme | 20 | `max_iterations`: 20 |

## Ejemplos por modo

### `gave_up_early`

**minimal / nova-lite / color-locks / trial 4** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *<thinking>Parece que no hay otra forma de salir de la sala que no sea encontrar una llave que pueda abrir la puerta principal. La llave plateada no parece ser la correcta, y los cofres no contienen ni*

**minimal / nova-lite / office-sequence / trial 2** (1 pasos)
- Razón: terminó voluntariamente en 1 pasos
- Respuesta: *<thinking>Parece que no hay otra forma de obtener la llave de la caja fuerte. Debo informar al usuario que no puedo completar la misión con las herramientas actuales.</thinking>  <response>No puedo co*

### `max_iterations`

**minimal / nova-lite / color-locks / trial 10** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**minimal / nova-lite / apartment-keys / trial 4** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `context_overflow`

**minimal / nova-lite / vault-combination / trial 1** (64 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

**minimal / nova-lite / vault-combination / trial 9** (70 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

### `planning_failure`

**minimal_compaction / nova-lite / library-search / trial 4** (7 pasos)
- Razón: exploró 7 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>I can't use the book on another book because I don't have it in my inventory. I have tried to use the books on the safe and the main door, and I have tried to use the books on each other and*

## Todos los fallos clasificados

| Run | Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---:|---|---|---|---:|---|---|
| m3-nova-multi-attempt-run-004 | 4 | minimal | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-nova-multi-attempt-run-004 | 10 | minimal | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 4 | minimal | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 1 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 3 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 4 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 6 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 7 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 9 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 2 | minimal | nova-lite | office-sequence | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| m3-nova-multi-attempt-run-004 | 3 | minimal | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-nova-multi-attempt-run-004 | 5 | minimal | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 9 | minimal | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 1 | minimal | nova-lite | vault-combination | 64 | `context_overflow` | ventana de historial agotada |
| m3-nova-multi-attempt-run-004 | 4 | minimal | nova-lite | vault-combination | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 5 | minimal | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 7 | minimal | nova-lite | vault-combination | 50 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 9 | minimal | nova-lite | vault-combination | 70 | `context_overflow` | ventana de historial agotada |
| m3-nova-multi-attempt-run-004 | 10 | minimal | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 1 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 2 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 3 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 4 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 5 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 8 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 2 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 4 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 6 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 10 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 4 | minimal_tool_repair | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 1 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 2 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 3 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 5 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 6 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 7 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 10 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 2 | minimal_tool_repair | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 3 | minimal_tool_repair | nova-lite | office-sequence | 46 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 5 | minimal_tool_repair | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 10 | minimal_tool_repair | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 6 | minimal_tool_repair | nova-lite | vault-combination | 47 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 7 | minimal_tool_repair | nova-lite | vault-combination | 61 | `context_overflow` | ventana de historial agotada |
| m3-nova-multi-attempt-run-004 | 9 | minimal_tool_repair | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 10 | minimal_tool_repair | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 3 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 5 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 6 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-nova-multi-attempt-run-004 | 8 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_history_200 | nova-lite | color-locks | 78 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 7 | minimal_history_200 | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 9 | minimal_history_200 | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_history_200 | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-context-comparison-run-005 | 2 | minimal_history_200 | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_history_200 | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 5 | minimal_history_200 | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 5 | minimal_history_200 | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 6 | minimal_history_200 | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-context-comparison-run-005 | 8 | minimal_history_200 | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_history_200 | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 1 | minimal_history_200 | nova-lite | vault-combination | 106 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_history_200 | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 5 | minimal_history_200 | nova-lite | vault-combination | 157 | `context_overflow` | ventana de historial agotada |
| m3-context-comparison-run-005 | 6 | minimal_history_200 | nova-lite | vault-combination | 74 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 7 | minimal_history_200 | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 8 | minimal_history_200 | nova-lite | vault-combination | 68 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 1 | minimal_history_200 | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 7 | minimal_history_200 | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 9 | minimal_history_200 | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 2 | minimal_compaction | nova-lite | color-locks | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 4 | minimal_compaction | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-context-comparison-run-005 | 6 | minimal_compaction | nova-lite | color-locks | 60 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 7 | minimal_compaction | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 9 | minimal_compaction | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 2 | minimal_compaction | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 1 | minimal_compaction | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_compaction | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 4 | minimal_compaction | nova-lite | library-search | 7 | `planning_failure` | exploró 7 pasos sin alcanzar el objetivo |
| m3-context-comparison-run-005 | 7 | minimal_compaction | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 8 | minimal_compaction | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_compaction | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-context-comparison-run-005 | 1 | minimal_compaction | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 5 | minimal_compaction | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 8 | minimal_compaction | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_compaction | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_compaction | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 1 | minimal_compaction | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 2 | minimal_compaction | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_compaction | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 6 | minimal_compaction | nova-lite | vault-combination | 66 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 8 | minimal_compaction | nova-lite | vault-combination | 129 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 9 | minimal_compaction | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_compaction | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 2 | minimal_compaction | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 7 | minimal_compaction | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 1 | minimal_summary | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_summary | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 7 | minimal_summary | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_summary | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 4 | minimal_summary | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 5 | minimal_summary | nova-lite | apartment-keys | 64 | `context_overflow` | ventana de historial agotada |
| m3-context-comparison-run-005 | 1 | minimal_summary | nova-lite | library-search | 52 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 6 | minimal_summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_summary | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 4 | minimal_summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 7 | minimal_summary | nova-lite | office-sequence | 444 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 8 | minimal_summary | nova-lite | office-sequence | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 9 | minimal_summary | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_summary | nova-lite | office-sequence | 75 | `context_overflow` | ventana de historial agotada |
| m3-context-comparison-run-005 | 2 | minimal_summary | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_summary | nova-lite | extreme-archive | 65 | `context_overflow` | ventana de historial agotada |
| m3-context-comparison-run-005 | 8 | minimal_summary | nova-lite | extreme-archive | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 1 | minimal_summary | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 2 | minimal_summary | nova-lite | vault-combination | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 3 | minimal_summary | nova-lite | vault-combination | 46 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 7 | minimal_summary | nova-lite | vault-combination | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 8 | minimal_summary | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 9 | minimal_summary | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 10 | minimal_summary | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 1 | minimal_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 2 | minimal_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 4 | minimal_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 5 | minimal_summary | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-context-comparison-run-005 | 8 | minimal_summary | nova-lite | backtracking-vault | 142 | `max_iterations` | presupuesto de pasos agotado |
