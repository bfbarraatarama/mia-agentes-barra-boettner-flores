# Análisis de presión de contexto — M3

**Runs:** `m3-final-run-002`, `m3-final-run-007`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 480 |
| Attempts | 1078 |
| Trials con terminación por presupuesto | 68 |
| Attempts terminados por presupuesto | 129 |
| Terminaciones por attempt_index | {1: 56, 2: 34, 3: 20, 4: 7, 5: 6, 6: 1, 7: 2, 8: 1, 9: 1, 10: 1} |
| Iteraciones al morir (min/media/max) | 1 / 20.27 / 40 |
| Tool calls por iteración | {0: 584, 1: 21198, 2: 551, 3: 138, 4: 52, 5: 7, 6: 6, 7: 6, 8: 23, 9: 2, 10: 3, 12: 1, 13: 1, 14: 1, 15: 1, 18: 1, 19: 2, 20: 8, 21: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 53 |
| Acciones ejecutadas | 23312 |
| Acciones repetidas (intra-trial) | 11824 (50.72%) |
| Trials con repetición | 313 |
| Acciones re-derivadas entre attempts | 6265 de 10190 (61.48%) |
| Tokens entrada / salida | 70648725 / 2489336 |
| Compactaciones (eventos / fallas) | 2079 / 314 |
| Tokens del compactor (in / out) | 4763901 / 898055 |

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

### `summary_strategic` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 178 |
| Trials con terminación por presupuesto | 1 |
| Attempts terminados por presupuesto | 1 |
| Terminaciones por attempt_index | {2: 1} |
| Iteraciones al morir (min/media/max) | 39 / 39.0 / 39 |
| Tool calls por iteración | {0: 108, 1: 3335, 2: 107, 3: 6, 4: 5, 7: 2, 8: 1, 13: 1, 20: 3} |
| Máximo de mensajes enviados | 99 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 3680 |
| Acciones repetidas (intra-trial) | 1829 (49.70%) |
| Trials con repetición | 57 |
| Acciones re-derivadas entre attempts | 828 de 1305 (63.45%) |
| Tokens entrada / salida | 10587357 / 467854 |
| Compactaciones (eventos / fallas) | 351 / 75 |
| Tokens del compactor (in / out) | 1048377 / 166426 |

### `planner_summary_strategic` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 153 |
| Trials con terminación por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 71, 1: 3708, 2: 107, 3: 17, 4: 6, 5: 2, 8: 8, 9: 1, 10: 2, 15: 1, 18: 1, 19: 1} |
| Máximo de mensajes enviados | 97 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 4152 |
| Acciones repetidas (intra-trial) | 2107 (50.75%) |
| Trials con repetición | 58 |
| Acciones re-derivadas entre attempts | 990 de 1541 (64.24%) |
| Tokens entrada / salida | 11789450 / 439367 |
| Compactaciones (eventos / fallas) | 384 / 73 |
| Tokens del compactor (in / out) | 1117345 / 179498 |

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
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 1 / 0 | 3.77% |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 1 | 50 / 22 | 52.93% |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 10 / 1 | 3.88% |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 47 / 5 | 61.75% |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 41 / 13 | 42.53% |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 63 / 5 | 31.73% |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 76 / 16 | 60.59% |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 63 / 13 | 59.44% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 37 / 12 | 50.35% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 27 / 5 | 51.35% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 49 / 17 | 50.56% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 42 / 16 | 47.26% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 82 / 2 | 36.36% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 76 / 11 | 60.12% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 71 / 10 | 61.78% |
