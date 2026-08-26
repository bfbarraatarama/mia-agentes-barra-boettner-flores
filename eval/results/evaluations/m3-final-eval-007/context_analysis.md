# Análisis de presión de contexto — M3

**Runs:** `m3-final-run-006`, `m3-final-run-007`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 320 |
| Attempts | 632 |
| Trials con terminación por presupuesto | 3 |
| Attempts terminados por presupuesto | 3 |
| Terminaciones por attempt_index | {1: 1, 2: 2} |
| Iteraciones al morir (min/media/max) | 15 / 27.67 / 39 |
| Tool calls por iteración | {0: 351, 1: 13535, 2: 352, 3: 146, 4: 28, 5: 15, 6: 46, 7: 2, 8: 15, 9: 1, 10: 2, 13: 1, 15: 1, 18: 1, 19: 1, 20: 4} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 7 |
| Acciones ejecutadas | 15437 |
| Acciones repetidas (intra-trial) | 8007 (51.87%) |
| Trials con repetición | 220 |
| Acciones re-derivadas entre attempts | 3828 de 5492 (69.70%) |
| Tokens entrada / salida | 50602767 / 1486625 |
| Compactaciones (eventos / fallas) | 899 / 175 |
| Tokens del compactor (in / out) | 2865398 / 462942 |

## Por sistema

### `summary_token_trigger` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 150 |
| Trials con terminación por presupuesto | 1 |
| Attempts terminados por presupuesto | 1 |
| Terminaciones por attempt_index | {2: 1} |
| Iteraciones al morir (min/media/max) | 15 / 15.0 / 15 |
| Tool calls por iteración | {0: 89, 1: 3193, 2: 40, 3: 84, 4: 5, 5: 1, 6: 46, 8: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 3 |
| Acciones ejecutadas | 3828 |
| Acciones repetidas (intra-trial) | 1935 (50.55%) |
| Trials con repetición | 51 |
| Acciones re-derivadas entre attempts | 936 de 1276 (73.35%) |
| Tokens entrada / salida | 13558381 / 273450 |
| Compactaciones (eventos / fallas) | 81 / 13 |
| Tokens del compactor (in / out) | 286187 / 52524 |

### `planner_summary_token_trigger` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 151 |
| Trials con terminación por presupuesto | 1 |
| Attempts terminados por presupuesto | 1 |
| Terminaciones por attempt_index | {1: 1} |
| Iteraciones al morir (min/media/max) | 29 / 29.0 / 29 |
| Tool calls por iteración | {0: 83, 1: 3299, 2: 98, 3: 39, 4: 12, 5: 12, 8: 5, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 4 |
| Acciones ejecutadas | 3777 |
| Acciones repetidas (intra-trial) | 2136 (56.55%) |
| Trials con repetición | 54 |
| Acciones re-derivadas entre attempts | 1074 de 1370 (78.39%) |
| Tokens entrada / salida | 14667579 / 305954 |
| Compactaciones (eventos / fallas) | 83 / 14 |
| Tokens del compactor (in / out) | 413489 / 64494 |

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
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 11 / 4 | 68.30% |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 2 / 0 | 55.51% |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 5 / 1 | 61.27% |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 1 | 6 / 3 | 69.01% |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 49 / 3 | 26.78% |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 6 / 1 | 53.54% |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 2 / 1 | 38.17% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 3.17% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 9 / 1 | 74.24% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 8.76% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 17 / 6 | 54.12% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 3 / 0 | 59.04% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 35 / 3 | 37.81% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 1 | 15 / 4 | 69.94% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 4 / 0 | 55.66% |
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
