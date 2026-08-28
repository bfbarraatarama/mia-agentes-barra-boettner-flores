# Análisis de consumo y eficiencia — M3

**Runs:** `m3-final-run-002`, `m3-final-run-003`

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

## baseline_incremental / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 5.9 | 4.9 | 4.9 | 7,414 | 318 | 7,732 |
| color-locks | 10 | 1.1 | 0.0 | 29.5 | 30.8 | 30.8 | 111,991 | 2,076 | 114,067 |
| apartment-keys | 10 | 1.0 | 0.0 | 13.1 | 12.4 | 12.4 | 23,226 | 758 | 23,984 |
| library-search | 10 | 1.5 | 0.0 | 47.9 | 47.3 | 47.3 | 362,865 | 4,329 | 367,194 |
| office-sequence | 10 | 1.4 | 0.0 | 55.4 | 57.2 | 57.2 | 190,451 | 2,719 | 193,170 |
| extreme-archive | 10 | 1.4 | 0.0 | 48.0 | 47.4 | 47.4 | 527,154 | 5,035 | 532,188 |
| vault-combination | 10 | 1.9 | 0.0 | 70.8 | 76.6 | 76.6 | 278,006 | 3,899 | 281,905 |
| backtracking-vault | 10 | 2.3 | 0.0 | 53.0 | 51.6 | 51.6 | 198,142 | 3,460 | 201,602 |
| **Global** | 80 | 1.4 | 0.0 | 40.5 | 41.0 | 41.0 | 212,406 | 2,824 | 215,230 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 7,732 | 5.9 | 4.9 | 4.9 |
| color-locks | 10 | 9 | 90% | 1.2 | 126,741 | 32.8 | 34.2 | 34.2 |
| apartment-keys | 10 | 10 | 100% | 1.0 | 23,984 | 13.1 | 12.4 | 12.4 |
| library-search | 10 | 6 | 60% | 2.5 | 611,991 | 79.8 | 78.8 | 78.8 |
| office-sequence | 10 | 6 | 60% | 2.3 | 321,950 | 92.3 | 95.3 | 95.3 |
| extreme-archive | 10 | 6 | 60% | 2.3 | 886,981 | 80.0 | 79.0 | 79.0 |
| vault-combination | 10 | 4 | 40% | 4.8 | 704,762 | 177.0 | 191.5 | 191.5 |
| backtracking-vault | 10 | 5 | 50% | 4.6 | 403,204 | 106.0 | 103.2 | 103.2 |
| **Global** | 80 | 56 | 70% | 2.1 | 307,472 | 57.8 | 58.6 | 58.6 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 40.5 | 212,406 | 2,824 | 215,230 |
| **Total** | 40.5 | 212,406 | 2,824 | 215,230 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.3 | 0.0 | 1.0 | 1.0 | 1.6 | 4.9 |
| color-locks | 7.7 | 0.0 | 8.3 | 4.3 | 10.5 | 30.8 |
| apartment-keys | 1.2 | 5.4 | 3.0 | 1.0 | 1.8 | 12.4 |
| library-search | 26.7 | 0.0 | 9.4 | 2.1 | 9.1 | 47.3 |
| office-sequence | 6.9 | 26.1 | 17.6 | 2.4 | 4.2 | 57.2 |
| extreme-archive | 34.6 | 0.0 | 11.4 | 0.6 | 0.8 | 47.4 |
| vault-combination | 9.7 | 26.6 | 24.8 | 4.1 | 11.4 | 76.6 |
| backtracking-vault | 14.1 | 22.9 | 7.9 | 2.6 | 4.1 | 51.6 |
| **Global** | 12.8 | 10.1 | 10.4 | 2.3 | 5.4 | 41.0 |

## planner_incremental / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.9 | 0.0 | 10.2 | 6.3 | 6.3 | 16,517 | 772 | 17,290 |
| color-locks | 10 | 1.4 | 0.0 | 46.5 | 44.2 | 44.2 | 179,262 | 3,340 | 182,603 |
| apartment-keys | 10 | 1.1 | 0.0 | 23.2 | 22.1 | 22.1 | 61,352 | 1,593 | 62,945 |
| library-search | 10 | 1.3 | 0.0 | 34.0 | 32.3 | 32.3 | 224,622 | 2,386 | 227,008 |
| office-sequence | 10 | 2.3 | 0.0 | 52.3 | 50.1 | 50.1 | 189,339 | 3,620 | 192,958 |
| extreme-archive | 10 | 1.3 | 0.0 | 41.6 | 40.3 | 40.3 | 470,524 | 3,178 | 473,703 |
| vault-combination | 10 | 1.6 | 0.0 | 64.2 | 65.0 | 65.0 | 242,764 | 3,810 | 246,573 |
| backtracking-vault | 10 | 1.6 | 0.0 | 56.9 | 54.5 | 54.5 | 219,119 | 3,891 | 223,010 |
| **Global** | 80 | 1.6 | 0.0 | 41.1 | 39.4 | 39.4 | 200,437 | 2,824 | 203,261 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 9 | 90% | 2.1 | 19,211 | 11.3 | 7.0 | 7.0 |
| color-locks | 10 | 7 | 70% | 2.0 | 260,861 | 66.4 | 63.1 | 63.1 |
| apartment-keys | 10 | 9 | 90% | 1.2 | 69,939 | 25.8 | 24.6 | 24.6 |
| library-search | 10 | 7 | 70% | 1.9 | 324,297 | 48.6 | 46.1 | 46.1 |
| office-sequence | 10 | 7 | 70% | 3.3 | 275,655 | 74.7 | 71.6 | 71.6 |
| extreme-archive | 10 | 7 | 70% | 1.9 | 676,718 | 59.4 | 57.6 | 57.6 |
| vault-combination | 10 | 4 | 40% | 4.0 | 616,433 | 160.5 | 162.5 | 162.5 |
| backtracking-vault | 10 | 5 | 50% | 3.2 | 446,020 | 113.8 | 109.0 | 109.0 |
| **Global** | 80 | 55 | 69% | 2.3 | 295,653 | 59.8 | 57.2 | 57.2 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 39.0 | 198,326 | 2,548 | 200,875 |
| planning | 2.1 | 2,111 | 276 | 2,386 |
| **Total** | 41.1 | 200,437 | 2,824 | 203,261 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 2.4 | 0.0 | 1.2 | 0.9 | 1.8 | 6.3 |
| color-locks | 14.4 | 0.0 | 5.7 | 4.9 | 19.2 | 44.2 |
| apartment-keys | 2.4 | 7.9 | 8.6 | 1.1 | 2.1 | 22.1 |
| library-search | 20.8 | 0.0 | 7.9 | 1.7 | 1.9 | 32.3 |
| office-sequence | 4.0 | 22.2 | 10.6 | 3.6 | 9.7 | 50.1 |
| extreme-archive | 31.4 | 0.0 | 4.1 | 0.8 | 4.0 | 40.3 |
| vault-combination | 9.8 | 26.6 | 17.7 | 3.1 | 7.8 | 65.0 |
| backtracking-vault | 5.7 | 18.8 | 15.4 | 6.3 | 8.3 | 54.5 |
| **Global** | 11.4 | 9.4 | 8.9 | 2.8 | 6.8 | 39.4 |

## summary_incremental / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 7.1 | 6.1 | 6.1 | 9,431 | 393 | 9,824 |
| color-locks | 10 | 1.9 | 0.0 | 48.1 | 41.6 | 41.6 | 97,582 | 4,943 | 102,526 |
| apartment-keys | 10 | 1.1 | 0.0 | 20.5 | 17.3 | 17.3 | 34,399 | 1,560 | 35,959 |
| library-search | 10 | 1.6 | 0.0 | 44.4 | 39.1 | 39.1 | 140,955 | 6,919 | 147,875 |
| office-sequence | 10 | 4.3 | 0.0 | 70.9 | 57.9 | 57.9 | 132,470 | 6,197 | 138,667 |
| extreme-archive | 10 | 2.2 | 0.0 | 84.8 | 73.4 | 73.4 | 264,663 | 11,830 | 276,493 |
| vault-combination | 10 | 5.4 | 0.3 | 161.0 | 139.0 | 139.0 | 336,202 | 15,984 | 352,186 |
| backtracking-vault | 10 | 4.1 | 0.2 | 98.8 | 83.7 | 83.7 | 202,949 | 9,987 | 212,936 |
| **Global** | 80 | 2.7 | 0.1 | 67.0 | 57.3 | 57.3 | 152,332 | 7,227 | 159,558 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 9,824 | 7.1 | 6.1 | 6.1 |
| color-locks | 10 | 10 | 100% | 1.9 | 102,526 | 48.1 | 41.6 | 41.6 |
| apartment-keys | 10 | 10 | 100% | 1.1 | 35,959 | 20.5 | 17.3 | 17.3 |
| library-search | 10 | 8 | 80% | 2.0 | 184,843 | 55.5 | 48.9 | 48.9 |
| office-sequence | 10 | 6 | 60% | 7.2 | 231,112 | 118.2 | 96.5 | 96.5 |
| extreme-archive | 10 | 2 | 20% | 11.0 | 1,382,466 | 424.0 | 367.0 | 367.0 |
| vault-combination | 10 | 1 | 10% | 54.0 | 3,521,860 | 1,610.0 | 1,390.0 | 1,390.0 |
| backtracking-vault | 10 | 2 | 20% | 20.5 | 1,064,681 | 494.0 | 418.5 | 418.5 |
| **Global** | 80 | 49 | 61% | 4.4 | 260,503 | 109.3 | 93.5 | 93.5 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 58.0 | 133,791 | 3,761 | 137,553 |
| history_compaction | 9.0 | 18,540 | 3,465 | 22,005 |
| **Total** | 67.0 | 152,332 | 7,227 | 159,558 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.9 | 0.0 | 1.1 | 1.0 | 2.1 | 6.1 |
| color-locks | 20.1 | 0.0 | 5.1 | 4.6 | 11.8 | 41.6 |
| apartment-keys | 1.5 | 8.2 | 4.8 | 1.0 | 1.8 | 17.3 |
| library-search | 27.4 | 0.0 | 7.2 | 1.8 | 2.7 | 39.1 |
| office-sequence | 8.5 | 21.3 | 19.0 | 3.6 | 5.5 | 57.9 |
| extreme-archive | 70.1 | 0.0 | 2.8 | 0.3 | 0.2 | 73.4 |
| vault-combination | 19.1 | 46.9 | 47.7 | 4.8 | 20.5 | 139.0 |
| backtracking-vault | 28.6 | 15.3 | 24.6 | 5.1 | 10.1 | 83.7 |
| **Global** | 22.1 | 11.5 | 14.0 | 2.8 | 6.8 | 57.3 |

## planner_summary_incremental / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.1 | 8.0 | 5.1 | 5.1 | 9,627 | 479 | 10,106 |
| color-locks | 10 | 2.3 | 0.0 | 37.5 | 30.4 | 30.4 | 91,845 | 6,840 | 98,686 |
| apartment-keys | 10 | 1.0 | 0.2 | 22.8 | 17.7 | 17.7 | 39,758 | 2,064 | 41,821 |
| library-search | 10 | 2.4 | 0.0 | 75.5 | 66.4 | 66.4 | 195,547 | 9,395 | 204,942 |
| office-sequence | 10 | 2.9 | 0.0 | 63.0 | 51.6 | 51.6 | 120,304 | 5,710 | 126,013 |
| extreme-archive | 10 | 3.9 | 0.0 | 101.1 | 111.2 | 111.2 | 318,576 | 18,446 | 337,022 |
| vault-combination | 10 | 5.2 | 0.0 | 138.3 | 119.2 | 119.2 | 287,014 | 13,274 | 300,288 |
| backtracking-vault | 10 | 5.9 | 0.0 | 131.3 | 115.9 | 115.9 | 296,453 | 17,803 | 314,256 |
| **Global** | 80 | 3.1 | 0.0 | 72.2 | 64.7 | 64.7 | 169,890 | 9,251 | 179,142 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 10,106 | 8.0 | 5.1 | 5.1 |
| color-locks | 10 | 7 | 70% | 3.3 | 140,979 | 53.6 | 43.4 | 43.4 |
| apartment-keys | 10 | 10 | 100% | 1.0 | 41,821 | 22.8 | 17.7 | 17.7 |
| library-search | 10 | 6 | 60% | 4.0 | 341,570 | 125.8 | 110.7 | 110.7 |
| office-sequence | 10 | 7 | 70% | 4.1 | 180,019 | 90.0 | 73.7 | 73.7 |
| extreme-archive | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 1 | 10% | 59.0 | 3,142,562 | 1,313.0 | 1,159.0 | 1,159.0 |
| **Global** | 80 | 41 | 51% | 6.0 | 349,545 | 140.8 | 126.2 | 126.2 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 59.9 | 147,140 | 4,975 | 152,115 |
| history_compaction | 10.2 | 20,611 | 4,013 | 24,624 |
| planning | 2.1 | 2,140 | 263 | 2,402 |
| **Total** | 72.2 | 169,890 | 9,251 | 179,142 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.6 | 0.0 | 1.0 | 1.0 | 1.5 | 5.1 |
| color-locks | 9.5 | 0.0 | 5.9 | 3.8 | 11.2 | 30.4 |
| apartment-keys | 1.4 | 7.4 | 5.5 | 1.0 | 2.4 | 17.7 |
| library-search | 55.5 | 0.0 | 3.1 | 1.8 | 6.0 | 66.4 |
| office-sequence | 11.7 | 17.5 | 13.5 | 3.8 | 5.1 | 51.6 |
| extreme-archive | 108.3 | 0.0 | 2.6 | 0.3 | 0.0 | 111.2 |
| vault-combination | 15.8 | 41.2 | 45.3 | 4.2 | 12.7 | 119.2 |
| backtracking-vault | 35.6 | 22.0 | 40.5 | 6.1 | 11.7 | 115.9 |
| **Global** | 29.9 | 11.0 | 14.7 | 2.8 | 6.3 | 64.7 |
