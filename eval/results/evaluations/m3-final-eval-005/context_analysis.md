# Análisis de presión de contexto — M3

**Run:** `m3-final-run-005`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 277 |
| Trials con terminación por presupuesto | 1 |
| Attempts terminados por presupuesto | 1 |
| Terminaciones por attempt_index | {2: 1} |
| Iteraciones al morir (min/media/max) | 39 / 39.0 / 39 |
| Tool calls por iteración | {0: 127, 1: 7068, 2: 192, 3: 21, 4: 15, 5: 23, 7: 1, 8: 3, 10: 4, 20: 1} |
| Máximo de mensajes enviados | 99 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 7779 |
| Acciones repetidas (intra-trial) | 3976 (51.11%) |
| Trials con repetición | 117 |
| Acciones re-derivadas entre attempts | 1712 de 2970 (57.64%) |
| Tokens entrada / salida | 23434580 / 901857 |
| Compactaciones (eventos / fallas) | 697 / 59 |
| Tokens del compactor (in / out) | 2545903 / 330972 |

## Por sistema

### `summary_incremental_strategic` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 160 |
| Trials con terminación por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 88, 1: 3574, 2: 39, 3: 5, 4: 4, 5: 22, 7: 1, 8: 2, 10: 3, 20: 1} |
| Máximo de mensajes enviados | 79 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 3866 |
| Acciones repetidas (intra-trial) | 1979 (51.19%) |
| Trials con repetición | 57 |
| Acciones re-derivadas entre attempts | 738 de 1472 (50.14%) |
| Tokens entrada / salida | 11734377 / 465484 |
| Compactaciones (eventos / fallas) | 347 / 28 |
| Tokens del compactor (in / out) | 1323706 / 167682 |

### `planner_summary_incremental_strategic` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 117 |
| Trials con terminación por presupuesto | 1 |
| Attempts terminados por presupuesto | 1 |
| Terminaciones por attempt_index | {2: 1} |
| Iteraciones al morir (min/media/max) | 39 / 39.0 / 39 |
| Tool calls por iteración | {0: 39, 1: 3494, 2: 153, 3: 16, 4: 11, 5: 1, 8: 1, 10: 1} |
| Máximo de mensajes enviados | 99 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 3913 |
| Acciones repetidas (intra-trial) | 1997 (51.04%) |
| Trials con repetición | 60 |
| Acciones re-derivadas entre attempts | 974 de 1498 (65.02%) |
| Tokens entrada / salida | 11700203 / 436373 |
| Compactaciones (eventos / fallas) | 350 / 31 |
| Tokens del compactor (in / out) | 1222197 / 163290 |

## Por caso

| Agente | Modelo | Trial config | Escenario | Ventana | Trials | Presupuesto | Compactaciones | Repetición |
|---|---|---|---|---:|---:|---:|---:|---:|
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 14 / 1 | 2.09% |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 13 / 3 | 24.85% |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 40 / 1 | 48.44% |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 56 / 7 | 63.29% |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 77 / 8 | 39.16% |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 79 / 5 | 66.90% |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 68 / 3 | 58.54% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 5.36% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 22 / 0 | 33.72% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 13 / 0 | 20.35% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 29 / 1 | 41.62% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 45 / 4 | 49.32% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 80 / 2 | 35.86% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 80 / 11 | 59.58% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 1 | 81 / 13 | 74.89% |
