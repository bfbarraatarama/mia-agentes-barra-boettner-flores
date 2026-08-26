# Análisis de recuperación entre attempts — M3

**Run:** `m3-final-run-005`

Sólo se incluyen condiciones cuyo manifest declara una política `recoverable_attempt_terminations`.

**Trials ignorados sin política de recovery:** 0

## Resumen

| Métrica | Valor |
|---|---:|
| Trials analizados | 160 |
| Trials con terminación estructurada | 84 |
| Eventos de terminación | 149 |
| Eventos configurados como recuperables | 149 |
| Eventos con goal ya cumplido | 13 |
| Recuperaciones que abrieron otro attempt | 72 |
| Trials con recuperación | 71 |
| Trials recuperados con éxito final | 5 |
| Trials recuperados con fallo final | 66 |
| Éxito final entre trials recuperados | 7.0% |
| Eventos recuperables sin siguiente attempt | 64 |
| Terminaciones fatales no configuradas | 0 |
| Recuperaciones inesperadas | 0 |
| Trials con múltiples terminaciones | 64 |

## Por causa

| Causa | Eventos | Trials | Recuperaciones | Trials recuperados | Éxito final | Fallo final | Goal ya cumplido | Sin siguiente attempt | Repetición |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `context_overflow` | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| `max_iterations` | 148 | 84 | 71 | 71 | 5 | 66 | 13 | 64 | 64 |

## Por sistema y configuración de trial

| Agente | Modelo | Trial config | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos | Éxito tras recovery |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | 80 | 72 | 36 | 4 | 32 | 11.1% |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | 80 | 77 | 36 | 1 | 34 | 2.9% |

## Por caso

| Agente | Modelo | Trial config | Escenario | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos |
|---|---|---|---|---:|---:|---:|---:|---:|
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 0 | 0 | 0 | 0 |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 1 | 1 | 1 | 0 |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 6 | 4 | 2 | 2 |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 12 | 4 | 0 | 4 |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 17 | 9 | 0 | 9 |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 20 | 10 | 0 | 10 |
| `summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 16 | 8 | 1 | 7 |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 2 | 1 | 0 | 1 |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 1 | 0 | 0 | 0 |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 3 | 2 | 1 | 1 |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 12 | 3 | 0 | 3 |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 20 | 10 | 0 | 10 |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 20 | 10 | 0 | 10 |
| `planner_summary_incremental_strategic` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 19 | 10 | 0 | 9 |