# Análisis de presión de contexto — M3

**Run:** `m3-final-run-008`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 480 |
| Attempts | 793 |
| Trials con terminación por presupuesto | 10 |
| Attempts terminados por presupuesto | 11 |
| Terminaciones por attempt_index | {1: 8, 2: 3} |
| Iteraciones al morir (min/media/max) | 29 / 34.55 / 40 |
| Tool calls por iteración | {0: 457, 1: 18250, 2: 391, 3: 94, 4: 32, 5: 2, 6: 8, 8: 19, 9: 1, 10: 2, 20: 2} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 27 |
| Acciones ejecutadas | 19695 |
| Acciones repetidas (intra-trial) | 10708 (54.37%) |
| Trials con repetición | 297 |
| Acciones re-derivadas entre attempts | 5251 de 6419 (81.80%) |
| Tokens entrada / salida | 89582306 / 1350855 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

## Por sistema

### `planner` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 274 |
| Trials con terminación por presupuesto | 5 |
| Attempts terminados por presupuesto | 6 |
| Terminaciones por attempt_index | {1: 4, 2: 2} |
| Iteraciones al morir (min/media/max) | 29 / 35.83 / 40 |
| Tool calls por iteración | {0: 152, 1: 6458, 2: 169, 3: 36, 4: 9, 5: 1, 6: 1, 8: 15, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 12 |
| Acciones ejecutadas | 7080 |
| Acciones repetidas (intra-trial) | 3952 (55.82%) |
| Trials con repetición | 98 |
| Acciones re-derivadas entre attempts | 1869 de 2436 (76.72%) |
| Tokens entrada / salida | 29414399 / 436391 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `baseline_incremental` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 255 |
| Trials con terminación por presupuesto | 2 |
| Attempts terminados por presupuesto | 2 |
| Terminaciones por attempt_index | {1: 1, 2: 1} |
| Iteraciones al morir (min/media/max) | 30 / 31.5 / 33 |
| Tool calls por iteración | {0: 141, 1: 6305, 2: 81, 3: 28, 4: 1, 6: 7, 8: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 6 |
| Acciones ejecutadas | 6596 |
| Acciones repetidas (intra-trial) | 3669 (55.62%) |
| Trials con repetición | 96 |
| Acciones re-derivadas entre attempts | 1886 de 2214 (85.19%) |
| Tokens entrada / salida | 32453330 / 489501 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `planner_incremental` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 264 |
| Trials con terminación por presupuesto | 3 |
| Attempts terminados por presupuesto | 3 |
| Terminaciones por attempt_index | {1: 3} |
| Iteraciones al morir (min/media/max) | 30 / 34.0 / 38 |
| Tool calls por iteración | {0: 164, 1: 5487, 2: 141, 3: 30, 4: 22, 5: 1, 8: 3, 9: 1, 10: 2, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 9 |
| Acciones ejecutadas | 6019 |
| Acciones repetidas (intra-trial) | 3087 (51.29%) |
| Trials con repetición | 103 |
| Acciones re-derivadas entre attempts | 1496 de 1769 (84.57%) |
| Tokens entrada / salida | 27714577 / 424963 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

## Por caso

| Agente | Modelo | Trial config | Escenario | Ventana | Trials | Presupuesto | Compactaciones | Repetición |
|---|---|---|---|---:|---:|---:|---:|---:|
| `planner` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 20 | 0 | 0 / 0 | 0.00% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 20 | 1 | 0 / 0 | 62.96% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 20 | 0 | 0 / 0 | 55.20% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 20 | 1 | 0 / 0 | 50.25% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 20 | 0 | 0 / 0 | 59.04% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 20 | 0 | 0 / 0 | 0.39% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 20 | 2 | 0 / 0 | 63.78% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 20 | 1 | 0 / 0 | 66.86% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 20 | 1 | 0 / 0 | 37.20% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 20 | 0 | 0 / 0 | 57.84% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 20 | 0 | 0 / 0 | 23.25% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 20 | 1 | 0 / 0 | 65.22% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 20 | 0 | 0 / 0 | 63.77% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 20 | 0 | 0 / 0 | 38.32% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 20 | 0 | 0 / 0 | 56.23% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 20 | 0 | 0 / 0 | 59.50% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 100 | 20 | 0 | 0 / 0 | 26.24% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 100 | 20 | 0 | 0 / 0 | 54.87% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 100 | 20 | 0 | 0 / 0 | 30.27% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 100 | 20 | 1 | 0 / 0 | 57.20% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 100 | 20 | 0 | 0 / 0 | 45.98% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 100 | 20 | 0 | 0 / 0 | 33.18% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 100 | 20 | 1 | 0 / 0 | 61.81% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 100 | 20 | 1 | 0 / 0 | 56.63% |
