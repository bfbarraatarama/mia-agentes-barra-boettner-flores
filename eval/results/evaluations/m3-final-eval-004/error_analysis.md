# Análisis de errores — M3

**Run:** `m3-final-run-004`

| | |
|---|---|
| Total trials | 160 |
| Exitosos | 96 (60.0%) |
| Fallidos | 64 (40.0%) |
| Cobertura | 64/64 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 55 | 86% |
| `gave_up_early` | 8 | 12% |
| `planning_failure` | 1 | 2% |

## Por sistema

### summary_incremental_token_trigger / nova-lite (27 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 26 |
| `planning_failure` | 1 |

### planner_summary_incremental_token_trigger / nova-lite (37 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 29 |
| `gave_up_early` | 8 |

## Por modelo

### nova-lite (64 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 55 |
| `gave_up_early` | 8 |
| `planning_failure` | 1 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| study-with-key | easy | 1 | `max_iterations`: 1 |
| color-locks | medium | 8 | `max_iterations`: 7, `planning_failure`: 1 |
| apartment-keys | medium | 3 | `max_iterations`: 3 |
| library-search | hard | 6 | `max_iterations`: 3, `gave_up_early`: 3 |
| office-sequence | hard | 4 | `max_iterations`: 2, `gave_up_early`: 2 |
| extreme-archive | extreme | 18 | `max_iterations`: 16, `gave_up_early`: 2 |
| vault-combination | extreme | 15 | `max_iterations`: 15 |
| backtracking-vault | extreme | 9 | `max_iterations`: 8, `gave_up_early`: 1 |

## Ejemplos por modo

### `max_iterations`

**summary_incremental_token_trigger / nova-lite / study-with-key / trial 6** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**summary_incremental_token_trigger / nova-lite / color-locks / trial 6** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `planning_failure`

**summary_incremental_token_trigger / nova-lite / color-locks / trial 9** (6 pasos)
- Razón: exploró 6 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>El cofre azul no tiene cerradura y contiene un trapo viejo, que no parece ser útil para abrir la puerta principal. Debemos revisar nuevamente la llave plateada y los cofres para encontrar la*

### `gave_up_early`

**planner_summary_incremental_token_trigger / nova-lite / library-search / trial 2** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *No se pudo generar el plan inicial: structured_call falló tras 3 intentos: El modelo respondió con texto libre en lugar de invocar final_result.*

**planner_summary_incremental_token_trigger / nova-lite / library-search / trial 3** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *No se pudo generar el plan inicial: structured_call falló tras 3 intentos: El modelo respondió con texto libre en lugar de invocar final_result.*

## Todos los fallos clasificados

| Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---|---|---|---:|---|---|
| 6 | summary_incremental_token_trigger | nova-lite | study-with-key | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | summary_incremental_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary_incremental_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | summary_incremental_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary_incremental_token_trigger | nova-lite | color-locks | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| 1 | summary_incremental_token_trigger | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | summary_incremental_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary_incremental_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | summary_incremental_token_trigger | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary_incremental_token_trigger | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | summary_incremental_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary_incremental_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner_summary_incremental_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary_incremental_token_trigger | nova-lite | color-locks | 0 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_summary_incremental_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary_incremental_token_trigger | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_summary_incremental_token_trigger | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary_incremental_token_trigger | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner_summary_incremental_token_trigger | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 3 | planner_summary_incremental_token_trigger | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 4 | planner_summary_incremental_token_trigger | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary_incremental_token_trigger | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 1 | planner_summary_incremental_token_trigger | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 9 | planner_summary_incremental_token_trigger | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 1 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 7 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 10 | planner_summary_incremental_token_trigger | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner_summary_incremental_token_trigger | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner_summary_incremental_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary_incremental_token_trigger | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 4 | planner_summary_incremental_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary_incremental_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary_incremental_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_summary_incremental_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner_summary_incremental_token_trigger | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
