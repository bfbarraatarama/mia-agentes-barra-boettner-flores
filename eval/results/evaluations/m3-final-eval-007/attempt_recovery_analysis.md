# Análisis de recuperación entre attempts — M3

**Runs:** `m3-final-run-006`, `m3-final-run-007`

Sólo se incluyen condiciones cuyo manifest declara una política `recoverable_attempt_terminations`.

**Trials ignorados sin política de recovery:** 0

## Resumen

| Métrica | Valor |
|---|---:|
| Trials analizados | 320 |
| Trials con terminación estructurada | 167 |
| Eventos de terminación | 281 |
| Eventos configurados como recuperables | 281 |
| Eventos con goal ya cumplido | 33 |
| Recuperaciones que abrieron otro attempt | 138 |
| Trials con recuperación | 135 |
| Trials recuperados con éxito final | 13 |
| Trials recuperados con fallo final | 122 |
| Éxito final entre trials recuperados | 9.6% |
| Eventos recuperables sin siguiente attempt | 110 |
| Terminaciones fatales no configuradas | 0 |
| Recuperaciones inesperadas | 0 |
| Trials con múltiples terminaciones | 112 |

## Por causa

| Causa | Eventos | Trials | Recuperaciones | Trials recuperados | Éxito final | Fallo final | Goal ya cumplido | Sin siguiente attempt | Repetición |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `context_overflow` | 3 | 3 | 3 | 3 | 0 | 3 | 0 | 0 | 0 |
| `max_iterations` | 278 | 167 | 135 | 135 | 13 | 122 | 33 | 110 | 111 |

## Por sistema y configuración de trial

| Agente | Modelo | Trial config | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos | Éxito tras recovery |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | 80 | 61 | 29 | 0 | 28 | 0.0% |
| `planner_summary_token_trigger` | `nova-lite` | `multi_attempt_recovery` | 80 | 68 | 32 | 1 | 30 | 3.2% |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | 80 | 70 | 36 | 6 | 29 | 17.1% |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | 80 | 82 | 41 | 6 | 35 | 14.6% |

## Por caso

| Agente | Modelo | Trial config | Escenario | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos |
|---|---|---|---|---:|---:|---:|---:|---:|
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
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 6 | 4 | 1 | 2 |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 0 | 0 | 0 | 0 |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 9 | 6 | 2 | 4 |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 10 | 1 | 0 | 1 |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 12 | 8 | 3 | 5 |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 17 | 9 | 0 | 9 |
| `summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 16 | 8 | 0 | 8 |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 10 | 0 | 0 | 0 | 0 |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 10 | 6 | 4 | 1 | 3 |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 10 | 4 | 2 | 0 | 2 |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 10 | 4 | 4 | 2 | 2 |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 10 | 12 | 2 | 1 | 1 |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 10 | 18 | 10 | 2 | 8 |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 10 | 20 | 10 | 0 | 10 |
| `planner_summary_strategic` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 10 | 18 | 9 | 0 | 9 |