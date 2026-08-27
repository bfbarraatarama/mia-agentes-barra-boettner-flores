# Análisis de consumo y eficiencia — M3

**Runs:** `m3-final-run-002`, `m3-final-run-007`

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
