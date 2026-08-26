# Análisis de presión de contexto — M3

**Run:** `m3-final-run-004`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 297 |
| Trials con terminación por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 163, 1: 6947, 2: 71, 3: 9, 4: 4, 5: 7, 8: 2, 16: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 6 |
| Acciones ejecutadas | 7199 |
| Acciones repetidas (intra-trial) | 3550 (49.31%) |
| Trials con repetición | 109 |
| Acciones re-derivadas entre attempts | 1841 de 2566 (71.75%) |
| Tokens entrada / salida | 31034249 / 615899 |
| Compactaciones (eventos / fallas) | 190 / 29 |
| Tokens del compactor (in / out) | 912070 / 121452 |

## Por sistema

### `summary_incremental_token_trigger` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 118 |
| Trials con terminación por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 54, 1: 3426, 2: 29, 3: 7} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 1 |
| Acciones ejecutadas | 3505 |
| Acciones repetidas (intra-trial) | 1598 (45.59%) |
| Trials con repetición | 50 |
| Acciones re-derivadas entre attempts | 785 de 1157 (67.85%) |
| Tokens entrada / salida | 14942673 / 302790 |
| Compactaciones (eventos / fallas) | 95 / 19 |
| Tokens del compactor (in / out) | 519222 / 67372 |

### `planner_summary_incremental_token_trigger` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Attempts | 179 |
| Trials con terminación por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {0: 109, 1: 3521, 2: 42, 3: 2, 4: 4, 5: 7, 8: 2, 16: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 5 |
| Acciones ejecutadas | 3694 |
| Acciones repetidas (intra-trial) | 1952 (52.84%) |
| Trials con repetición | 59 |
| Acciones re-derivadas entre attempts | 1056 de 1409 (74.95%) |
| Tokens entrada / salida | 16091576 / 313109 |
| Compactaciones (eventos / fallas) | 95 / 10 |
| Tokens del compactor (in / out) | 392848 / 54080 |

## Por caso

| Agente | Modelo | Trial config | Escenario | Ventana | Trials | Presupuesto | Compactaciones | Repetición |
|---|---|---|---|---:|---:|---:|---:|---:|
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 1 / 0 | 59.52% |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 23 / 8 | 61.34% |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 1 / 0 | 48.98% |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 25 / 8 | 49.47% |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 3 / 0 | 53.59% |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 33 / 2 | 13.66% |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 7 / 1 | 61.64% |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 2 / 0 | 41.21% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 1.72% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 10 | 0 | 9 / 1 | 60.09% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 10 | 0 | 2 / 0 | 54.72% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 10 | 0 | 7 / 1 | 43.34% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 40.06% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 10 | 0 | 49 / 2 | 32.22% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 10 | 0 | 10 / 1 | 72.26% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 10 | 0 | 18 / 5 | 66.01% |
