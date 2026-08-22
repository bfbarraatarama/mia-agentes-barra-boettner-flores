# Análisis de errores — M3

**Runs:** `m3-nova-tool-repair-comparison-run-003`, `m3-planner-run-001`

| | |
|---|---|
| Total trials | 240 |
| Exitosos | 175 (72.9%) |
| Fallidos | 65 (27.1%) |
| Cobertura | 65/65 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 54 | 83% |
| `planning_failure` | 9 | 14% |
| `context_overflow` | 2 | 3% |

## Por sistema

### minimal / nova-lite (15 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 13 |
| `context_overflow` | 2 |

### minimal_tool_repair / nova-lite (27 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 23 |
| `planning_failure` | 4 |

### planner / nova-lite (23 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 18 |
| `planning_failure` | 5 |

## Por modelo

### nova-lite (65 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 54 |
| `planning_failure` | 9 |
| `context_overflow` | 2 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 13 | `max_iterations`: 13 |
| library-search | hard | 11 | `max_iterations`: 10, `planning_failure`: 1 |
| office-sequence | hard | 6 | `max_iterations`: 4, `planning_failure`: 2 |
| vault-combination | extreme | 21 | `max_iterations`: 18, `context_overflow`: 2, `planning_failure`: 1 |
| backtracking-vault | extreme | 9 | `max_iterations`: 5, `planning_failure`: 4 |
| apartment-keys | medium | 2 | `max_iterations`: 2 |
| extreme-archive | extreme | 3 | `max_iterations`: 2, `planning_failure`: 1 |

## Ejemplos por modo

### `max_iterations`

**minimal / nova-lite / color-locks / trial 3** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**minimal / nova-lite / color-locks / trial 4** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `context_overflow`

**minimal / nova-lite / vault-combination / trial 1** (70 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

**minimal / nova-lite / vault-combination / trial 9** (68 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

### `planning_failure`

**minimal_tool_repair / nova-lite / office-sequence / trial 4** (18 pasos)
- Razón: exploró 18 pasos sin alcanzar el objetivo
- Respuesta: *- The generated text has been blocked by our content filters.*

**minimal_tool_repair / nova-lite / office-sequence / trial 5** (13 pasos)
- Razón: exploró 13 pasos sin alcanzar el objetivo
- Respuesta: *<thinking>Parece que la caja fuerte no está visible en la descripción. Debo preguntar al usuario si hay algo que no estoy viendo o si hay otra forma de encontrar la caja fuerte.</thinking>*

## Todos los fallos clasificados

| Run | Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---:|---|---|---|---:|---|---|
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
| m3-planner-run-001 | 4 | planner | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 5 | planner | nova-lite | color-locks | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 6 | planner | nova-lite | color-locks | 43 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 5 | planner | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 2 | planner | nova-lite | library-search | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| m3-planner-run-001 | 3 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 5 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 6 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 8 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 9 | planner | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 4 | planner | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 2 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 5 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 6 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 7 | planner | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 8 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 9 | planner | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 10 | planner | nova-lite | vault-combination | 45 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 4 | planner | nova-lite | backtracking-vault | 46 | `planning_failure` | exploró 46 pasos sin alcanzar el objetivo |
| m3-planner-run-001 | 6 | planner | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| m3-planner-run-001 | 7 | planner | nova-lite | backtracking-vault | 29 | `planning_failure` | exploró 29 pasos sin alcanzar el objetivo |
| m3-planner-run-001 | 8 | planner | nova-lite | backtracking-vault | 18 | `planning_failure` | exploró 18 pasos sin alcanzar el objetivo |
| m3-planner-run-001 | 9 | planner | nova-lite | backtracking-vault | 21 | `planning_failure` | exploró 21 pasos sin alcanzar el objetivo |
