# Análisis de presión de contexto — M3

**Runs:** `m3-final-run-001`, `m3-final-run-002`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 640 |
| Attempts | 1127 |
| Trials con terminación por presupuesto | 139 |
| Attempts terminados por presupuesto | 200 |
| Terminaciones por attempt_index | {1: 128, 2: 33, 3: 20, 4: 7, 5: 6, 6: 1, 7: 2, 8: 1, 9: 1, 10: 1} |
| Iteraciones al morir (min/media/max) | 1 / 19.73 / 40 |
| Tool calls por iteración | {0: 624, 1: 21606, 2: 560, 3: 180, 4: 65, 5: 13, 6: 18, 7: 8, 8: 28, 9: 2, 10: 1, 12: 1, 14: 1, 19: 1, 20: 6, 21: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 81 |
| Acciones ejecutadas | 23834 |
| Acciones repetidas (intra-trial) | 10575 (44.37%) |
| Trials con repetición | 370 |
| Acciones re-derivadas entre attempts | 4638 de 7722 (60.06%) |
| Tokens entrada / salida | 74170369 / 2357777 |
| Compactaciones (eventos / fallas) | 1862 / 254 |
| Tokens del compactor (in / out) | 3647903 / 792220 |

## Por sistema

### `baseline` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 231 |
| Trials con terminación por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 148, 1: 5035, 2: 113, 3: 23, 4: 11, 5: 2, 7: 2, 8: 3, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 1 |
| Acciones ejecutadas | 5442 |
| Acciones repetidas (intra-trial) | 2576 (47.34%) |
| Trials con repetición | 92 |
| Acciones re-derivadas entre attempts | 1003 de 1075 (93.30%) |
| Tokens entrada / salida | 22742172 / 348042 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `planner` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 235 |
| Trials con terminación por presupuesto | 4 |
| Attempts terminados por presupuesto | 4 |
| Terminaciones por attempt_index | {1: 4} |
| Iteraciones al morir (min/media/max) | 19 / 31.25 / 38 |
| Tool calls por iteración | {0: 168, 1: 4511, 2: 122, 3: 56, 4: 18, 5: 5, 6: 12, 8: 14, 21: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 6 |
| Acciones ejecutadas | 5206 |
| Acciones repetidas (intra-trial) | 2191 (42.09%) |
| Trials con repetición | 84 |
| Acciones re-derivadas entre attempts | 745 de 898 (82.96%) |
| Tokens entrada / salida | 20096635 / 329847 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `summary` / `nova-lite` (ventana: 20)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 354 |
| Trials con terminación por presupuesto | 69 |
| Attempts terminados por presupuesto | 99 |
| Terminaciones por attempt_index | {1: 61, 2: 17, 3: 11, 4: 3, 5: 3, 7: 1, 8: 1, 9: 1, 10: 1} |
| Iteraciones al morir (min/media/max) | 2 / 19.31 / 38 |
| Tool calls por iteración | {0: 178, 1: 6054, 2: 193, 3: 59, 4: 17, 5: 3, 6: 3, 7: 4, 8: 2, 9: 1, 12: 1, 14: 1, 19: 1, 20: 1} |
| Máximo de mensajes enviados | 20 |
| Llamadas con la ventana llena | 33 |
| Acciones ejecutadas | 6687 |
| Acciones repetidas (intra-trial) | 3083 (46.10%) |
| Trials con repetición | 96 |
| Acciones re-derivadas entre attempts | 1564 de 2962 (52.80%) |
| Tokens entrada / salida | 15514310 / 827046 |
| Compactaciones (eventos / fallas) | 946 / 126 |
| Tokens del compactor (in / out) | 1816923 / 396853 |

### `planner_summary` / `nova-lite` (ventana: 20)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 307 |
| Trials con terminación por presupuesto | 66 |
| Attempts terminados por presupuesto | 97 |
| Terminaciones por attempt_index | {1: 63, 2: 16, 3: 9, 4: 4, 5: 3, 6: 1, 7: 1} |
| Iteraciones al morir (min/media/max) | 1 / 19.68 / 40 |
| Tool calls por iteración | {0: 130, 1: 6006, 2: 132, 3: 42, 4: 19, 5: 3, 6: 3, 7: 2, 8: 9, 9: 1, 10: 1, 20: 4} |
| Máximo de mensajes enviados | 20 |
| Llamadas con la ventana llena | 41 |
| Acciones ejecutadas | 6499 |
| Acciones repetidas (intra-trial) | 2725 (41.93%) |
| Trials con repetición | 98 |
| Acciones re-derivadas entre attempts | 1326 de 2787 (47.58%) |
| Tokens entrada / salida | 15817252 / 852842 |
| Compactaciones (eventos / fallas) | 916 / 128 |
| Tokens del compactor (in / out) | 1830980 / 395367 |

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
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 74.12% |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 50.40% |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 0 / 0 | 79.35% |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 49.88% |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 25.88% |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 0 / 0 | 39.23% |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 60.35% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 3.08% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 18.83% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 0 / 0 | 29.39% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 49.76% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 2 | 0 / 0 | 54.08% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 74.54% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 20 | 10 | 0 | 0 / 0 | 1.75% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 20 | 10 | 3 | 42 / 8 | 27.05% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 20 | 10 | 3 | 30 / 4 | 37.02% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 20 | 10 | 3 | 60 / 3 | 54.78% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 20 | 10 | 7 | 116 / 18 | 57.84% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 20 | 10 | 4 | 121 / 7 | 40.07% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 20 | 10 | 7 | 183 / 21 | 62.27% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 20 | 10 | 8 | 141 / 24 | 60.07% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 20 | 10 | 0 | 1 / 0 | 5.08% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 20 | 10 | 3 | 55 / 7 | 37.81% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 20 | 10 | 3 | 34 / 6 | 43.77% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 20 | 10 | 1 | 36 / 3 | 34.29% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 20 | 10 | 8 | 112 / 19 | 64.64% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 20 | 10 | 2 | 117 / 1 | 32.42% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 20 | 10 | 8 | 178 / 36 | 57.24% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 20 | 10 | 5 | 118 / 9 | 58.71% |
