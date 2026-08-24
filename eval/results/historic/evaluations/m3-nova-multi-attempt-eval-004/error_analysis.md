# Análisis de errores — M3

**Run:** `m3-nova-multi-attempt-run-004`

| | |
|---|---|
| Total trials | 160 |
| Exitosos | 111 (69.4%) |
| Fallidos | 49 (30.6%) |
| Cobertura | 49/49 trials fallidos clasificados |

## Modos de fallo

| Modo | Trials | % |
|---|---:|---:|
| `max_iterations` | 43 | 88% |
| `gave_up_early` | 3 | 6% |
| `context_overflow` | 3 | 6% |

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

## Por modelo

### nova-lite (49 fallos)

| Modo | Trials |
|---|---:|
| `max_iterations` | 43 |
| `gave_up_early` | 3 |
| `context_overflow` | 3 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| color-locks | medium | 6 | `max_iterations`: 5, `gave_up_early`: 1 |
| apartment-keys | medium | 2 | `max_iterations`: 2 |
| library-search | hard | 13 | `max_iterations`: 13 |
| office-sequence | hard | 5 | `max_iterations`: 3, `gave_up_early`: 2 |
| extreme-archive | extreme | 3 | `max_iterations`: 3 |
| vault-combination | extreme | 10 | `max_iterations`: 7, `context_overflow`: 3 |
| backtracking-vault | extreme | 10 | `max_iterations`: 10 |

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

## Todos los fallos clasificados

| Trial | Configuración de agente | Modelo | Escenario | Pasos | Modo | Razón |
|---|---|---|---|---:|---|---|
| 4 | minimal | nova-lite | color-locks | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 10 | minimal | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | minimal | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | minimal | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | minimal | nova-lite | office-sequence | 1 | `gave_up_early` | terminó voluntariamente en 1 pasos |
| 3 | minimal | nova-lite | office-sequence | 0 | `gave_up_early` | terminó voluntariamente en 0 pasos |
| 5 | minimal | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 9 | minimal | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | minimal | nova-lite | vault-combination | 64 | `context_overflow` | ventana de historial agotada |
| 4 | minimal | nova-lite | vault-combination | 43 | `max_iterations` | presupuesto de pasos agotado |
| 5 | minimal | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | minimal | nova-lite | vault-combination | 50 | `max_iterations` | presupuesto de pasos agotado |
| 9 | minimal | nova-lite | vault-combination | 70 | `context_overflow` | ventana de historial agotada |
| 10 | minimal | nova-lite | vault-combination | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | minimal | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | minimal_tool_repair | nova-lite | color-locks | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | minimal_tool_repair | nova-lite | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 7 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | minimal_tool_repair | nova-lite | library-search | 40 | `max_iterations` | presupuesto de pasos agotado |
| 2 | minimal_tool_repair | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 3 | minimal_tool_repair | nova-lite | office-sequence | 46 | `max_iterations` | presupuesto de pasos agotado |
| 5 | minimal_tool_repair | nova-lite | office-sequence | 40 | `max_iterations` | presupuesto de pasos agotado |
| 10 | minimal_tool_repair | nova-lite | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | minimal_tool_repair | nova-lite | vault-combination | 47 | `max_iterations` | presupuesto de pasos agotado |
| 7 | minimal_tool_repair | nova-lite | vault-combination | 61 | `context_overflow` | ventana de historial agotada |
| 9 | minimal_tool_repair | nova-lite | vault-combination | 41 | `max_iterations` | presupuesto de pasos agotado |
| 10 | minimal_tool_repair | nova-lite | vault-combination | 42 | `max_iterations` | presupuesto de pasos agotado |
| 3 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 5 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 6 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
| 8 | minimal_tool_repair | nova-lite | backtracking-vault | 40 | `max_iterations` | presupuesto de pasos agotado |
