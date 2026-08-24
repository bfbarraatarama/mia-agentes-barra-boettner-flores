# Análisis de errores — M3

**Run:** `m3-baseline-run-001`

| | |
|---|---|
| Total trials | 80 |
| Exitosos | 12 (15%) |
| Fallidos | 68 (85%) |
| Cobertura | 68/68 trials fallidos clasificados |

## Modos de fallo

| Modo | Runs | % |
|---|---:|---:|
| `planning_failure` | 30 | 44% |
| `hallucination` | 14 | 21% |
| `wrong_tool_use` | 13 | 19% |
| `context_overflow` | 6 | 9% |
| `max_iterations` | 2 | 3% |
| `navigation_error` | 2 | 3% |
| `gave_up_early` | 1 | 1% |

## Por modelo

### llama3.1 (37 fallos)

| Modo | Runs |
|---|---:|
| `hallucination` | 13 |
| `wrong_tool_use` | 12 |
| `context_overflow` | 6 |
| `planning_failure` | 5 |
| `max_iterations` | 1 |

### qwen2.5:7b (31 fallos)

| Modo | Runs |
|---|---:|
| `planning_failure` | 25 |
| `navigation_error` | 2 |
| `hallucination` | 1 |
| `max_iterations` | 1 |
| `wrong_tool_use` | 1 |
| `gave_up_early` | 1 |

## Por escenario

| Escenario | Dificultad | Fallos | Distribución |
|---|---|---:|---|
| study-with-key | easy | 5 | `hallucination`: 3, `wrong_tool_use`: 2 |
| color-locks | medium | 8 | `wrong_tool_use`: 2, `context_overflow`: 2, `hallucination`: 2, `planning_failure`: 2 |
| apartment-keys | medium | 6 | `planning_failure`: 4, `hallucination`: 1, `max_iterations`: 1 |
| library-search | hard | 10 | `planning_failure`: 8, `hallucination`: 1, `wrong_tool_use`: 1 |
| office-sequence | hard | 10 | `planning_failure`: 5, `context_overflow`: 4, `hallucination`: 1 |
| extreme-archive | extreme | 9 | `hallucination`: 4, `planning_failure`: 4, `max_iterations`: 1 |
| vault-combination | extreme | 10 | `wrong_tool_use`: 4, `planning_failure`: 4, `hallucination`: 1, `gave_up_early`: 1 |
| backtracking-vault | extreme | 10 | `wrong_tool_use`: 4, `planning_failure`: 3, `navigation_error`: 2, `hallucination`: 1 |

## Ejemplos por modo

### `wrong_tool_use`

**llama3.1 / study-with-key / trial 1** (2 pasos)
- Razón: _make_examine.<locals>.examine_impl() got an unexpected keyword argument 'obj'
- Respuesta: *La puerta principal está cerrada. No hay ninguna marca o señal que indique cómo abrir la puerta. Ves:   - alfombra [id: alfombra]   - escritorio [id: escritorio]   - puerta principal [id: puerta_princ*

**llama3.1 / study-with-key / trial 2** (2 pasos)
- Razón: _make_examine.<locals>.examine_impl() got an unexpected keyword argument 'obj'
- Respuesta: *La puerta principal está cerrada. Hay un candado en la parte inferior de la puerta. Ves:   - alfombra [id: alfombra]   - escritorio [id: escritorio]   - puerta principal [id: puerta_principal] (cerrad*

### `hallucination`

**llama3.1 / study-with-key / trial 3** (3 pasos)
- Razón: narró tool calls como texto en vez de ejecutarlas
- Respuesta: *{"name": "search", "parameters": {"target":"escritorio"}}*

**llama3.1 / study-with-key / trial 4** (4 pasos)
- Razón: narró tool calls como texto en vez de ejecutarlas
- Respuesta: *No puedes tomar la alfombra porque está en el suelo y no hay un lugar donde colocarla.  {"name": "examine", "parameters": {"target":"puerta_principal"}}*

### `context_overflow`

**llama3.1 / color-locks / trial 2** (66 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

**llama3.1 / color-locks / trial 3** (66 pasos)
- Razón: ventana de historial agotada
- Respuesta: *Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages=100.*

### `planning_failure`

**llama3.1 / apartment-keys / trial 2** (23 pasos)
- Razón: exploró 23 pasos sin alcanzar el objetivo
- Respuesta: *La llave estaba en la puerta principal. La usaste para abrir la puerta y salir del apartamento.*

**llama3.1 / library-search / trial 1** (6 pasos)
- Razón: exploró 6 pasos sin alcanzar el objetivo
- Respuesta: *Al examinar el escritorio, encuentro un papel con una nota que dice: "La respuesta está en los libros". También hay un pequeño compartimiento secreto en la mesa donde se encuentra un llavero con ocho*

### `max_iterations`

**llama3.1 / extreme-archive / trial 3** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

**qwen2.5:7b / apartment-keys / trial 5** (40 pasos)
- Razón: presupuesto de pasos agotado
- Respuesta: *Se alcanzó el límite de 40 iteraciones sin obtener una respuesta final.*

### `gave_up_early`

**qwen2.5:7b / vault-combination / trial 3** (2 pasos)
- Razón: terminó voluntariamente en 2 pasos
- Respuesta: *Ahora estás en la Galería central. Parece un lugar amplio con varios pasillos que se extienden en diferentes direcciones. No ves ningún núcleo aquí, pero hay una vitrina cerrada y una puerta al sur.*

### `navigation_error`

**qwen2.5:7b / backtracking-vault / trial 1** (10 pasos)
- Razón: no usó go en escenario multi-sala
- Respuesta: *Veo que aún no tenemos la llave oxidada en nuestro inventario. Vamos a intentar abrir el cofre nuevamente para ver si hay alguna manera de obtener la llave oxidada.  Primero, vamos a usar cualquier ob*

**qwen2.5:7b / backtracking-vault / trial 4** (27 pasos)
- Razón: no usó go en escenario multi-sala
- Respuesta: *Entiendo que no tenemos la llave oxidada en nuestro inventario. Vamos a intentar abrir el cofre antiguo directamente para ver si podemos encontrar la llave oxidada dentro.  Primero, vamos a intentar u*

## Todos los fallos clasificados

| Trial | Modelo | Escenario | Pasos | Modo | Razón |
|---|---|---|---:|---|---|
| 1 | llama3.1 | study-with-key | 2 | `wrong_tool_use` | _make_examine.<locals>.examine_impl() got an unexpected keyw |
| 2 | llama3.1 | study-with-key | 2 | `wrong_tool_use` | _make_examine.<locals>.examine_impl() got an unexpected keyw |
| 3 | llama3.1 | study-with-key | 3 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 4 | llama3.1 | study-with-key | 4 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 5 | llama3.1 | study-with-key | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 1 | llama3.1 | color-locks | 32 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| 2 | llama3.1 | color-locks | 66 | `context_overflow` | ventana de historial agotada |
| 3 | llama3.1 | color-locks | 66 | `context_overflow` | ventana de historial agotada |
| 4 | llama3.1 | color-locks | 20 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| 5 | llama3.1 | color-locks | 11 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 2 | llama3.1 | apartment-keys | 23 | `planning_failure` | exploró 23 pasos sin alcanzar el objetivo |
| 3 | llama3.1 | apartment-keys | 23 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 1 | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| 2 | llama3.1 | library-search | 12 | `planning_failure` | exploró 12 pasos sin alcanzar el objetivo |
| 3 | llama3.1 | library-search | 6 | `planning_failure` | exploró 6 pasos sin alcanzar el objetivo |
| 4 | llama3.1 | library-search | 6 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 5 | llama3.1 | library-search | 5 | `planning_failure` | exploró 5 pasos sin alcanzar el objetivo |
| 1 | llama3.1 | office-sequence | 68 | `context_overflow` | ventana de historial agotada |
| 2 | llama3.1 | office-sequence | 68 | `context_overflow` | ventana de historial agotada |
| 3 | llama3.1 | office-sequence | 63 | `context_overflow` | ventana de historial agotada |
| 4 | llama3.1 | office-sequence | 56 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 5 | llama3.1 | office-sequence | 67 | `context_overflow` | ventana de historial agotada |
| 1 | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 2 | llama3.1 | extreme-archive | 2 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 3 | llama3.1 | extreme-archive | 40 | `max_iterations` | presupuesto de pasos agotado |
| 4 | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 5 | llama3.1 | extreme-archive | 1 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 1 | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| 2 | llama3.1 | vault-combination | 2 | `hallucination` | declaró éxito cuando el objetivo no estaba cumplido |
| 3 | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| 4 | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| 5 | llama3.1 | vault-combination | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| 1 | llama3.1 | backtracking-vault | 6 | `wrong_tool_use` | _make_go.<locals>.go_impl() got an unexpected keyword argume |
| 2 | llama3.1 | backtracking-vault | 3 | `wrong_tool_use` | _make_go.<locals>.go_impl() got an unexpected keyword argume |
| 3 | llama3.1 | backtracking-vault | 8 | `wrong_tool_use` | _make_go.<locals>.go_impl() got an unexpected keyword argume |
| 4 | llama3.1 | backtracking-vault | 9 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 5 | llama3.1 | backtracking-vault | 2 | `wrong_tool_use` | _make_take.<locals>.take_impl() got an unexpected keyword ar |
| 2 | qwen2.5:7b | color-locks | 23 | `hallucination` | narró tool calls como texto en vez de ejecutarlas |
| 3 | qwen2.5:7b | color-locks | 11 | `planning_failure` | exploró 11 pasos sin alcanzar el objetivo |
| 4 | qwen2.5:7b | color-locks | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| 1 | qwen2.5:7b | apartment-keys | 38 | `planning_failure` | exploró 38 pasos sin alcanzar el objetivo |
| 2 | qwen2.5:7b | apartment-keys | 28 | `planning_failure` | exploró 28 pasos sin alcanzar el objetivo |
| 3 | qwen2.5:7b | apartment-keys | 17 | `planning_failure` | exploró 17 pasos sin alcanzar el objetivo |
| 5 | qwen2.5:7b | apartment-keys | 40 | `max_iterations` | presupuesto de pasos agotado |
| 1 | qwen2.5:7b | library-search | 16 | `planning_failure` | exploró 16 pasos sin alcanzar el objetivo |
| 2 | qwen2.5:7b | library-search | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| 3 | qwen2.5:7b | library-search | 16 | `planning_failure` | exploró 16 pasos sin alcanzar el objetivo |
| 4 | qwen2.5:7b | library-search | 20 | `wrong_tool_use` | _make_look.<locals>.look_impl() got an unexpected keyword ar |
| 5 | qwen2.5:7b | library-search | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| 1 | qwen2.5:7b | office-sequence | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| 2 | qwen2.5:7b | office-sequence | 15 | `planning_failure` | exploró 15 pasos sin alcanzar el objetivo |
| 3 | qwen2.5:7b | office-sequence | 22 | `planning_failure` | exploró 22 pasos sin alcanzar el objetivo |
| 4 | qwen2.5:7b | office-sequence | 23 | `planning_failure` | exploró 23 pasos sin alcanzar el objetivo |
| 5 | qwen2.5:7b | office-sequence | 24 | `planning_failure` | exploró 24 pasos sin alcanzar el objetivo |
| 1 | qwen2.5:7b | extreme-archive | 5 | `planning_failure` | exploró 5 pasos sin alcanzar el objetivo |
| 2 | qwen2.5:7b | extreme-archive | 29 | `planning_failure` | exploró 29 pasos sin alcanzar el objetivo |
| 3 | qwen2.5:7b | extreme-archive | 18 | `planning_failure` | exploró 18 pasos sin alcanzar el objetivo |
| 5 | qwen2.5:7b | extreme-archive | 8 | `planning_failure` | exploró 8 pasos sin alcanzar el objetivo |
| 1 | qwen2.5:7b | vault-combination | 8 | `planning_failure` | exploró 8 pasos sin alcanzar el objetivo |
| 2 | qwen2.5:7b | vault-combination | 21 | `planning_failure` | exploró 21 pasos sin alcanzar el objetivo |
| 3 | qwen2.5:7b | vault-combination | 2 | `gave_up_early` | terminó voluntariamente en 2 pasos |
| 4 | qwen2.5:7b | vault-combination | 25 | `planning_failure` | exploró 25 pasos sin alcanzar el objetivo |
| 5 | qwen2.5:7b | vault-combination | 19 | `planning_failure` | exploró 19 pasos sin alcanzar el objetivo |
| 1 | qwen2.5:7b | backtracking-vault | 10 | `navigation_error` | no usó go en escenario multi-sala |
| 2 | qwen2.5:7b | backtracking-vault | 9 | `planning_failure` | exploró 9 pasos sin alcanzar el objetivo |
| 3 | qwen2.5:7b | backtracking-vault | 7 | `planning_failure` | exploró 7 pasos sin alcanzar el objetivo |
| 4 | qwen2.5:7b | backtracking-vault | 27 | `navigation_error` | no usó go en escenario multi-sala |
| 5 | qwen2.5:7b | backtracking-vault | 25 | `planning_failure` | exploró 25 pasos sin alcanzar el objetivo |
