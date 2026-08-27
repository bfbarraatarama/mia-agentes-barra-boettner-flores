# Análisis de consumo y eficiencia — M3

**Run:** `m3-final-run-005`

## summary_incremental_strategic / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 6.2 | 5.2 | 5.2 | 7,899 | 341 | 8,240 |
| color-locks | 10 | 1.0 | 0.0 | 21.5 | 19.1 | 19.1 | 40,779 | 1,881 | 42,660 |
| apartment-keys | 10 | 1.1 | 0.1 | 19.0 | 16.5 | 16.5 | 36,190 | 1,260 | 37,449 |
| library-search | 10 | 2.3 | 0.1 | 49.2 | 45.0 | 45.0 | 158,630 | 5,673 | 164,303 |
| office-sequence | 10 | 3.1 | 0.0 | 62.3 | 65.1 | 65.1 | 162,087 | 9,289 | 171,376 |
| extreme-archive | 10 | 2.7 | 0.0 | 82.0 | 76.1 | 76.1 | 335,267 | 11,501 | 346,768 |
| vault-combination | 10 | 2.1 | 0.0 | 92.6 | 85.8 | 85.8 | 229,815 | 9,126 | 238,941 |
| backtracking-vault | 10 | 2.7 | 0.2 | 81.6 | 73.8 | 73.8 | 202,771 | 7,479 | 210,250 |
| **Global** | 80 | 2.0 | 0.1 | 51.8 | 48.3 | 48.3 | 146,680 | 5,819 | 152,498 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 8,240 | 6.2 | 5.2 | 5.2 |
| color-locks | 10 | 10 | 100% | 1.0 | 42,660 | 21.5 | 19.1 | 19.1 |
| apartment-keys | 10 | 10 | 100% | 1.1 | 37,449 | 19.0 | 16.5 | 16.5 |
| library-search | 10 | 7 | 70% | 3.3 | 234,719 | 70.3 | 64.3 | 64.3 |
| office-sequence | 10 | 5 | 50% | 6.2 | 342,751 | 124.6 | 130.2 | 130.2 |
| extreme-archive | 10 | 1 | 10% | 27.0 | 3,467,681 | 820.0 | 761.0 | 761.0 |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 2 | 20% | 13.5 | 1,051,248 | 408.0 | 369.0 | 369.0 |
| **Global** | 80 | 45 | 56% | 3.6 | 271,108 | 92.1 | 85.9 | 85.9 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 46.8 | 130,133 | 3,723 | 133,856 |
| history_compaction | 5.0 | 16,546 | 2,096 | 18,642 |
| **Total** | 51.8 | 146,680 | 5,819 | 152,498 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.4 | 0.0 | 1.0 | 1.0 | 1.8 | 5.2 |
| color-locks | 6.8 | 0.0 | 1.2 | 5.0 | 6.1 | 19.1 |
| apartment-keys | 1.2 | 9.4 | 3.5 | 1.0 | 1.4 | 16.5 |
| library-search | 35.9 | 0.0 | 4.4 | 1.7 | 3.0 | 45.0 |
| office-sequence | 4.5 | 32.7 | 21.7 | 3.4 | 2.8 | 65.1 |
| extreme-archive | 68.6 | 0.0 | 7.3 | 0.1 | 0.1 | 76.1 |
| vault-combination | 14.6 | 30.8 | 33.5 | 2.5 | 4.4 | 85.8 |
| backtracking-vault | 23.2 | 20.7 | 21.0 | 3.1 | 5.8 | 73.8 |
| **Global** | 19.5 | 11.7 | 11.7 | 2.2 | 3.2 | 48.3 |

## planner_summary_incremental_strategic / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 8.6 | 5.6 | 5.6 | 10,973 | 545 | 11,517 |
| color-locks | 10 | 1.1 | 0.0 | 30.2 | 26.1 | 26.1 | 63,634 | 3,073 | 66,707 |
| apartment-keys | 10 | 1.1 | 0.0 | 20.9 | 17.2 | 17.2 | 37,278 | 1,664 | 38,943 |
| library-search | 10 | 1.2 | 0.0 | 38.8 | 33.4 | 33.4 | 105,226 | 3,844 | 109,070 |
| office-sequence | 10 | 1.3 | 0.0 | 57.6 | 51.7 | 51.7 | 132,374 | 5,322 | 137,696 |
| extreme-archive | 10 | 2.0 | 0.0 | 91.0 | 81.7 | 81.7 | 339,246 | 11,282 | 350,528 |
| vault-combination | 10 | 2.0 | 0.0 | 91.6 | 85.6 | 85.6 | 238,737 | 8,470 | 247,208 |
| backtracking-vault | 10 | 2.0 | 0.0 | 89.4 | 90.0 | 90.0 | 242,552 | 9,436 | 251,989 |
| **Global** | 80 | 1.5 | 0.0 | 53.5 | 48.9 | 48.9 | 146,253 | 5,455 | 151,707 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 11,517 | 8.6 | 5.6 | 5.6 |
| color-locks | 10 | 9 | 90% | 1.2 | 74,119 | 33.6 | 29.0 | 29.0 |
| apartment-keys | 10 | 10 | 100% | 1.1 | 38,943 | 20.9 | 17.2 | 17.2 |
| library-search | 10 | 8 | 80% | 1.5 | 136,337 | 48.5 | 41.8 | 41.8 |
| office-sequence | 10 | 7 | 70% | 1.9 | 196,709 | 82.3 | 73.9 | 73.9 |
| extreme-archive | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 1 | 10% | 20.0 | 2,519,889 | 894.0 | 900.0 | 900.0 |
| **Global** | 80 | 45 | 56% | 2.6 | 269,702 | 95.1 | 87.0 | 87.0 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 46.5 | 128,848 | 3,152 | 132,000 |
| history_compaction | 5.0 | 15,277 | 2,041 | 17,319 |
| planning | 2.1 | 2,127 | 262 | 2,389 |
| **Total** | 53.5 | 146,253 | 5,455 | 151,707 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.4 | 0.0 | 1.2 | 1.0 | 2.0 | 5.6 |
| color-locks | 15.0 | 0.0 | 1.5 | 4.2 | 5.4 | 26.1 |
| apartment-keys | 1.5 | 6.7 | 6.0 | 1.0 | 2.0 | 17.2 |
| library-search | 26.4 | 0.0 | 2.7 | 2.2 | 2.1 | 33.4 |
| office-sequence | 9.3 | 21.1 | 14.4 | 3.9 | 3.0 | 51.7 |
| extreme-archive | 77.4 | 0.0 | 4.0 | 0.0 | 0.3 | 81.7 |
| vault-combination | 12.1 | 38.4 | 23.8 | 4.0 | 7.3 | 85.6 |
| backtracking-vault | 30.7 | 17.8 | 32.1 | 2.6 | 6.8 | 90.0 |
| **Global** | 21.7 | 10.5 | 10.7 | 2.4 | 3.6 | 48.9 |
