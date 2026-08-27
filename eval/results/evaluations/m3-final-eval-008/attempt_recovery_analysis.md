# Análisis de recuperación entre attempts — M3

**Run:** `m3-final-run-008`

Sólo se incluyen condiciones cuyo manifest declara una política `recoverable_attempt_terminations`.

**Trials ignorados sin política de recovery:** 0

## Resumen

| Métrica | Valor |
|---|---:|
| Trials analizados | 480 |
| Trials con terminación estructurada | 194 |
| Eventos de terminación | 332 |
| Eventos configurados como recuperables | 332 |
| Eventos con goal ya cumplido | 48 |
| Recuperaciones que abrieron otro attempt | 157 |
| Trials con recuperación | 151 |
| Trials recuperados con éxito final | 22 |
| Trials recuperados con fallo final | 129 |
| Éxito final entre trials recuperados | 14.6% |
| Eventos recuperables sin siguiente attempt | 127 |
| Terminaciones fatales no configuradas | 0 |
| Recuperaciones inesperadas | 0 |
| Trials con múltiples terminaciones | 132 |

## Por causa

| Causa | Eventos | Trials | Recuperaciones | Trials recuperados | Éxito final | Fallo final | Goal ya cumplido | Sin siguiente attempt | Repetición |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `context_overflow` | 11 | 10 | 11 | 10 | 4 | 6 | 0 | 0 | 1 |
| `max_iterations` | 321 | 189 | 146 | 146 | 18 | 128 | 48 | 127 | 132 |

## Por sistema y configuración de trial

| Agente | Modelo | Trial config | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos | Éxito tras recovery |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `planner` | `nova-lite` | `multi_attempt_recovery` | 160 | 122 | 59 | 7 | 49 | 12.5% |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | 160 | 114 | 56 | 11 | 44 | 20.0% |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | 160 | 96 | 42 | 4 | 36 | 10.0% |

## Por caso

| Agente | Modelo | Trial config | Escenario | Trials | Terminaciones | Recuperaciones | Éxitos | Fallos |
|---|---|---|---|---:|---:|---:|---:|---:|
| `planner` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 20 | 0 | 0 | 0 | 0 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 20 | 16 | 9 | 1 | 8 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 20 | 9 | 4 | 0 | 4 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 20 | 7 | 5 | 3 | 2 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 20 | 27 | 7 | 1 | 6 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 20 | 1 | 1 | 1 | 0 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 20 | 36 | 19 | 1 | 17 |
| `planner` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 20 | 26 | 14 | 0 | 12 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 20 | 1 | 1 | 1 | 0 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 20 | 15 | 8 | 1 | 7 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 20 | 2 | 1 | 0 | 1 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 20 | 15 | 8 | 0 | 7 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 20 | 30 | 10 | 4 | 6 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 20 | 9 | 5 | 2 | 3 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 20 | 25 | 14 | 3 | 11 |
| `baseline_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 20 | 17 | 9 | 0 | 9 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `study-with-key` | 20 | 1 | 0 | 0 | 0 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `color-locks` | 20 | 11 | 6 | 1 | 5 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `apartment-keys` | 20 | 3 | 2 | 1 | 1 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `library-search` | 20 | 11 | 6 | 1 | 5 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `office-sequence` | 20 | 19 | 1 | 0 | 1 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `extreme-archive` | 20 | 6 | 3 | 0 | 3 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `vault-combination` | 20 | 28 | 15 | 1 | 13 |
| `planner_incremental` | `nova-lite` | `multi_attempt_recovery` | `backtracking-vault` | 20 | 17 | 9 | 0 | 8 |