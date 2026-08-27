# Análisis de recuperación entre attempts — M3

**Run:** `m3-final-run-004`

Sólo se incluyen condiciones cuyo manifest declara una política `recoverable_attempt_terminations`.

**Trials ignorados sin política de recovery:** 0

## Resumen

| Métrica | Valor |
|---|---:|
| Trials analizados | 160 |
| Trials con terminación estructurada | 78 |
| Eventos de terminación | 132 |
| Eventos configurados como recuperables | 132 |
| Eventos con goal ya cumplido | 17 |
| Recuperaciones que abrieron otro attempt | 61 |
| Trials con recuperación | 61 |
| Trials recuperados con éxito final | 5 |
| Trials recuperados con fallo final | 56 |
| Éxito final entre trials recuperados | 8.2% |
| Eventos recuperables sin siguiente attempt | 54 |
| Terminaciones fatales no configuradas | 0 |
| Recuperaciones inesperadas | 0 |
| Trials con múltiples terminaciones | 54 |

## Por causa

| Causa | Eventos | Trials | Recuperaciones | Trials recuperados | Éxito final | Fallo final | Goal ya cumplido | Sin siguiente attempt | Repetición |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `max_iterations` | 132 | 78 | 61 | 61 | 5 | 56 | 17 | 54 | 54 |

## Por sistema y configuración de trial

| Agente | Modelo | Trial config | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos | Éxito tras recovery |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | 80 | 64 | 28 | 2 | 26 | 7.1% |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | 80 | 68 | 33 | 3 | 30 | 9.1% |

## Por caso

| Agente | Modelo | Trial config | Escenario | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos |
|---|---|---|---|---:|---:|---:|---:|---:|
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 2 | 1 | 0 | 1 |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 8 | 4 | 1 | 3 |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 3 | 1 | 0 | 1 |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 5 | 2 | 0 | 2 |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 11 | 2 | 0 | 2 |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 18 | 9 | 0 | 9 |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 13 | 7 | 1 | 6 |
| `summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 4 | 2 | 0 | 2 |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 8 | 5 | 1 | 4 |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 4 | 2 | 0 | 2 |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 4 | 3 | 2 | 1 |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 7 | 0 | 0 | 0 |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 15 | 8 | 0 | 8 |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 18 | 9 | 0 | 9 |
| `planner_summary_incremental_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 12 | 6 | 0 | 6 |