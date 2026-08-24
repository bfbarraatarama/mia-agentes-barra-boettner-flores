# Análisis de presión de contexto — M3

**Run:** `m3-llm-judge-smoke-summary-run-001`

## Totales

| Métrica | Valor |
|---|---:|
| Trials | 2 |
| Attempts | 2 |
| Trials terminados por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {1: 78, 2: 2} |
| Máximo de mensajes enviados | 80 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 82 |
| Acciones repetidas (intra-trial) | 35 (42.68%) |
| Trials con repetición | 2 |
| Acciones re-derivadas entre attempts | 0 de 0 (n/a) |
| Tokens entrada / salida | 242431 / 3979 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

## Por sistema

### `minimal_summary` / `nova-lite` (ventana: 100)

| Métrica | Valor |
|---|---:|
| Trials | 2 |
| Attempts | 2 |
| Trials terminados por presupuesto | 0 |
| Attempts terminados por presupuesto | 0 |
| Terminaciones por attempt_index | — |
| Iteraciones al morir (min/media/max) | None / None / None |
| Tool calls por iteración | {1: 78, 2: 2} |
| Máximo de mensajes enviados | 80 |
| Llamadas con la ventana llena | 0 |
| Acciones ejecutadas | 82 |
| Acciones repetidas (intra-trial) | 35 (42.68%) |
| Trials con repetición | 2 |
| Acciones re-derivadas entre attempts | 0 de 0 (n/a) |
| Tokens entrada / salida | 242431 / 3979 |
| Compactaciones (eventos / fallas) | 0 / 0 |
| Tokens del compactor (in / out) | 0 / 0 |

## Por caso

| Agente | Modelo | Trial config | Escenario | Ventana | Trials | Presupuesto | Compactaciones | Repetición |
|---|---|---|---|---:|---:|---:|---:|---:|
| `minimal_summary` | `nova-lite` | `multi_attempt` | `office-sequence` | 100 | 2 | 0 | 0 / 0 | 42.68% |
