# Análisis de presión de contexto — M3

**Runs:** `m3-nova-multi-attempt-run-004`, `m3-context-comparison-run-005`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 400 |
| Attempts | 475 |
| Trials terminados por presupuesto | 7 |
| Attempts terminados por presupuesto | 7 |
| Terminaciones por attempt_index | {1: 7} |
| Iteraciones al morir (min/media/max) | 21 / 32.71 / 38 |
| Tool calls por iteración | {0: 327, 1: 9652, 2: 347, 3: 140, 4: 84, 5: 30, 6: 4, 7: 24, 8: 6, 10: 1, 11: 1, 12: 1, 14: 28, 20: 2} |
| Máximo de mensajes enviados | 194 |
| Llamadas con la ventana llena | 3 |
| Acciones ejecutadas | 11935 |
| Acciones repetidas (intra-trial) | 4910 (41.14%) |
| Trials con repetición | 216 |
| Acciones re-derivadas entre attempts | 64 de 150 (42.67%) |
| Tokens entrada / salida | 40556283 / 699909 |
| Compactaciones (eventos / fallas) | 21 / 4 |
| Tokens del compactor (in / out) | 33708 / 13364 |

## Por sistema

### `minimal` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 108 |
| Trials terminados por presupuesto | 2 |
| Attempts terminados por presupuesto | 2 |
| Terminaciones por attempt_index | {1: 2} |
| Iteraciones al morir (min/media/max) | 29 / 32.0 / 35 |
| Tool calls por iteración | {0: 78, 1: 1948, 2: 80, 3: 20, 4: 12, 5: 3, 6: 2, 8: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 1 |
| Acciones ejecutadas | 2248 |
| Acciones repetidas (intra-trial) | 853 (37.94%) |
| Trials con repetición | 49 |
| Acciones re-derivadas entre attempts | 15 de 50 (30.00%) |
| Tokens entrada / salida | 8075582 / 134575 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `minimal_tool_repair` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 80 |
| Trials terminados por presupuesto | 1 |
| Attempts terminados por presupuesto | 1 |
| Terminaciones por attempt_index | {1: 1} |
| Iteraciones al morir (min/media/max) | 38 / 38.0 / 38 |
| Tool calls por iteración | {0: 50, 1: 2007, 2: 45, 3: 23, 4: 6, 5: 1} |
| Máximo de mensajes enviados | 99 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 2192 |
| Acciones repetidas (intra-trial) | 761 (34.72%) |
| Trials con repetición | 43 |
| Acciones re-derivadas entre attempts | 0 de 0 (n/a) |
| Tokens entrada / salida | 8187709 / 131965 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `minimal_history_200` / `nova-lite` (ventana: 200)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 100 |
| Trials terminados por presupuesto | 1 |
| Attempts terminados por presupuesto | 1 |
| Terminaciones por attempt_index | {1: 1} |
| Iteraciones al morir (min/media/max) | 37 / 37.0 / 37 |
| Tool calls por iteración | {0: 74, 1: 1793, 2: 87, 3: 64, 4: 8, 6: 1, 7: 21} |
| Máximo de mensajes enviados | 194 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 2337 |
| Acciones repetidas (intra-trial) | 982 (42.02%) |
| Trials con repetición | 36 |
| Acciones re-derivadas entre attempts | 1 de 38 (2.63%) |
| Tokens entrada / salida | 7842864 / 133651 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `minimal_compaction` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 107 |
| Trials terminados por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 78, 1: 2020, 2: 45, 3: 20, 4: 17, 5: 12, 7: 1, 8: 1, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 2 |
| Acciones ejecutadas | 2333 |
| Acciones repetidas (intra-trial) | 871 (37.33%) |
| Trials con repetición | 44 |
| Acciones re-derivadas entre attempts | 48 de 62 (77.42%) |
| Tokens entrada / salida | 8517622 / 148801 |
| Compactaciones (eventos / fallas) | 8 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `minimal_summary` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 80 |
| Trials terminados por presupuesto | 3 |
| Attempts terminados por presupuesto | 3 |
| Terminaciones por attempt_index | {1: 3} |
| Iteraciones al morir (min/media/max) | 21 / 30.0 / 35 |
| Tool calls por iteración | {0: 47, 1: 1884, 2: 90, 3: 13, 4: 41, 5: 14, 6: 1, 7: 2, 8: 4, 10: 1, 11: 1, 12: 1, 14: 28, 20: 1} |
| Máximo de mensajes enviados | 99 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 2825 |
| Acciones repetidas (intra-trial) | 1443 (51.08%) |
| Trials con repetición | 44 |
| Acciones re-derivadas entre attempts | 0 de 0 (n/a) |
| Tokens entrada / salida | 7932506 / 150917 |
| Compactaciones (eventos / fallas) | 13 / 4 |
| Tokens del compactor (in / out) | 33708 / 13364 |
