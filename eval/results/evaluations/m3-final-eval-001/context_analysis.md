# Análisis de presión de contexto — M3

**Run:** `m3-final-run-001`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 320 |
| Attempts | 380 |
| Trials terminados por presupuesto | 72 |
| Attempts terminados por presupuesto | 72 |
| Terminaciones por attempt_index | {1: 72} |
| Iteraciones al morir (min/media/max) | 3 / 19.03 / 38 |
| Tool calls por iteración | {0: 219, 1: 7451, 2: 223, 3: 65, 4: 24, 5: 8, 6: 12, 7: 4, 8: 14, 9: 1, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 28 |
| Acciones ejecutadas | 8354 |
| Acciones repetidas (intra-trial) | 2687 (32.16%) |
| Trials con repetición | 172 |
| Acciones re-derivadas entre attempts | 191 de 378 (50.53%) |
| Tokens entrada / salida | 25898451 / 775662 |
| Compactaciones (eventos / fallas) | 518 / 88 |
| Tokens del compactor (in / out) | 1049724 / 240089 |

## Por sistema

### `baseline` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 99 |
| Trials terminados por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 71, 1: 1986, 2: 47, 3: 11, 4: 4, 5: 2, 7: 1, 8: 2} |
| Máximo de mensajes enviados | 99 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 2162 |
| Acciones repetidas (intra-trial) | 704 (32.56%) |
| Trials con repetición | 43 |
| Acciones re-derivadas entre attempts | 36 de 59 (61.02%) |
| Tokens entrada / salida | 7962054 / 132871 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `planner` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 100 |
| Trials terminados por presupuesto | 2 |
| Attempts terminados por presupuesto | 2 |
| Terminaciones por attempt_index | {1: 2} |
| Iteraciones al morir (min/media/max) | 19 / 25.0 / 31 |
| Tool calls por iteración | {0: 72, 1: 2043, 2: 46, 3: 27, 4: 7, 5: 4, 6: 12, 8: 9} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 1 |
| Acciones ejecutadas | 2394 |
| Acciones repetidas (intra-trial) | 941 (39.31%) |
| Trials con repetición | 45 |
| Acciones re-derivadas entre attempts | 85 de 103 (82.52%) |
| Tokens entrada / salida | 9133034 / 150728 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `summary` / `nova-lite` (ventana: 20)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 95 |
| Trials terminados por presupuesto | 34 |
| Attempts terminados por presupuesto | 34 |
| Terminaciones por attempt_index | {1: 34} |
| Iteraciones al morir (min/media/max) | 9 / 17.44 / 38 |
| Tool calls por iteración | {0: 42, 1: 1694, 2: 62, 3: 15, 4: 5, 5: 1, 7: 2} |
| Máximo de mensajes enviados | 20 |
| Llamadas con la ventana llena | 16 |
| Acciones ejecutadas | 1863 |
| Acciones repetidas (intra-trial) | 570 (30.60%) |
| Trials con repetición | 39 |
| Acciones re-derivadas entre attempts | 42 de 113 (37.17%) |
| Tokens entrada / salida | 4272516 / 232211 |
| Compactaciones (eventos / fallas) | 253 / 41 |
| Tokens del compactor (in / out) | 496623 / 112790 |

### `planner_summary` / `nova-lite` (ventana: 20)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 86 |
| Trials terminados por presupuesto | 36 |
| Attempts terminados por presupuesto | 36 |
| Terminaciones por attempt_index | {1: 36} |
| Iteraciones al morir (min/media/max) | 3 / 20.19 / 38 |
| Tool calls por iteración | {0: 34, 1: 1728, 2: 68, 3: 12, 4: 8, 5: 1, 7: 1, 8: 3, 9: 1, 20: 1} |
| Máximo de mensajes enviados | 20 |
| Llamadas con la ventana llena | 11 |
| Acciones ejecutadas | 1935 |
| Acciones repetidas (intra-trial) | 472 (24.39%) |
| Trials con repetición | 45 |
| Acciones re-derivadas entre attempts | 28 de 103 (27.18%) |
| Tokens entrada / salida | 4530847 / 259852 |
| Compactaciones (eventos / fallas) | 265 / 47 |
| Tokens del compactor (in / out) | 553101 / 127299 |

## Por caso

| Agente | Modelo | Trial config | Escenario | Ventana | Trials | Presupuesto | Compactaciones | Repetición |
|---|---|---|---|---:|---:|---:|---:|---:|
| `baseline` | `nova-lite` | `multi_attempt` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `baseline` | `nova-lite` | `multi_attempt` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 48.29% |
| `baseline` | `nova-lite` | `multi_attempt` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 10.74% |
| `baseline` | `nova-lite` | `multi_attempt` | `library-search` | 100 | 10 | 0 | 0 / 0 | 28.51% |
| `baseline` | `nova-lite` | `multi_attempt` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 48.77% |
| `baseline` | `nova-lite` | `multi_attempt` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `baseline` | `nova-lite` | `multi_attempt` | `vault-combination` | 100 | 10 | 0 | 0 / 0 | 30.60% |
| `baseline` | `nova-lite` | `multi_attempt` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 39.89% |
| `planner` | `nova-lite` | `multi_attempt` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `planner` | `nova-lite` | `multi_attempt` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 53.05% |
| `planner` | `nova-lite` | `multi_attempt` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 27.54% |
| `planner` | `nova-lite` | `multi_attempt` | `library-search` | 100 | 10 | 1 | 0 / 0 | 55.47% |
| `planner` | `nova-lite` | `multi_attempt` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 44.00% |
| `planner` | `nova-lite` | `multi_attempt` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 2.03% |
| `planner` | `nova-lite` | `multi_attempt` | `vault-combination` | 100 | 10 | 1 | 0 / 0 | 30.28% |
| `planner` | `nova-lite` | `multi_attempt` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 49.72% |
| `summary` | `nova-lite` | `multi_attempt` | `study-with-key` | 20 | 10 | 0 | 0 / 0 | 0.00% |
| `summary` | `nova-lite` | `multi_attempt` | `color-locks` | 20 | 10 | 2 | 40 / 3 | 35.55% |
| `summary` | `nova-lite` | `multi_attempt` | `apartment-keys` | 20 | 10 | 4 | 21 / 5 | 29.34% |
| `summary` | `nova-lite` | `multi_attempt` | `library-search` | 20 | 10 | 2 | 38 / 2 | 47.85% |
| `summary` | `nova-lite` | `multi_attempt` | `office-sequence` | 20 | 10 | 10 | 32 / 11 | 13.79% |
| `summary` | `nova-lite` | `multi_attempt` | `extreme-archive` | 20 | 10 | 2 | 41 / 4 | 11.39% |
| `summary` | `nova-lite` | `multi_attempt` | `vault-combination` | 20 | 10 | 5 | 47 / 6 | 41.93% |
| `summary` | `nova-lite` | `multi_attempt` | `backtracking-vault` | 20 | 10 | 9 | 34 / 10 | 30.50% |
| `planner_summary` | `nova-lite` | `multi_attempt` | `study-with-key` | 20 | 10 | 1 | 3 / 1 | 13.43% |
| `planner_summary` | `nova-lite` | `multi_attempt` | `color-locks` | 20 | 10 | 8 | 33 / 10 | 22.54% |
| `planner_summary` | `nova-lite` | `multi_attempt` | `apartment-keys` | 20 | 10 | 2 | 14 / 3 | 8.27% |
| `planner_summary` | `nova-lite` | `multi_attempt` | `library-search` | 20 | 10 | 2 | 30 / 2 | 22.49% |
| `planner_summary` | `nova-lite` | `multi_attempt` | `office-sequence` | 20 | 10 | 6 | 49 / 10 | 36.53% |
| `planner_summary` | `nova-lite` | `multi_attempt` | `extreme-archive` | 20 | 10 | 2 | 40 / 1 | 11.95% |
| `planner_summary` | `nova-lite` | `multi_attempt` | `vault-combination` | 20 | 10 | 7 | 47 / 10 | 31.09% |
| `planner_summary` | `nova-lite` | `multi_attempt` | `backtracking-vault` | 20 | 10 | 8 | 49 / 10 | 29.69% |
