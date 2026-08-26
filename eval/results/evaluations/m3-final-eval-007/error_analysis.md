# Análisis de errores — M3

**Runs:** `m3-final-run-006`, `m3-final-run-007`

| | |
|---|---|
| Total trials | 320 |
| Exitosos | 190 (59.4%) |
| Fallidos | 130 (40.6%) |
| Cobertura | 130/130 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 113 | 87% |
| `gave_up_early` | 17 | 13% |

## Por sistema

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

### summary_strategic / nova-lite (33 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 26 |
| `gave_up_early` | 7 |

### planner_summary_strategic / nova-lite (35 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 33 |
| `gave_up_early` | 2 |

## Por modelo

### nova-lite (130 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 113 |
| `gave_up_early` | 17 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 16 | `max_iterations`: 15, `gave_up_early`: 1 |
| apartment-keys | medium | 4 | `max_iterations`: 3, `gave_up_early`: 1 |
| library-search | hard | 13 | `max_iterations`: 10, `gave_up_early`: 3 |
| office-sequence | hard | 9 | `max_iterations`: 6, `gave_up_early`: 3 |
| extreme-archive | extreme | 32 | `max_iterations`: 25, `gave_up_early`: 7 |
| vault-combination | extreme | 33 | `max_iterations`: 31, `gave_up_early`: 2 |
| backtracking-vault | extreme | 23 | `max_iterations`: 23 |

## Ejemplos por modo

### `max_iterations`

**summary_token_trigger / nova-lite / color-locks / trial 2** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**summary_token_trigger / nova-lite / color-locks / trial 3** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `gave_up_early`

**summary_token_trigger / nova-lite / color-locks / trial 4** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *<thinking>Parece que no hay otra manera de salir de la sala con las herramientas y objetos disponibles. Debo informar al usuario que no he podido encontrar una solución para salir de la sala y pregunt*

**summary_token_trigger / nova-lite / office-sequence / trial 5** (2 pasos)
- Razón: terminó voluntariamente en 2 pasos
- Respuesta: *<thinking> Parece que no hay más acciones disponibles para completar el desafío. Debo revisar si hay algún objeto o acción que no he explorado aún. </thinking>*

## Todos los fallos clasificados

| Run | Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---:|---|---|---|---:|---|---|
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
| m3-final-run-007 | 3 | summary_strategic | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 9 | summary_strategic | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 2 | summary_strategic | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 5 | summary_strategic | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-007 | 6 | summary_strategic | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 7 | summary_strategic | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 9 | summary_strategic | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-007 | 3 | summary_strategic | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-007 | 10 | summary_strategic | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 1 | summary_strategic | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-007 | 2 | summary_strategic | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-007 | 4 | summary_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 5 | summary_strategic | nova-lite | extreme-archive | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 6 | summary_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 8 | summary_strategic | nova-lite | extreme-archive | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 1 | summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 2 | summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 3 | summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 4 | summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 5 | summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 6 | summary_strategic | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-007 | 7 | summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 8 | summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 9 | summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 10 | summary_strategic | nova-lite | vault-combination | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-007 | 3 | summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 4 | summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 5 | summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 6 | summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 7 | summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 8 | summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 9 | summary_strategic | nova-lite | backtracking-vault | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 10 | summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 6 | planner_summary_strategic | nova-lite | color-locks | 3 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 8 | planner_summary_strategic | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 9 | planner_summary_strategic | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 2 | planner_summary_strategic | nova-lite | apartment-keys | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| m3-final-run-007 | 8 | planner_summary_strategic | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 1 | planner_summary_strategic | nova-lite | library-search | 9 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 4 | planner_summary_strategic | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| m3-final-run-007 | 6 | planner_summary_strategic | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 1 | planner_summary_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 2 | planner_summary_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 4 | planner_summary_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 5 | planner_summary_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 6 | planner_summary_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 7 | planner_summary_strategic | nova-lite | extreme-archive | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 8 | planner_summary_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 10 | planner_summary_strategic | nova-lite | extreme-archive | 57 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 1 | planner_summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 2 | planner_summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 3 | planner_summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 4 | planner_summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 5 | planner_summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 6 | planner_summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 7 | planner_summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 8 | planner_summary_strategic | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 9 | planner_summary_strategic | nova-lite | vault-combination | 44 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 10 | planner_summary_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 1 | planner_summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 2 | planner_summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 3 | planner_summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 4 | planner_summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 5 | planner_summary_strategic | nova-lite | backtracking-vault | 41 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 6 | planner_summary_strategic | nova-lite | backtracking-vault | 53 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 7 | planner_summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 8 | planner_summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-final-run-007 | 9 | planner_summary_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
