# Análisis de consumo y eficiencia — M3

**Runs:** `m3-final-run-002`, `m3-final-run-006`

## baseline / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 6.0 | 5.0 | 5.0 | 6,394 | 312 | 6,705 |
| color-locks | 10 | 3.3 | 0.0 | 59.2 | 59.5 | 59.5 | 286,098 | 4,619 | 290,717 |
| apartment-keys | 10 | 1.1 | 0.0 | 25.6 | 25.0 | 25.0 | 62,482 | 1,297 | 63,779 |
| library-search | 10 | 1.7 | 0.0 | 60.5 | 61.5 | 61.5 | 453,379 | 5,582 | 458,960 |
| office-sequence | 10 | 2.2 | 0.0 | 43.0 | 42.3 | 42.3 | 123,849 | 2,036 | 125,885 |
| extreme-archive | 10 | 1.1 | 0.0 | 28.0 | 31.3 | 31.3 | 199,264 | 1,959 | 201,223 |
| vault-combination | 10 | 1.3 | 0.0 | 43.6 | 46.9 | 46.9 | 151,993 | 2,803 | 154,796 |
| backtracking-vault | 10 | 1.5 | 0.0 | 55.5 | 56.5 | 56.5 | 194,553 | 2,910 | 197,463 |
| **Global** | 80 | 1.6 | 0.0 | 40.2 | 41.0 | 41.0 | 184,751 | 2,690 | 187,441 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 6,705 | 6.0 | 5.0 | 5.0 |
| color-locks | 10 | 3 | 30% | 11.0 | 969,055 | 197.3 | 198.3 | 198.3 |
| apartment-keys | 10 | 9 | 90% | 1.2 | 70,865 | 28.4 | 27.8 | 27.8 |
| library-search | 10 | 3 | 30% | 5.7 | 1,529,868 | 201.7 | 205.0 | 205.0 |
| office-sequence | 10 | 8 | 80% | 2.8 | 157,356 | 53.8 | 52.9 | 52.9 |
| extreme-archive | 10 | 9 | 90% | 1.2 | 223,581 | 31.1 | 34.8 | 34.8 |
| vault-combination | 10 | 7 | 70% | 1.9 | 221,138 | 62.3 | 67.0 | 67.0 |
| backtracking-vault | 10 | 5 | 50% | 3.0 | 394,927 | 111.0 | 113.0 | 113.0 |
| **Global** | 80 | 54 | 68% | 2.4 | 277,691 | 59.5 | 60.7 | 60.7 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 40.2 | 184,751 | 2,690 | 187,441 |
| **Total** | 40.2 | 184,751 | 2,690 | 187,441 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.2 | 0.0 | 1.0 | 1.0 | 1.8 | 5.0 |
| color-locks | 35.5 | 0.0 | 10.6 | 2.3 | 11.1 | 59.5 |
| apartment-keys | 1.1 | 15.8 | 3.9 | 1.0 | 3.2 | 25.0 |
| library-search | 43.8 | 0.0 | 6.4 | 4.0 | 7.3 | 61.5 |
| office-sequence | 5.6 | 23.6 | 5.9 | 4.0 | 3.2 | 42.3 |
| extreme-archive | 22.3 | 0.0 | 5.0 | 3.1 | 0.9 | 31.3 |
| vault-combination | 3.8 | 13.4 | 11.8 | 5.6 | 12.3 | 46.9 |
| backtracking-vault | 8.0 | 20.0 | 17.4 | 3.9 | 7.2 | 56.5 |
| **Global** | 15.2 | 9.1 | 7.8 | 3.1 | 5.9 | 41.0 |

## planner / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 7.3 | 5.6 | 5.6 | 7,970 | 450 | 8,420 |
| color-locks | 10 | 1.0 | 0.0 | 19.3 | 22.7 | 22.7 | 42,890 | 1,446 | 44,336 |
| apartment-keys | 10 | 1.0 | 0.0 | 16.4 | 15.4 | 15.4 | 30,682 | 967 | 31,649 |
| library-search | 10 | 2.0 | 0.0 | 23.3 | 24.5 | 24.5 | 130,178 | 1,612 | 131,790 |
| office-sequence | 10 | 2.9 | 0.0 | 43.2 | 41.0 | 41.0 | 131,162 | 2,423 | 133,585 |
| extreme-archive | 10 | 1.0 | 0.0 | 25.1 | 25.3 | 25.3 | 204,890 | 1,932 | 206,822 |
| vault-combination | 10 | 1.8 | 0.0 | 69.1 | 76.0 | 76.0 | 258,217 | 4,355 | 262,572 |
| backtracking-vault | 10 | 2.8 | 0.0 | 73.1 | 70.7 | 70.7 | 290,370 | 4,726 | 295,096 |
| **Global** | 80 | 1.7 | 0.0 | 34.6 | 35.1 | 35.1 | 137,045 | 2,239 | 139,284 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 8,420 | 7.3 | 5.6 | 5.6 |
| color-locks | 10 | 10 | 100% | 1.0 | 44,336 | 19.3 | 22.7 | 22.7 |
| apartment-keys | 10 | 10 | 100% | 1.0 | 31,649 | 16.4 | 15.4 | 15.4 |
| library-search | 10 | 8 | 80% | 2.5 | 164,738 | 29.1 | 30.6 | 30.6 |
| office-sequence | 10 | 7 | 70% | 4.1 | 190,836 | 61.7 | 58.6 | 58.6 |
| extreme-archive | 10 | 10 | 100% | 1.0 | 206,822 | 25.1 | 25.3 | 25.3 |
| vault-combination | 10 | 5 | 50% | 3.6 | 525,144 | 138.2 | 152.0 | 152.0 |
| backtracking-vault | 10 | 3 | 30% | 9.3 | 983,654 | 243.7 | 235.7 | 235.7 |
| **Global** | 80 | 63 | 79% | 2.1 | 176,869 | 43.9 | 44.6 | 44.6 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 33.6 | 136,350 | 2,052 | 138,402 |
| planning | 1.0 | 695 | 187 | 882 |
| **Total** | 34.6 | 137,045 | 2,239 | 139,284 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.9 | 0.0 | 1.1 | 1.0 | 1.6 | 5.6 |
| color-locks | 6.2 | 0.0 | 2.1 | 4.2 | 10.2 | 22.7 |
| apartment-keys | 1.0 | 7.1 | 3.4 | 1.0 | 2.9 | 15.4 |
| library-search | 13.0 | 0.0 | 8.1 | 1.6 | 1.8 | 24.5 |
| office-sequence | 2.4 | 24.1 | 8.1 | 3.0 | 3.4 | 41.0 |
| extreme-archive | 22.1 | 0.0 | 1.1 | 1.0 | 1.1 | 25.3 |
| vault-combination | 11.0 | 30.4 | 15.4 | 5.0 | 14.2 | 76.0 |
| backtracking-vault | 26.3 | 22.1 | 12.6 | 2.1 | 7.6 | 70.7 |
| **Global** | 10.5 | 10.5 | 6.5 | 2.4 | 5.3 | 35.1 |

## summary / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 6.6 | 5.7 | 5.7 | 7,345 | 341 | 7,686 |
| color-locks | 10 | 2.4 | 0.0 | 33.9 | 32.9 | 32.9 | 60,351 | 3,865 | 64,216 |
| apartment-keys | 10 | 1.3 | 0.0 | 27.5 | 23.5 | 23.5 | 43,434 | 2,349 | 45,783 |
| library-search | 10 | 1.6 | 0.0 | 50.1 | 46.0 | 46.0 | 123,856 | 7,174 | 131,030 |
| office-sequence | 10 | 4.6 | 0.0 | 86.7 | 73.3 | 73.3 | 149,565 | 8,154 | 157,718 |
| extreme-archive | 10 | 5.0 | 0.0 | 93.6 | 87.6 | 87.6 | 270,252 | 12,184 | 282,436 |
| vault-combination | 10 | 5.0 | 0.0 | 138.7 | 123.5 | 123.5 | 267,518 | 14,375 | 281,893 |
| backtracking-vault | 10 | 5.0 | 0.0 | 107.3 | 89.9 | 89.9 | 201,860 | 11,041 | 212,901 |
| **Global** | 80 | 3.2 | 0.0 | 68.0 | 60.3 | 60.3 | 140,522 | 7,435 | 147,958 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 7,686 | 6.6 | 5.7 | 5.7 |
| color-locks | 10 | 9 | 90% | 2.7 | 71,351 | 37.7 | 36.6 | 36.6 |
| apartment-keys | 10 | 10 | 100% | 1.3 | 45,783 | 27.5 | 23.5 | 23.5 |
| library-search | 10 | 7 | 70% | 2.3 | 187,185 | 71.6 | 65.7 | 65.7 |
| office-sequence | 10 | 6 | 60% | 7.7 | 262,864 | 144.5 | 122.2 | 122.2 |
| extreme-archive | 10 | 1 | 10% | 50.0 | 2,824,360 | 936.0 | 876.0 | 876.0 |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 2 | 20% | 25.0 | 1,064,504 | 536.5 | 449.5 | 449.5 |
| **Global** | 80 | 45 | 56% | 5.8 | 263,036 | 121.0 | 107.2 | 107.2 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 58.7 | 124,019 | 3,885 | 127,903 |
| history_compaction | 9.3 | 16,504 | 3,551 | 20,055 |
| **Total** | 68.0 | 140,522 | 7,435 | 147,958 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.5 | 0.0 | 1.2 | 1.0 | 2.0 | 5.7 |
| color-locks | 15.0 | 0.0 | 2.7 | 4.6 | 10.6 | 32.9 |
| apartment-keys | 1.4 | 11.8 | 6.1 | 1.2 | 3.0 | 23.5 |
| library-search | 32.5 | 0.0 | 2.6 | 1.8 | 9.1 | 46.0 |
| office-sequence | 10.8 | 25.6 | 23.7 | 4.2 | 9.0 | 73.3 |
| extreme-archive | 78.1 | 0.0 | 2.4 | 5.6 | 1.5 | 87.6 |
| vault-combination | 20.1 | 34.4 | 40.9 | 6.1 | 22.0 | 123.5 |
| backtracking-vault | 33.5 | 11.1 | 23.6 | 7.2 | 14.5 | 89.9 |
| **Global** | 24.1 | 10.4 | 12.9 | 4.0 | 9.0 | 60.3 |

## planner_summary / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 8.1 | 5.9 | 5.9 | 9,180 | 541 | 9,720 |
| color-locks | 10 | 2.9 | 0.0 | 45.8 | 40.2 | 40.2 | 101,806 | 8,335 | 110,140 |
| apartment-keys | 10 | 1.5 | 0.0 | 31.1 | 26.5 | 26.5 | 49,651 | 2,713 | 52,364 |
| library-search | 10 | 1.4 | 0.0 | 32.7 | 31.5 | 31.5 | 81,524 | 4,289 | 85,812 |
| office-sequence | 10 | 3.3 | 0.0 | 86.4 | 72.4 | 72.4 | 158,053 | 8,182 | 166,234 |
| extreme-archive | 10 | 3.4 | 0.0 | 96.9 | 83.9 | 83.9 | 303,848 | 13,082 | 316,930 |
| vault-combination | 10 | 6.0 | 0.0 | 131.3 | 113.9 | 113.9 | 245,937 | 12,883 | 258,820 |
| backtracking-vault | 10 | 2.6 | 0.0 | 96.6 | 82.1 | 82.1 | 178,642 | 9,276 | 187,918 |
| **Global** | 80 | 2.8 | 0.0 | 66.1 | 57.0 | 57.0 | 141,080 | 7,412 | 148,492 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 9,720 | 8.1 | 5.9 | 5.9 |
| color-locks | 10 | 9 | 90% | 3.2 | 122,378 | 50.9 | 44.7 | 44.7 |
| apartment-keys | 10 | 10 | 100% | 1.5 | 52,364 | 31.1 | 26.5 | 26.5 |
| library-search | 10 | 10 | 100% | 1.4 | 85,812 | 32.7 | 31.5 | 31.5 |
| office-sequence | 10 | 6 | 60% | 5.5 | 277,057 | 144.0 | 120.7 | 120.7 |
| extreme-archive | 10 | 1 | 10% | 34.0 | 3,169,301 | 969.0 | 839.0 | 839.0 |
| vault-combination | 10 | 1 | 10% | 60.0 | 2,588,200 | 1,313.0 | 1,139.0 | 1,139.0 |
| backtracking-vault | 10 | 2 | 20% | 13.0 | 939,590 | 483.0 | 410.5 | 410.5 |
| **Global** | 80 | 49 | 61% | 4.5 | 242,437 | 107.9 | 93.1 | 93.1 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 56.2 | 124,401 | 3,880 | 128,280 |
| history_compaction | 8.9 | 15,973 | 3,351 | 19,324 |
| planning | 1.0 | 706 | 182 | 888 |
| **Total** | 66.1 | 141,080 | 7,412 | 148,492 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.8 | 0.0 | 1.2 | 1.0 | 1.9 | 5.9 |
| color-locks | 16.5 | 0.0 | 4.7 | 4.4 | 14.6 | 40.2 |
| apartment-keys | 1.9 | 13.7 | 7.0 | 1.1 | 2.8 | 26.5 |
| library-search | 23.9 | 0.0 | 2.0 | 2.4 | 3.2 | 31.5 |
| office-sequence | 4.4 | 23.5 | 35.1 | 3.7 | 5.7 | 72.4 |
| extreme-archive | 75.9 | 0.0 | 7.8 | 0.1 | 0.1 | 83.9 |
| vault-combination | 18.2 | 38.0 | 35.4 | 5.0 | 17.3 | 113.9 |
| backtracking-vault | 24.9 | 18.3 | 23.9 | 4.0 | 11.0 | 82.1 |
| **Global** | 20.9 | 11.7 | 14.6 | 2.7 | 7.1 | 57.0 |

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
