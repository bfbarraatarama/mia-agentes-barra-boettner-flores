# Análisis de consumo y eficiencia — M3

**Runs:** `m3-final-run-006`, `m3-final-run-007`

## summary_token_trigger / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 5.9 | 4.9 | 4.9 | 6,240 | 304 | 6,544 |
| color-locks | 10 | 2.4 | 0.0 | 53.2 | 51.1 | 51.1 | 215,237 | 3,728 | 218,965 |
| apartment-keys | 10 | 1.2 | 0.0 | 27.3 | 27.2 | 27.2 | 76,990 | 1,743 | 78,733 |
| library-search | 10 | 1.3 | 0.0 | 38.2 | 37.7 | 37.7 | 144,726 | 2,623 | 147,348 |
| office-sequence | 10 | 2.0 | 0.0 | 49.3 | 72.6 | 72.6 | 152,269 | 2,917 | 155,186 |
| extreme-archive | 10 | 3.6 | 0.0 | 85.7 | 91.5 | 91.5 | 433,939 | 9,784 | 443,723 |
| vault-combination | 10 | 2.3 | 0.0 | 51.6 | 55.1 | 55.1 | 190,036 | 3,875 | 193,911 |
| backtracking-vault | 10 | 1.2 | 0.0 | 42.9 | 42.7 | 42.7 | 136,402 | 2,370 | 138,772 |
| **Global** | 80 | 1.9 | 0.0 | 44.3 | 47.9 | 47.9 | 169,480 | 3,418 | 172,898 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 6,544 | 5.9 | 4.9 | 4.9 |
| color-locks | 10 | 4 | 40% | 6.0 | 547,414 | 133.0 | 127.8 | 127.8 |
| apartment-keys | 10 | 8 | 80% | 1.5 | 98,416 | 34.1 | 34.0 | 34.0 |
| library-search | 10 | 7 | 70% | 1.9 | 210,498 | 54.6 | 53.9 | 53.9 |
| office-sequence | 10 | 8 | 80% | 2.5 | 193,983 | 61.6 | 90.8 | 90.8 |
| extreme-archive | 10 | 1 | 10% | 36.0 | 4,437,230 | 857.0 | 915.0 | 915.0 |
| vault-combination | 10 | 5 | 50% | 4.6 | 387,822 | 103.2 | 110.2 | 110.2 |
| backtracking-vault | 10 | 8 | 80% | 1.5 | 173,465 | 53.6 | 53.4 | 53.4 |
| **Global** | 80 | 51 | 64% | 2.9 | 271,212 | 69.4 | 75.1 | 75.1 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 43.2 | 165,902 | 2,762 | 168,664 |
| history_compaction | 1.0 | 3,577 | 657 | 4,234 |
| **Total** | 44.3 | 169,480 | 3,418 | 172,898 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.0 | 0.0 | 1.1 | 1.0 | 1.8 | 4.9 |
| color-locks | 15.6 | 0.0 | 13.4 | 2.7 | 19.4 | 51.1 |
| apartment-keys | 1.2 | 17.6 | 3.2 | 0.9 | 4.3 | 27.2 |
| library-search | 18.3 | 0.0 | 1.1 | 9.2 | 9.1 | 37.7 |
| office-sequence | 8.1 | 37.8 | 9.1 | 8.5 | 9.1 | 72.6 |
| extreme-archive | 88.6 | 0.0 | 1.5 | 1.2 | 0.2 | 91.5 |
| vault-combination | 3.9 | 13.0 | 11.9 | 3.9 | 22.4 | 55.1 |
| backtracking-vault | 7.9 | 14.3 | 9.3 | 4.0 | 7.2 | 42.7 |
| **Global** | 18.1 | 10.3 | 6.3 | 3.9 | 9.2 | 47.9 |

## planner_summary_token_trigger / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 8.3 | 6.3 | 6.3 | 9,746 | 532 | 10,278 |
| color-locks | 10 | 1.6 | 0.0 | 52.1 | 65.6 | 65.6 | 210,147 | 4,983 | 215,130 |
| apartment-keys | 10 | 1.0 | 0.0 | 14.9 | 13.7 | 13.7 | 24,345 | 837 | 25,182 |
| library-search | 10 | 1.7 | 0.0 | 45.2 | 44.9 | 44.9 | 211,304 | 4,966 | 216,270 |
| office-sequence | 10 | 2.2 | 0.0 | 51.1 | 49.8 | 49.8 | 172,280 | 3,012 | 175,292 |
| extreme-archive | 10 | 4.3 | 0.0 | 70.5 | 64.8 | 64.8 | 337,649 | 7,394 | 345,043 |
| vault-combination | 10 | 1.9 | 0.0 | 76.1 | 80.5 | 80.5 | 312,869 | 5,569 | 318,438 |
| backtracking-vault | 10 | 1.4 | 0.0 | 53.8 | 52.1 | 52.1 | 188,418 | 3,303 | 191,721 |
| **Global** | 80 | 1.9 | 0.0 | 46.5 | 47.2 | 47.2 | 183,345 | 3,824 | 187,169 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 10,278 | 8.3 | 6.3 | 6.3 |
| color-locks | 10 | 5 | 50% | 3.2 | 430,259 | 104.2 | 131.2 | 131.2 |
| apartment-keys | 10 | 10 | 100% | 1.0 | 25,182 | 14.9 | 13.7 | 13.7 |
| library-search | 10 | 7 | 70% | 2.4 | 308,958 | 64.6 | 64.1 | 64.1 |
| office-sequence | 10 | 6 | 60% | 3.7 | 292,152 | 85.2 | 83.0 | 83.0 |
| extreme-archive | 10 | 1 | 10% | 43.0 | 3,450,434 | 705.0 | 648.0 | 648.0 |
| vault-combination | 10 | 2 | 20% | 9.5 | 1,592,188 | 380.5 | 402.5 | 402.5 |
| backtracking-vault | 10 | 6 | 60% | 2.3 | 319,534 | 89.7 | 86.8 | 86.8 |
| **Global** | 80 | 47 | 59% | 3.2 | 318,586 | 79.2 | 80.4 | 80.4 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 44.4 | 177,495 | 2,842 | 180,337 |
| history_compaction | 1.1 | 5,169 | 806 | 5,975 |
| planning | 1.0 | 681 | 177 | 858 |
| **Total** | 46.5 | 183,345 | 3,824 | 187,169 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 2.0 | 0.0 | 1.2 | 1.0 | 2.1 | 6.3 |
| color-locks | 31.7 | 0.0 | 9.2 | 4.3 | 20.4 | 65.6 |
| apartment-keys | 1.1 | 6.0 | 3.5 | 1.1 | 2.0 | 13.7 |
| library-search | 22.0 | 0.0 | 8.1 | 2.3 | 12.5 | 44.9 |
| office-sequence | 3.6 | 25.7 | 14.5 | 2.5 | 3.5 | 49.8 |
| extreme-archive | 59.2 | 0.0 | 5.2 | 0.3 | 0.1 | 64.8 |
| vault-combination | 7.5 | 27.5 | 34.1 | 3.3 | 8.1 | 80.5 |
| backtracking-vault | 10.1 | 17.3 | 9.7 | 7.4 | 7.6 | 52.1 |
| **Global** | 17.1 | 9.6 | 10.7 | 2.8 | 7.0 | 47.2 |

## summary_strategic / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 6.4 | 5.3 | 5.3 | 7,142 | 380 | 7,522 |
| color-locks | 10 | 1.4 | 0.0 | 47.1 | 46.1 | 46.1 | 125,034 | 5,249 | 130,283 |
| apartment-keys | 10 | 1.0 | 0.0 | 14.7 | 12.9 | 12.9 | 21,719 | 1,065 | 22,783 |
| library-search | 10 | 3.5 | 0.0 | 56.3 | 51.5 | 51.5 | 186,745 | 9,740 | 196,485 |
| office-sequence | 10 | 2.0 | 0.0 | 47.8 | 44.2 | 44.2 | 97,943 | 4,133 | 102,076 |
| extreme-archive | 10 | 3.5 | 0.0 | 64.1 | 62.4 | 62.4 | 230,556 | 11,266 | 241,822 |
| vault-combination | 10 | 3.6 | 0.0 | 82.4 | 74.1 | 74.1 | 196,972 | 7,680 | 204,651 |
| backtracking-vault | 10 | 1.8 | 0.0 | 78.0 | 71.5 | 71.5 | 192,625 | 7,273 | 199,898 |
| **Global** | 80 | 2.2 | 0.0 | 49.6 | 46.0 | 46.0 | 132,342 | 5,848 | 138,190 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 7,522 | 6.4 | 5.3 | 5.3 |
| color-locks | 10 | 8 | 80% | 1.8 | 162,854 | 58.9 | 57.6 | 57.6 |
| apartment-keys | 10 | 10 | 100% | 1.0 | 22,783 | 14.7 | 12.9 | 12.9 |
| library-search | 10 | 5 | 50% | 7.0 | 392,971 | 112.6 | 103.0 | 103.0 |
| office-sequence | 10 | 8 | 80% | 2.5 | 127,596 | 59.8 | 55.2 | 55.2 |
| extreme-archive | 10 | 4 | 40% | 8.8 | 604,555 | 160.2 | 156.0 | 156.0 |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 2 | 20% | 9.0 | 999,490 | 390.0 | 357.5 | 357.5 |
| **Global** | 80 | 47 | 59% | 3.8 | 235,217 | 84.4 | 78.3 | 78.3 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 44.6 | 119,237 | 3,768 | 123,005 |
| history_compaction | 5.0 | 13,105 | 2,080 | 15,185 |
| **Total** | 49.6 | 132,342 | 5,848 | 138,190 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.3 | 0.0 | 1.2 | 1.0 | 1.8 | 5.3 |
| color-locks | 19.6 | 0.0 | 4.1 | 4.1 | 18.3 | 46.1 |
| apartment-keys | 1.3 | 5.5 | 3.3 | 1.0 | 1.8 | 12.9 |
| library-search | 42.9 | 0.0 | 1.9 | 2.9 | 3.8 | 51.5 |
| office-sequence | 3.5 | 22.4 | 8.7 | 5.8 | 3.8 | 44.2 |
| extreme-archive | 58.3 | 0.0 | 3.0 | 0.6 | 0.5 | 62.4 |
| vault-combination | 17.6 | 22.8 | 21.0 | 4.7 | 8.0 | 74.1 |
| backtracking-vault | 21.2 | 17.4 | 22.4 | 2.8 | 7.7 | 71.5 |
| **Global** | 20.7 | 8.5 | 8.2 | 2.9 | 5.7 | 46.0 |

## planner_summary_strategic / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 6.9 | 5.4 | 5.4 | 7,482 | 457 | 7,939 |
| color-locks | 10 | 2.2 | 0.0 | 43.8 | 42.7 | 42.7 | 116,187 | 4,789 | 120,975 |
| apartment-keys | 10 | 2.0 | 0.0 | 33.9 | 29.6 | 29.6 | 69,985 | 2,625 | 72,609 |
| library-search | 10 | 3.0 | 0.0 | 47.2 | 44.7 | 44.7 | 142,005 | 4,593 | 146,598 |
| office-sequence | 10 | 1.2 | 0.0 | 54.4 | 49.3 | 49.3 | 125,179 | 4,845 | 130,023 |
| extreme-archive | 10 | 2.0 | 0.0 | 83.4 | 82.5 | 82.5 | 286,564 | 10,444 | 297,008 |
| vault-combination | 10 | 2.0 | 0.0 | 89.7 | 82.5 | 82.5 | 228,085 | 8,780 | 236,865 |
| backtracking-vault | 10 | 1.9 | 0.0 | 84.0 | 78.5 | 78.5 | 203,458 | 7,405 | 210,863 |
| **Global** | 80 | 1.9 | 0.0 | 55.4 | 51.9 | 51.9 | 147,368 | 5,492 | 152,860 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 7,939 | 6.9 | 5.4 | 5.4 |
| color-locks | 10 | 7 | 70% | 3.1 | 172,822 | 62.6 | 61.0 | 61.0 |
| apartment-keys | 10 | 8 | 80% | 2.5 | 90,762 | 42.4 | 37.0 | 37.0 |
| library-search | 10 | 8 | 80% | 3.8 | 183,248 | 59.0 | 55.9 | 55.9 |
| office-sequence | 10 | 9 | 90% | 1.3 | 144,470 | 60.4 | 54.8 | 54.8 |
| extreme-archive | 10 | 2 | 20% | 10.0 | 1,485,040 | 417.0 | 412.5 | 412.5 |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 1 | 10% | 19.0 | 2,108,632 | 840.0 | 785.0 | 785.0 |
| **Global** | 80 | 45 | 56% | 3.4 | 271,751 | 98.5 | 92.3 | 92.3 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 49.1 | 132,720 | 3,069 | 135,789 |
| history_compaction | 5.3 | 13,967 | 2,244 | 16,211 |
| planning | 1.0 | 681 | 180 | 861 |
| **Total** | 55.4 | 147,368 | 5,492 | 152,860 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.8 | 0.0 | 1.1 | 1.0 | 1.5 | 5.4 |
| color-locks | 15.1 | 0.0 | 4.9 | 4.6 | 18.1 | 42.7 |
| apartment-keys | 8.2 | 13.0 | 5.3 | 1.1 | 2.0 | 29.6 |
| library-search | 27.6 | 0.0 | 3.4 | 2.4 | 11.3 | 44.7 |
| office-sequence | 2.9 | 26.8 | 12.2 | 4.3 | 3.1 | 49.3 |
| extreme-archive | 79.5 | 0.0 | 2.5 | 0.2 | 0.3 | 82.5 |
| vault-combination | 11.3 | 35.0 | 27.1 | 3.8 | 5.3 | 82.5 |
| backtracking-vault | 16.3 | 27.4 | 24.5 | 3.4 | 6.9 | 78.5 |
| **Global** | 20.3 | 12.8 | 10.1 | 2.6 | 6.1 | 51.9 |
