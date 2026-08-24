# Análisis de consumo y eficiencia — M3

**Run:** `m3-llm-judge-smoke-summary-run-001`

## minimal_summary / nova-lite / multi_attempt

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| office-sequence | 2 | 1.0 | 0.0 | 40.0 | 41.0 | 41.0 | 121,216 | 1,990 | 123,205 |
| **Global** | 2 | 1.0 | 0.0 | 40.0 | 41.0 | 41.0 | 121,216 | 1,990 | 123,205 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| office-sequence | 2 | 2 | 100% | 1.0 | 123,205 | 40.0 | 41.0 | 41.0 |
| **Global** | 2 | 2 | 100% | 1.0 | 123,205 | 40.0 | 41.0 | 41.0 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 40.0 | 121,216 | 1,990 | 123,205 |
| **Total** | 40.0 | 121,216 | 1,990 | 123,205 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| office-sequence | 2.5 | 18.0 | 13.5 | 4.5 | 2.5 | 41.0 |
| **Global** | 2.5 | 18.0 | 13.5 | 4.5 | 2.5 | 41.0 |
