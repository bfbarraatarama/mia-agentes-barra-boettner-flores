# Análisis de consumo y eficiencia — M3

**Run:** `m3-final-run-004`

## summary_incremental_token_trigger / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.1 | 0.0 | 13.7 | 12.6 | 12.6 | 44,503 | 1,186 | 45,689 |
| color-locks | 10 | 2.3 | 0.0 | 53.4 | 49.4 | 49.4 | 228,176 | 4,574 | 232,750 |
| apartment-keys | 10 | 1.1 | 0.0 | 25.0 | 24.5 | 24.5 | 70,889 | 1,498 | 72,387 |
| library-search | 10 | 1.3 | 0.0 | 41.9 | 37.8 | 37.8 | 204,599 | 5,928 | 210,527 |
| office-sequence | 10 | 1.2 | 0.0 | 47.2 | 47.4 | 47.4 | 162,577 | 2,540 | 165,116 |
| extreme-archive | 10 | 1.9 | 0.0 | 78.9 | 75.4 | 75.4 | 405,445 | 7,946 | 413,391 |
| vault-combination | 10 | 1.7 | 0.0 | 62.5 | 63.6 | 63.6 | 244,577 | 4,004 | 248,581 |
| backtracking-vault | 10 | 1.2 | 0.0 | 40.5 | 39.8 | 39.8 | 133,501 | 2,604 | 136,105 |
| **Global** | 80 | 1.5 | 0.0 | 45.4 | 43.8 | 43.8 | 186,783 | 3,785 | 190,568 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 9 | 90% | 1.2 | 50,766 | 15.2 | 14.0 | 14.0 |
| color-locks | 10 | 6 | 60% | 3.8 | 387,917 | 89.0 | 82.3 | 82.3 |
| apartment-keys | 10 | 9 | 90% | 1.2 | 80,430 | 27.8 | 27.2 | 27.2 |
| library-search | 10 | 8 | 80% | 1.6 | 263,159 | 52.4 | 47.2 | 47.2 |
| office-sequence | 10 | 8 | 80% | 1.5 | 206,396 | 59.0 | 59.2 | 59.2 |
| extreme-archive | 10 | 1 | 10% | 19.0 | 4,133,910 | 789.0 | 754.0 | 754.0 |
| vault-combination | 10 | 4 | 40% | 4.2 | 621,452 | 156.2 | 159.0 | 159.0 |
| backtracking-vault | 10 | 8 | 80% | 1.5 | 170,131 | 50.6 | 49.8 | 49.8 |
| **Global** | 80 | 53 | 66% | 2.2 | 287,650 | 68.5 | 66.1 | 66.1 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 44.0 | 180,281 | 2,942 | 183,222 |
| history_compaction | 1.4 | 6,490 | 842 | 7,332 |
| tool_call_repair | 0.0 | 13 | 1 | 14 |
| **Total** | 45.4 | 186,783 | 3,785 | 190,568 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 8.4 | 0.0 | 1.5 | 0.9 | 1.8 | 12.6 |
| color-locks | 30.0 | 0.0 | 3.9 | 3.3 | 12.2 | 49.4 |
| apartment-keys | 1.3 | 14.4 | 4.6 | 1.0 | 3.2 | 24.5 |
| library-search | 27.5 | 0.0 | 3.2 | 3.4 | 3.7 | 37.8 |
| office-sequence | 4.5 | 24.1 | 13.2 | 3.0 | 2.6 | 47.4 |
| extreme-archive | 72.2 | 0.0 | 2.8 | 0.1 | 0.3 | 75.4 |
| vault-combination | 5.6 | 26.0 | 19.1 | 4.4 | 8.5 | 63.6 |
| backtracking-vault | 9.5 | 17.7 | 4.3 | 3.6 | 4.7 | 39.8 |
| **Global** | 19.9 | 10.3 | 6.6 | 2.5 | 4.6 | 43.8 |

## planner_summary_incremental_token_trigger / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 8.8 | 5.8 | 5.8 | 11,265 | 558 | 11,822 |
| color-locks | 10 | 2.3 | 0.0 | 50.2 | 45.6 | 45.6 | 198,454 | 3,712 | 202,166 |
| apartment-keys | 10 | 1.2 | 0.0 | 29.2 | 26.5 | 26.5 | 80,580 | 1,860 | 82,440 |
| library-search | 10 | 2.2 | 0.0 | 32.6 | 29.3 | 29.3 | 141,071 | 2,946 | 144,017 |
| office-sequence | 10 | 2.8 | 0.0 | 37.4 | 34.7 | 34.7 | 113,414 | 2,204 | 115,619 |
| extreme-archive | 10 | 3.8 | 0.1 | 89.2 | 84.1 | 84.1 | 452,422 | 9,020 | 461,442 |
| vault-combination | 10 | 1.9 | 0.0 | 77.5 | 77.5 | 77.5 | 317,437 | 5,780 | 323,217 |
| backtracking-vault | 10 | 2.7 | 0.1 | 70.8 | 65.9 | 65.9 | 294,514 | 5,230 | 299,745 |
| **Global** | 80 | 2.2 | 0.0 | 49.5 | 46.2 | 46.2 | 201,145 | 3,914 | 205,059 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 11,822 | 8.8 | 5.8 | 5.8 |
| color-locks | 10 | 6 | 60% | 3.8 | 336,944 | 83.7 | 76.0 | 76.0 |
| apartment-keys | 10 | 8 | 80% | 1.5 | 103,050 | 36.5 | 33.1 | 33.1 |
| library-search | 10 | 6 | 60% | 3.7 | 240,029 | 54.3 | 48.8 | 48.8 |
| office-sequence | 10 | 8 | 80% | 3.5 | 144,524 | 46.8 | 43.4 | 43.4 |
| extreme-archive | 10 | 1 | 10% | 38.0 | 4,614,422 | 892.0 | 841.0 | 841.0 |
| vault-combination | 10 | 1 | 10% | 19.0 | 3,232,171 | 775.0 | 775.0 | 775.0 |
| backtracking-vault | 10 | 3 | 30% | 9.0 | 999,149 | 236.0 | 219.7 | 219.7 |
| **Global** | 80 | 43 | 54% | 4.2 | 381,504 | 92.0 | 85.9 | 85.9 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 46.1 | 194,075 | 2,977 | 197,052 |
| history_compaction | 1.2 | 4,911 | 676 | 5,587 |
| planning | 2.1 | 2,159 | 261 | 2,420 |
| **Total** | 49.5 | 201,145 | 3,914 | 205,059 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.8 | 0.0 | 1.1 | 1.0 | 1.9 | 5.8 |
| color-locks | 17.0 | 0.0 | 11.2 | 3.5 | 13.9 | 45.6 |
| apartment-keys | 1.1 | 19.3 | 3.7 | 1.0 | 1.4 | 26.5 |
| library-search | 23.0 | 0.0 | 3.1 | 1.5 | 1.7 | 29.3 |
| office-sequence | 2.2 | 19.5 | 7.6 | 3.3 | 2.1 | 34.7 |
| extreme-archive | 73.5 | 0.0 | 3.5 | 7.0 | 0.1 | 84.1 |
| vault-combination | 13.4 | 43.5 | 14.8 | 2.5 | 3.3 | 77.5 |
| backtracking-vault | 14.4 | 21.1 | 22.1 | 4.0 | 4.3 | 65.9 |
| **Global** | 18.3 | 12.9 | 8.4 | 3.0 | 3.6 | 46.2 |
