# Análisis de errores — M3

**Run:** `m3-final-run-005`

| | |
|---|---|
| Total trials | 160 |
| Exitosos | 90 (56.2%) |
| Fallidos | 70 (43.8%) |
| Cobertura | 70/70 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 64 | 91% |
| `gave_up_early` | 6 | 9% |

## Por sistema

### summary_incremental_strategic / nova-lite (35 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 30 |
| `gave_up_early` | 5 |

### planner_summary_incremental_strategic / nova-lite (35 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 34 |
| `gave_up_early` | 1 |

## Por modelo

### nova-lite (70 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 64 |
| `gave_up_early` | 6 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| library-search | hard | 5 | `max_iterations`: 3, `gave_up_early`: 2 |
| office-sequence | hard | 8 | `max_iterations`: 6, `gave_up_early`: 2 |
| extreme-archive | extreme | 19 | `max_iterations`: 18, `gave_up_early`: 1 |
| vault-combination | extreme | 20 | `max_iterations`: 20 |
| backtracking-vault | extreme | 17 | `max_iterations`: 16, `gave_up_early`: 1 |
| color-locks | medium | 1 | `max_iterations`: 1 |

## Ejemplos por modo

### `gave_up_early`

**summary_incremental_strategic / nova-lite / library-search / trial 2** (1 pasos)
- Razón: terminó voluntariamente en 1 pasos
- Respuesta: *<thinking>La sala ha sido examinada nuevamente y no contiene ninguna pista útil para abrir la puerta principal. No tengo ninguna otra idea de cómo abrir la puerta principal. Podría preguntar al usuari*

**summary_incremental_strategic / nova-lite / office-sequence / trial 5** (0 pasos)
- Razón: terminó voluntariamente en 0 pasos
- Respuesta: *<thinking>Parece que todavía estoy en el archivo y la única salida disponible es hacia el sur. Debo haberme movido en la dirección incorrecta al intentar salir. Revisaré las acciones anteriores para e*

### `max_iterations`

**summary_incremental_strategic / nova-lite / library-search / trial 3** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**summary_incremental_strategic / nova-lite / library-search / trial 7** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

## Todos los fallos clasificados

| Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---|---|---|---:|---|---|
| 2 | summary_incremental_strategic | nova-lite | library-search | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| 3 | summary_incremental_strategic | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary_incremental_strategic | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | summary_incremental_strategic | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | summary_incremental_strategic | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | summary_incremental_strategic | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 8 | summary_incremental_strategic | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | summary_incremental_strategic | nova-lite | office-sequence | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| 1 | summary_incremental_strategic | nova-lite | extreme-archive | 41 | `max_iterations` | presupuesto de pasos agotado |
| 3 | summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary_incremental_strategic | nova-lite | extreme-archive | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 10 | summary_incremental_strategic | nova-lite | extreme-archive | 59 | `max_iterations` | presupuesto de pasos agotado |
| 1 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | summary_incremental_strategic | nova-lite | vault-combination | 44 | `max_iterations` | presupuesto de pasos agotado |
| 4 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | summary_incremental_strategic | nova-lite | backtracking-vault | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| 4 | summary_incremental_strategic | nova-lite | backtracking-vault | 44 | `max_iterations` | presupuesto de pasos agotado |
| 5 | summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary_incremental_strategic | nova-lite | color-locks | 44 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary_incremental_strategic | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_summary_incremental_strategic | nova-lite | library-search | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 3 | planner_summary_incremental_strategic | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary_incremental_strategic | nova-lite | office-sequence | 42 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_summary_incremental_strategic | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner_summary_incremental_strategic | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner_summary_incremental_strategic | nova-lite | vault-combination | 48 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner_summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary_incremental_strategic | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary_incremental_strategic | nova-lite | vault-combination | 60 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | planner_summary_incremental_strategic | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 43 | `max_iterations` | presupuesto de pasos agotado |
| 9 | planner_summary_incremental_strategic | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
