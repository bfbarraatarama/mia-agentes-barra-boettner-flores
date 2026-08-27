# Evaluación cualitativa por sistema

- Dataset: `m3-final-selection-qualitative-v1`
- Judge evaluation: `m3-final-selection-judge-001`

| Sistema | Casos | Q1.1 | Q1.2 | Q1.3 | Q1.4 |
|---|---:|---:|---:|---:|---:|
| `baseline_incremental / nova-lite / multi_attempt_recovery` | 24 | 18/24 (75.0%) | 20/24 (83.3%) | 14/24 (58.3%) | 10/21 (47.6%) |
| `planner / nova-lite / multi_attempt_recovery` | 24 | 19/24 (79.2%) | 20/24 (83.3%) | 16/24 (66.7%) | 9/18 (50.0%) |
| `planner_incremental / nova-lite / multi_attempt_recovery` | 24 | 17/24 (70.8%) | 19/24 (79.2%) | 16/24 (66.7%) | 13/21 (61.9%) |

Cada celda muestra `PASS/aplicables` y su proporción. Q1.4 puede tener un denominador menor porque sólo se evalúa cuando existe una oportunidad observable de adaptación.
