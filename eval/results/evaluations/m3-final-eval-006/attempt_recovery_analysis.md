# Análisis de recuperación entre attempts — M3

**Runs:** `m3-final-run-002`, `m3-final-run-006`

Sólo se incluyen condiciones cuyo manifest declara una política `recoverable_attempt_terminations`.

**Trials ignorados sin política de recovery:** 0

## Resumen

| Métrica | Valor |
|---|---:|
| Trials analizados | 480 |
| Trials con terminación estructurada | 230 |
| Eventos de terminación | 471 |
| Eventos configurados como recuperables | 471 |
| Eventos con goal ya cumplido | 47 |
| Recuperaciones que abrieron otro attempt | 286 |
| Trials con recuperación | 193 |
| Trials recuperados con éxito final | 34 |
| Trials recuperados con fallo final | 159 |
| Éxito final entre trials recuperados | 17.6% |
| Eventos recuperables sin siguiente attempt | 138 |
| Terminaciones fatales no configuradas | 0 |
| Recuperaciones inesperadas | 0 |
| Trials con múltiples terminaciones | 167 |

## Por causa

| Causa | Eventos | Trials | Recuperaciones | Trials recuperados | Éxito final | Fallo final | Goal ya cumplido | Sin siguiente attempt | Repetición |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `context_overflow` | 130 | 69 | 121 | 67 | 26 | 41 | 8 | 1 | 36 |
| `max_iterations` | 341 | 201 | 165 | 165 | 14 | 151 | 39 | 137 | 140 |

## Por sistema y configuración de trial

| Agente | Modelo | Trial config | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos | Éxito tras recovery |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `baseline` | `nova-lite` | `multi_attempt_recovery` | 80 | 55 | 24 | 1 | 23 | 4.2% |
| `planner` | `nova-lite` | `multi_attempt_recovery` | 80 | 39 | 16 | 2 | 13 | 13.3% |
| `summary` | `nova-lite` | `multi_attempt_recovery` | 80 | 123 | 93 | 13 | 35 | 27.1% |
| `planner_summary` | `nova-lite` | `multi_attempt_recovery` | 80 | 125 | 92 | 17 | 30 | 36.2% |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | 80 | 61 | 29 | 0 | 28 | 0.0% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | 80 | 68 | 32 | 1 | 30 | 3.2% |

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
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 10 | 5 | 0 | 5 |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 4 | 2 | 0 | 2 |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 6 | 3 | 0 | 3 |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 12 | 3 | 0 | 2 |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 16 | 9 | 0 | 9 |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 9 | 5 | 0 | 5 |
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 4 | 2 | 0 | 2 |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 10 | 5 | 0 | 5 |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 0 | 0 | 0 | 0 |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 7 | 4 | 1 | 3 |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 11 | 3 | 0 | 3 |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 13 | 7 | 0 | 7 |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 18 | 9 | 0 | 8 |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 9 | 4 | 0 | 4 |