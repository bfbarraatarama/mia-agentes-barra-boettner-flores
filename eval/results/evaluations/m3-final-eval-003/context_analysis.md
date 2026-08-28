# Análisis de presión de contexto — M3

**Runs:** `m3-final-run-002`, `m3-final-run-003`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 640 |
| Attempts | 1450 |
| Trials con terminación por presupuesto | 134 |
| Attempts terminados por presupuesto | 248 |
| Terminaciones por attempt_index | {1: 113, 2: 62, 3: 34, 4: 13, 5: 12, 6: 5, 7: 3, 8: 3, 9: 2, 10: 1} |
| Iteraciones al morir (min/media/max) | 1 / 20.75 / 40 |
| Tool calls por iteración | {0: 751, 1: 29087, 2: 644, 3: 196, 4: 140, 5: 11, 6: 6, 7: 5, 8: 17, 9: 1, 10: 1, 12: 1, 14: 1, 15: 5, 19: 1, 20: 5, 21: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 86 |
| Acciones ejecutadas | 31666 |
| Acciones repetidas (intra-trial) | 16326 (51.56%) |
| Trials con repetición | 405 |
| Acciones re-derivadas entre attempts | 9158 de 15462 (59.23%) |
| Tokens entrada / salida | 107077158 / 3352193 |
| Compactaciones (eventos / fallas) | 2765 / 318 |
| Tokens del compactor (in / out) | 5730278 / 1150406 |

## Por sistema

### `baseline` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 132 |
| Trials con terminación por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 77, 1: 3049, 2: 66, 3: 12, 4: 7, 7: 1, 8: 1, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 1 |
| Acciones ejecutadas | 3280 |
| Acciones repetidas (intra-trial) | 1872 (57.07%) |
| Trials con repetición | 49 |
| Acciones re-derivadas entre attempts | 967 de 1016 (95.18%) |
| Tokens entrada / salida | 14780118 / 215171 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `planner` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 135 |
| Trials con terminación por presupuesto | 2 |
| Attempts terminados por presupuesto | 2 |
| Terminaciones por attempt_index | {1: 2} |
| Iteraciones al morir (min/media/max) | 37 / 37.5 / 38 |
| Tool calls por iteración | {0: 96, 1: 2468, 2: 76, 3: 29, 4: 11, 5: 1, 8: 5, 21: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 5 |
| Acciones ejecutadas | 2812 |
| Acciones repetidas (intra-trial) | 1250 (44.45%) |
| Trials con repetición | 39 |
| Acciones re-derivadas entre attempts | 660 de 795 (83.02%) |
| Tokens entrada / salida | 10963601 / 179119 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `summary` / `nova-lite` (ventana: 20)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 259 |
| Trials con terminación por presupuesto | 35 |
| Attempts terminados por presupuesto | 65 |
| Terminaciones por attempt_index | {1: 27, 2: 17, 3: 11, 4: 3, 5: 3, 7: 1, 8: 1, 9: 1, 10: 1} |
| Iteraciones al morir (min/media/max) | 2 / 20.29 / 38 |
| Tool calls por iteración | {0: 136, 1: 4360, 2: 131, 3: 44, 4: 12, 5: 2, 6: 3, 7: 2, 8: 2, 9: 1, 12: 1, 14: 1, 19: 1, 20: 1} |
| Máximo de mensajes enviados | 20 |
| Llamadas con la ventana llena | 17 |
| Acciones ejecutadas | 4824 |
| Acciones repetidas (intra-trial) | 2513 (52.09%) |
| Trials con repetición | 57 |
| Acciones re-derivadas entre attempts | 1522 de 2849 (53.42%) |
| Tokens entrada / salida | 11241794 / 594835 |
| Compactaciones (eventos / fallas) | 693 / 85 |
| Tokens del compactor (in / out) | 1320300 / 284063 |

### `planner_summary` / `nova-lite` (ventana: 20)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 221 |
| Trials con terminación por presupuesto | 30 |
| Attempts terminados por presupuesto | 61 |
| Terminaciones por attempt_index | {1: 27, 2: 16, 3: 9, 4: 4, 5: 3, 6: 1, 7: 1} |
| Iteraciones al morir (min/media/max) | 1 / 19.38 / 40 |
| Tool calls por iteración | {0: 96, 1: 4278, 2: 64, 3: 30, 4: 11, 5: 2, 6: 3, 7: 1, 8: 6, 10: 1, 20: 3} |
| Máximo de mensajes enviados | 20 |
| Llamadas con la ventana llena | 30 |
| Acciones ejecutadas | 4564 |
| Acciones repetidas (intra-trial) | 2253 (49.36%) |
| Trials con repetición | 53 |
| Acciones re-derivadas entre attempts | 1298 de 2684 (48.36%) |
| Tokens entrada / salida | 11286405 / 592990 |
| Compactaciones (eventos / fallas) | 651 / 81 |
| Tokens del compactor (in / out) | 1277879 / 268068 |

### `baseline_incremental` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 116 |
| Trials con terminación por presupuesto | 2 |
| Attempts terminados por presupuesto | 2 |
| Terminaciones por attempt_index | {1: 2} |
| Iteraciones al morir (min/media/max) | 38 / 39.0 / 40 |
| Tool calls por iteración | {0: 59, 1: 3088, 2: 76, 3: 8, 4: 5} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 2 |
| Acciones ejecutadas | 3282 |
| Acciones repetidas (intra-trial) | 1863 (56.76%) |
| Trials con repetición | 49 |
| Acciones re-derivadas entre attempts | 902 de 1041 (86.65%) |
| Tokens entrada / salida | 16992486 / 225937 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `planner_incremental` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 125 |
| Trials con terminación por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 72, 1: 2979, 2: 59, 3: 8, 4: 1, 5: 3, 8: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 4 |
| Acciones ejecutadas | 3148 |
| Acciones repetidas (intra-trial) | 1719 (54.61%) |
| Trials con repetición | 46 |
| Acciones re-derivadas entre attempts | 934 de 1001 (93.31%) |
| Tokens entrada / salida | 16034985 / 225910 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `summary_incremental` / `nova-lite` (ventana: 20)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 216 |
| Trials con terminación por presupuesto | 34 |
| Attempts terminados por presupuesto | 64 |
| Terminaciones por attempt_index | {1: 28, 2: 17, 3: 7, 4: 3, 5: 2, 6: 3, 7: 1, 8: 2, 9: 1} |
| Iteraciones al morir (min/media/max) | 7 / 20.05 / 38 |
| Tool calls por iteración | {0: 91, 1: 4465, 2: 54, 3: 12, 4: 4, 5: 3, 7: 1, 8: 1} |
| Máximo de mensajes enviados | 20 |
| Llamadas con la ventana llena | 9 |
| Acciones ejecutadas | 4581 |
| Acciones repetidas (intra-trial) | 2279 (49.75%) |
| Trials con repetición | 57 |
| Acciones re-derivadas entre attempts | 1345 de 2836 (47.43%) |
| Tokens entrada / salida | 12186533 / 578126 |
| Compactaciones (eventos / fallas) | 660 / 80 |
| Tokens del compactor (in / out) | 1483218 / 277208 |

### `planner_summary_incremental` / `nova-lite` (ventana: 20)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 246 |
| Trials con terminación por presupuesto | 31 |
| Attempts terminados por presupuesto | 54 |
| Terminaciones por attempt_index | {1: 27, 2: 12, 3: 7, 4: 3, 5: 4, 6: 1} |
| Iteraciones al morir (min/media/max) | 6 / 22.39 / 38 |
| Tool calls por iteración | {0: 124, 1: 4400, 2: 118, 3: 53, 4: 89, 8: 1, 15: 5} |
| Máximo de mensajes enviados | 20 |
| Llamadas con la ventana llena | 18 |
| Acciones ejecutadas | 5175 |
| Acciones repetidas (intra-trial) | 2577 (49.80%) |
| Trials con repetición | 55 |
| Acciones re-derivadas entre attempts | 1530 de 3240 (47.22%) |
| Tokens entrada / salida | 13591236 / 740105 |
| Compactaciones (eventos / fallas) | 761 / 72 |
| Tokens del compactor (in / out) | 1648881 / 321067 |

## Por caso

| Agente | Modelo | Trial config | Escenario | Ventana | Trials | Presupuesto | Compactaciones | Repetición |
|---|---|---|---|---:|---:|---:|---:|---:|
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
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 32.47% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 2.42% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 0 / 0 | 63.85% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 65.73% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 64.98% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 2 | 0 / 0 | 60.31% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 60.47% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 14.29% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 59.05% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 40.72% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 0 / 0 | 49.23% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 57.09% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 45.91% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 0 / 0 | 62.31% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 59.45% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 20 | 10 | 0 | 0 / 0 | 1.64% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 20 | 10 | 4 | 56 / 6 | 38.22% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 20 | 10 | 1 | 20 / 3 | 17.92% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 20 | 10 | 3 | 51 / 3 | 48.85% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 20 | 10 | 8 | 96 / 20 | 51.81% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 20 | 10 | 4 | 103 / 4 | 26.70% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 20 | 10 | 8 | 210 / 31 | 65.97% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 20 | 10 | 6 | 124 / 13 | 57.83% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 20 | 10 | 0 | 0 / 0 | 0.00% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 20 | 10 | 3 | 39 / 4 | 39.47% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 20 | 10 | 0 | 19 / 0 | 22.03% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 20 | 10 | 1 | 90 / 1 | 53.31% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 20 | 10 | 9 | 82 / 17 | 49.03% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 20 | 10 | 2 | 182 / 4 | 21.94% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 20 | 10 | 9 | 176 / 25 | 63.42% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 20 | 10 | 7 | 173 / 21 | 69.97% |
