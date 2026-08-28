# Análisis de recuperación entre attempts — M3

**Runs:** `m3-final-run-002`, `m3-final-run-003`

Sólo se incluyen condiciones cuyo manifest declara una política `recoverable_attempt_terminations`.

**Trials ignorados sin política de recovery:** 0

## Resumen

| Métrica | Valor |
|---|---:|
| Trials analizados | 640 |
| Trials con terminación estructurada | 314 |
| Eventos de terminación | 697 |
| Eventos configurados como recuperables | 697 |
| Eventos con goal ya cumplido | 60 |
| Recuperaciones que abrieron otro attempt | 453 |
| Trials con recuperación | 275 |
| Trials recuperados con éxito final | 60 |
| Trials recuperados con fallo final | 215 |
| Éxito final entre trials recuperados | 21.8% |
| Eventos recuperables sin siguiente attempt | 184 |
| Terminaciones fatales no configuradas | 0 |
| Recuperaciones inesperadas | 0 |
| Trials con múltiples terminaciones | 232 |

## Por causa

| Causa | Eventos | Trials | Recuperaciones | Trials recuperados | Éxito final | Fallo final | Goal ya cumplido | Sin siguiente attempt | Repetición |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `context_overflow` | 248 | 134 | 227 | 127 | 41 | 86 | 20 | 1 | 66 |
| `max_iterations` | 449 | 260 | 226 | 226 | 27 | 199 | 40 | 183 | 189 |

## Por sistema y configuración de trial

| Agente | Modelo | Trial config | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos | Éxito tras recovery |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `baseline` | `nova-lite` | `multi_attempt_recovery` | 80 | 55 | 24 | 1 | 23 | 4.2% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | 80 | 39 | 16 | 2 | 13 | 13.3% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | 80 | 123 | 93 | 13 | 35 | 27.1% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | 80 | 125 | 92 | 17 | 30 | 36.2% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | 80 | 57 | 27 | 2 | 23 | 8.0% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | 80 | 52 | 25 | 3 | 22 | 12.0% |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | 80 | 125 | 91 | 14 | 31 | 31.1% |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | 80 | 121 | 85 | 8 | 38 | 17.4% |

## Por caso

| Agente | Modelo | Trial config | Escenario | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos |
|---|---|---|---|---:|---:|---:|---:|---:|
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 10 | 5 | 0 | 5 |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 4 | 1 | 0 | 1 |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 14 | 7 | 0 | 7 |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 9 | 2 | 1 | 1 |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 2 | 1 | 0 | 1 |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 6 | 3 | 0 | 3 |
| `baseline` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 10 | 5 | 0 | 5 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 0 | 0 | 0 | 0 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 1 | 0 | 0 | 0 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 2 | 1 | 0 | 1 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 9 | 1 | 0 | 1 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 0 | 0 | 0 | 0 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 15 | 8 | 2 | 5 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 12 | 6 | 0 | 6 |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 5 | 4 | 2 | 1 |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 5 | 3 | 2 | 0 |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 10 | 6 | 3 | 3 |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 19 | 16 | 4 | 4 |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 21 | 15 | 0 | 9 |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 33 | 25 | 0 | 10 |
| `summary` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 30 | 24 | 2 | 8 |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 9 | 8 | 4 | 0 |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 6 | 5 | 3 | 0 |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 4 | 3 | 3 | 0 |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 24 | 17 | 5 | 4 |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 20 | 12 | 0 | 9 |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 38 | 31 | 1 | 9 |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 24 | 16 | 1 | 8 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 3 | 1 | 0 | 1 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 0 | 0 | 0 | 0 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 9 | 5 | 1 | 4 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 13 | 4 | 0 | 4 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 8 | 4 | 0 | 4 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 15 | 9 | 1 | 6 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 9 | 4 | 0 | 4 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 7 | 4 | 1 | 3 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 2 | 1 | 0 | 1 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 5 | 3 | 1 | 2 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 10 | 3 | 1 | 2 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 6 | 3 | 0 | 3 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 12 | 6 | 0 | 6 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 10 | 5 | 0 | 5 |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 8 | 7 | 4 | 0 |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 2 | 1 | 1 | 0 |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 8 | 6 | 3 | 2 |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 21 | 14 | 4 | 4 |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 20 | 12 | 0 | 8 |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 42 | 33 | 1 | 9 |
| `summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 24 | 18 | 1 | 8 |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 6 | 5 | 2 | 2 |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 0 | 0 | 0 | 0 |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 11 | 7 | 2 | 4 |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 18 | 9 | 3 | 3 |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 20 | 12 | 0 | 10 |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 35 | 27 | 0 | 10 |
| `planner_summary_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 31 | 25 | 1 | 9 |