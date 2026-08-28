# Análisis de errores — M3

**Run:** `m3-final-run-008`

| | |
|---|---|
| Total trials | 480 |
| Exitosos | 333 (69.4%) |
| Fallidos | 147 (30.6%) |
| Cobertura | 147/147 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 127 | 86% |
| `gave_up_early` | 17 | 12% |
| `planning_failure` | 3 | 2% |

## Por sistema

### planner / nova-lite (54 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 48 |
| `gave_up_early` | 5 |
| `planning_failure` | 1 |

### baseline_incremental / nova-lite (47 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 43 |
| `gave_up_early` | 3 |
| `planning_failure` | 1 |

### planner_incremental / nova-lite (46 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 36 |
| `gave_up_early` | 9 |
| `planning_failure` | 1 |

## Por modelo

### nova-lite (147 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 127 |
| `gave_up_early` | 17 |
| `planning_failure` | 3 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 23 | `max_iterations`: 19, `gave_up_early`: 3, `planning_failure`: 1 |
| apartment-keys | medium | 6 | `max_iterations`: 6 |
| library-search | hard | 26 | `max_iterations`: 14, `gave_up_early`: 10, `planning_failure`: 2 |
| office-sequence | hard | 13 | `max_iterations`: 13 |
| vault-combination | extreme | 41 | `max_iterations`: 41 |
| backtracking-vault | extreme | 30 | `max_iterations`: 28, `gave_up_early`: 2 |
| extreme-archive | extreme | 7 | `max_iterations`: 6, `gave_up_early`: 1 |
| study-with-key | easy | 1 | `gave_up_early`: 1 |

## Ejemplos por modo

### `max_iterations`

**planner / nova-lite / color-locks / trial 5** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**planner / nova-lite / color-locks / trial 6** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `gave_up_early`

**planner / nova-lite / color-locks / trial 12** (2 pasos)
- Razón: terminó voluntariamente en 2 pasos
- Respuesta: *<thinking>La llave plateada no funcionó para abrir la cerradura dorada. Debo buscar otras formas de abrir la cerradura dorada, como herramientas o combinaciones. Sin embargo, no tengo ninguna herramie*

**planner / nova-lite / library-search / trial 2** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *<thinking>Parece que no hay una salida evidente en la sala. Debo considerar si hay otra forma de salir, como buscar una salida secreta o preguntar al archivero si está disponible.</thinking>*

### `planning_failure`

**planner / nova-lite / library-search / trial 5** (7 pasos)
- Razón: exploró 7 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>El libro de genealogía no parece contener ninguna pista útil para abrir la puerta o la caja fuerte. Hasta ahora, no he encontrado ninguna pista que pueda ayudarme a abrir la puerta o la caja*

**baseline_incremental / nova-lite / library-search / trial 20** (8 pasos)
- Razón: exploró 8 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>He inspeccionado todos los objetos y libros en la sala, y no he encontrado ninguna pista útil que pueda ayudar a abrir la caja fuerte o la puerta principal. No tengo más información ni herra*

## Todos los fallos clasificados

| Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---|---|---|---:|---|---|
| 5 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 12 | planner | nova-lite | color-locks | 2 | `gave_up_early` | terminó voluntariamente en 2 pasos |
| 15 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 16 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 17 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 18 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 14 | planner | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 15 | planner | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | planner | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | planner | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 5 | planner | nova-lite | library-search | 7 | `planning_failure` | exploró 7 pasos sin alcanzar el objetivo |
| 6 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 11 | planner | nova-lite | library-search | 3 | `gave_up_early` | terminó voluntariamente en 3 pasos |
| 13 | planner | nova-lite | library-search | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| 15 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | planner | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 2 | planner | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 13 | planner | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 16 | planner | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 11 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 12 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 13 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 14 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 16 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 17 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 18 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 11 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 13 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 14 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 15 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 16 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 17 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 18 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | baseline_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | baseline_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | baseline_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | baseline_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 14 | baseline_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 18 | baseline_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | baseline_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | baseline_incremental | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | baseline_incremental | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 3 | baseline_incremental | nova-lite | library-search | 50 | `max_iterations` | presupuesto de pasos agotado |
| 6 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | baseline_incremental | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 12 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 13 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 18 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | baseline_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | baseline_incremental | nova-lite | library-search | 8 | `planning_failure` | exploró 8 pasos sin alcanzar el objetivo |
| 1 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 17 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | baseline_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | baseline_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 14 | baseline_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | baseline_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | baseline_incremental | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| 4 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | baseline_incremental | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| 8 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 11 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 13 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 16 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | baseline_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | baseline_incremental | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 4 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 13 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 18 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | baseline_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_incremental | nova-lite | study-with-key | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 3 | planner_incremental | nova-lite | color-locks | 5 | `planning_failure` | exploró 5 pasos sin alcanzar el objetivo |
| 5 | planner_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_incremental | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 9 | planner_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner_incremental | nova-lite | color-locks | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| 14 | planner_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 18 | planner_incremental | nova-lite | color-locks | 45 | `max_iterations` | presupuesto de pasos agotado |
| 20 | planner_incremental | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 12 | planner_incremental | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_incremental | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 11 | planner_incremental | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 12 | planner_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 14 | planner_incremental | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 18 | planner_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | planner_incremental | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | planner_incremental | nova-lite | library-search | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| 12 | planner_incremental | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_incremental | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 16 | planner_incremental | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 13 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 14 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 15 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 16 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 18 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 19 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 20 | planner_incremental | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 12 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 13 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 14 | planner_incremental | nova-lite | backtracking-vault | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 17 | planner_incremental | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
