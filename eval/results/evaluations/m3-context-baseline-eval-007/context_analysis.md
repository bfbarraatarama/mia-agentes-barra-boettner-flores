# Análisis de presión de contexto — M3

**Runs:** `m3-nova-tool-repair-comparison-run-003`, `m3-nova-multi-attempt-run-004`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 320 |
| Attempts | 348 |
| Trials terminados por presupuesto | 5 |
| Attempts terminados por presupuesto | 5 |
| Terminaciones por attempt_index | {1: 5} |
| Iteraciones al morir (min/media/max) | 26 / 31.8 / 38 |
| Tool calls por iteración | {0: 231, 1: 7824, 2: 212, 3: 87, 4: 27, 5: 8, 6: 3, 7: 6, 8: 5, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 1 |
| Acciones ejecutadas | 8763 |
| Acciones repetidas (intra-trial) | 3020 (34.46%) |
| Trials con repetición | 178 |
| Acciones re-derivadas entre attempts | 15 de 50 (30.00%) |
| Tokens entrada / salida | 31273551 / 523251 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

## Por sistema

### `minimal` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 188 |
| Trials terminados por presupuesto | 4 |
| Attempts terminados por presupuesto | 4 |
| Terminaciones por attempt_index | {1: 4} |
| Iteraciones al morir (min/media/max) | 26 / 30.25 / 35 |
| Tool calls por iteración | {0: 134, 1: 3767, 2: 120, 3: 52, 4: 20, 5: 7, 6: 3, 7: 4, 8: 2, 20: 1} |
| Máximo de mensajes enviados | 100 |
| Llamadas con la ventana llena | 1 |
| Acciones ejecutadas | 4349 |
| Acciones repetidas (intra-trial) | 1452 (33.39%) |
| Trials con repetición | 88 |
| Acciones re-derivadas entre attempts | 15 de 50 (30.00%) |
| Tokens entrada / salida | 15094629 / 255607 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

### `minimal_tool_repair` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 160 |
| Attempts | 160 |
| Trials terminados por presupuesto | 1 |
| Attempts terminados por presupuesto | 1 |
| Terminaciones por attempt_index | {1: 1} |
| Iteraciones al morir (min/media/max) | 38 / 38.0 / 38 |
| Tool calls por iteración | {0: 97, 1: 4057, 2: 92, 3: 35, 4: 7, 5: 1, 7: 2, 8: 3} |
| Máximo de mensajes enviados | 99 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 4414 |
| Acciones repetidas (intra-trial) | 1568 (35.52%) |
| Trials con repetición | 90 |
| Acciones re-derivadas entre attempts | 0 de 0 (n/a) |
| Tokens entrada / salida | 16178922 / 267644 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

## Por caso

| Agente | Modelo | Trial config | Escenario | Ventana | Trials | Presupuesto | Compactaciones | Repetición |
|---|---|---|---|---:|---:|---:|---:|---:|
| `minimal` | `nova-lite` | `single_attempt` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 3.64% |
| `minimal` | `nova-lite` | `single_attempt` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 40.41% |
| `minimal` | `nova-lite` | `single_attempt` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 7.03% |
| `minimal` | `nova-lite` | `single_attempt` | `library-search` | 100 | 10 | 0 | 0 / 0 | 18.87% |
| `minimal` | `nova-lite` | `single_attempt` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 51.95% |
| `minimal` | `nova-lite` | `single_attempt` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 0.85% |
| `minimal` | `nova-lite` | `single_attempt` | `vault-combination` | 100 | 10 | 2 | 0 / 0 | 36.16% |
| `minimal` | `nova-lite` | `single_attempt` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 17.22% |
| `minimal_tool_repair` | `nova-lite` | `single_attempt` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `minimal_tool_repair` | `nova-lite` | `single_attempt` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 54.55% |
| `minimal_tool_repair` | `nova-lite` | `single_attempt` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 40.65% |
| `minimal_tool_repair` | `nova-lite` | `single_attempt` | `library-search` | 100 | 10 | 0 | 0 / 0 | 43.86% |
| `minimal_tool_repair` | `nova-lite` | `single_attempt` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 46.69% |
| `minimal_tool_repair` | `nova-lite` | `single_attempt` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 16.14% |
| `minimal_tool_repair` | `nova-lite` | `single_attempt` | `vault-combination` | 100 | 10 | 0 | 0 / 0 | 34.46% |
| `minimal_tool_repair` | `nova-lite` | `single_attempt` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 20.99% |
| `minimal` | `nova-lite` | `multi_attempt` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 0.00% |
| `minimal` | `nova-lite` | `multi_attempt` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 23.02% |
| `minimal` | `nova-lite` | `multi_attempt` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 22.36% |
| `minimal` | `nova-lite` | `multi_attempt` | `library-search` | 100 | 10 | 0 | 0 / 0 | 57.32% |
| `minimal` | `nova-lite` | `multi_attempt` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 45.91% |
| `minimal` | `nova-lite` | `multi_attempt` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 28.03% |
| `minimal` | `nova-lite` | `multi_attempt` | `vault-combination` | 100 | 10 | 2 | 0 / 0 | 39.74% |
| `minimal` | `nova-lite` | `multi_attempt` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 41.19% |
| `minimal_tool_repair` | `nova-lite` | `multi_attempt` | `study-with-key` | 100 | 10 | 0 | 0 / 0 | 5.26% |
| `minimal_tool_repair` | `nova-lite` | `multi_attempt` | `color-locks` | 100 | 10 | 0 | 0 / 0 | 40.49% |
| `minimal_tool_repair` | `nova-lite` | `multi_attempt` | `apartment-keys` | 100 | 10 | 0 | 0 / 0 | 26.51% |
| `minimal_tool_repair` | `nova-lite` | `multi_attempt` | `library-search` | 100 | 10 | 0 | 0 / 0 | 53.98% |
| `minimal_tool_repair` | `nova-lite` | `multi_attempt` | `office-sequence` | 100 | 10 | 0 | 0 / 0 | 53.69% |
| `minimal_tool_repair` | `nova-lite` | `multi_attempt` | `extreme-archive` | 100 | 10 | 0 | 0 / 0 | 12.75% |
| `minimal_tool_repair` | `nova-lite` | `multi_attempt` | `vault-combination` | 100 | 10 | 1 | 0 / 0 | 20.75% |
| `minimal_tool_repair` | `nova-lite` | `multi_attempt` | `backtracking-vault` | 100 | 10 | 0 | 0 / 0 | 29.00% |
