# Análisis de consumo y eficiencia — M3

**Runs:** `m3-final-run-001`, `m3-final-run-002`

## baseline / nova-lite / multi_attempt

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 5.9 | 5.0 | 5.0 | 6,249 | 312 | 6,561 |
| color-locks | 10 | 1.0 | 0.0 | 30.6 | 32.1 | 32.1 | 106,498 | 2,040 | 108,537 |
| apartment-keys | 10 | 1.0 | 0.0 | 15.7 | 14.9 | 14.9 | 27,519 | 872 | 28,391 |
| library-search | 10 | 2.8 | 0.0 | 23.5 | 22.8 | 22.8 | 108,200 | 1,765 | 109,965 |
| office-sequence | 10 | 1.0 | 0.0 | 40.0 | 40.8 | 40.8 | 114,997 | 1,972 | 116,969 |
| extreme-archive | 10 | 1.1 | 0.0 | 24.9 | 23.8 | 23.8 | 212,893 | 2,172 | 215,064 |
| vault-combination | 10 | 1.0 | 0.0 | 34.8 | 40.2 | 40.2 | 109,420 | 2,089 | 111,508 |
| backtracking-vault | 10 | 1.0 | 0.0 | 37.0 | 36.6 | 36.6 | 110,430 | 2,067 | 112,497 |
| **Global** | 80 | 1.2 | 0.0 | 26.6 | 27.0 | 27.0 | 99,526 | 1,661 | 101,187 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 6,561 | 5.9 | 5.0 | 5.0 |
| color-locks | 10 | 5 | 50% | 2.0 | 217,074 | 61.2 | 64.2 | 64.2 |
| apartment-keys | 10 | 10 | 100% | 1.0 | 28,391 | 15.7 | 14.9 | 14.9 |
| library-search | 10 | 7 | 70% | 4.0 | 157,093 | 33.6 | 32.6 | 32.6 |
| office-sequence | 10 | 8 | 80% | 1.2 | 146,211 | 50.0 | 51.0 | 51.0 |
| extreme-archive | 10 | 10 | 100% | 1.1 | 215,064 | 24.9 | 23.8 | 23.8 |
| vault-combination | 10 | 5 | 50% | 2.0 | 223,016 | 69.6 | 80.4 | 80.4 |
| backtracking-vault | 10 | 4 | 40% | 2.5 | 281,242 | 92.5 | 91.5 | 91.5 |
| **Global** | 80 | 59 | 74% | 1.7 | 137,202 | 36.0 | 36.6 | 36.6 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 26.6 | 99,526 | 1,661 | 101,187 |
| **Total** | 26.6 | 99,526 | 1,661 | 101,187 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.1 | 0.0 | 1.0 | 1.0 | 1.9 | 5.0 |
| color-locks | 12.5 | 0.0 | 6.9 | 2.8 | 9.9 | 32.1 |
| apartment-keys | 1.1 | 6.5 | 4.3 | 1.1 | 1.9 | 14.9 |
| library-search | 17.0 | 0.0 | 1.5 | 1.6 | 2.7 | 22.8 |
| office-sequence | 3.8 | 21.2 | 6.0 | 4.3 | 5.5 | 40.8 |
| extreme-archive | 20.3 | 0.0 | 1.2 | 1.1 | 1.2 | 23.8 |
| vault-combination | 3.0 | 16.7 | 8.1 | 4.7 | 7.7 | 40.2 |
| backtracking-vault | 8.3 | 13.2 | 6.3 | 3.7 | 5.1 | 36.6 |
| **Global** | 8.4 | 7.2 | 4.4 | 2.5 | 4.5 | 27.0 |

## planner / nova-lite / multi_attempt

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 7.3 | 5.2 | 5.2 | 8,014 | 497 | 8,511 |
| color-locks | 10 | 1.2 | 0.0 | 34.9 | 37.7 | 37.7 | 133,470 | 2,494 | 135,965 |
| apartment-keys | 10 | 1.0 | 0.0 | 18.4 | 16.7 | 16.7 | 37,404 | 1,016 | 38,420 |
| library-search | 10 | 1.9 | 0.0 | 35.8 | 39.3 | 39.3 | 204,424 | 2,693 | 207,117 |
| office-sequence | 10 | 1.0 | 0.0 | 36.5 | 37.5 | 37.5 | 113,608 | 2,175 | 115,783 |
| extreme-archive | 10 | 1.0 | 0.0 | 24.9 | 24.6 | 24.6 | 199,080 | 1,761 | 200,840 |
| vault-combination | 10 | 1.0 | 0.0 | 34.4 | 42.6 | 42.6 | 102,461 | 2,154 | 104,614 |
| backtracking-vault | 10 | 1.9 | 0.0 | 38.0 | 35.8 | 35.8 | 114,842 | 2,284 | 117,126 |
| **Global** | 80 | 1.2 | 0.0 | 28.8 | 29.9 | 29.9 | 114,163 | 1,884 | 116,047 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 8,511 | 7.3 | 5.2 | 5.2 |
| color-locks | 10 | 4 | 40% | 3.0 | 339,912 | 87.2 | 94.2 | 94.2 |
| apartment-keys | 10 | 9 | 90% | 1.1 | 42,689 | 20.4 | 18.6 | 18.6 |
| library-search | 10 | 5 | 50% | 3.8 | 414,234 | 71.6 | 78.6 | 78.6 |
| office-sequence | 10 | 10 | 100% | 1.0 | 115,783 | 36.5 | 37.5 | 37.5 |
| extreme-archive | 10 | 10 | 100% | 1.0 | 200,840 | 24.9 | 24.6 | 24.6 |
| vault-combination | 10 | 6 | 60% | 1.7 | 174,357 | 57.3 | 71.0 | 71.0 |
| backtracking-vault | 10 | 4 | 40% | 4.8 | 292,814 | 95.0 | 89.5 | 89.5 |
| **Global** | 80 | 58 | 72% | 1.7 | 160,065 | 39.7 | 41.3 | 41.3 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 27.8 | 113,457 | 1,700 | 115,157 |
| planning | 1.0 | 706 | 184 | 890 |
| **Total** | 28.8 | 114,163 | 1,884 | 116,047 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.6 | 0.0 | 1.1 | 1.0 | 1.5 | 5.2 |
| color-locks | 14.8 | 0.0 | 8.3 | 2.9 | 11.7 | 37.7 |
| apartment-keys | 1.8 | 7.2 | 5.2 | 1.0 | 1.5 | 16.7 |
| library-search | 32.8 | 0.0 | 2.8 | 1.6 | 2.1 | 39.3 |
| office-sequence | 2.0 | 18.6 | 10.9 | 3.2 | 2.8 | 37.5 |
| extreme-archive | 20.8 | 0.0 | 1.7 | 1.0 | 1.1 | 24.6 |
| vault-combination | 3.9 | 18.9 | 7.3 | 4.2 | 8.3 | 42.6 |
| backtracking-vault | 7.0 | 16.1 | 6.0 | 2.1 | 4.6 | 35.8 |
| **Global** | 10.6 | 7.6 | 5.4 | 2.1 | 4.2 | 29.9 |

## summary / nova-lite / multi_attempt

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 5.8 | 4.9 | 4.9 | 6,135 | 306 | 6,441 |
| color-locks | 10 | 2.4 | 0.0 | 34.6 | 30.1 | 30.1 | 62,804 | 3,766 | 66,570 |
| apartment-keys | 10 | 1.0 | 0.0 | 17.7 | 16.7 | 16.7 | 25,865 | 1,457 | 27,322 |
| library-search | 10 | 1.0 | 0.0 | 33.2 | 30.3 | 30.3 | 89,151 | 4,552 | 93,703 |
| office-sequence | 10 | 1.0 | 0.0 | 21.4 | 17.4 | 17.4 | 32,456 | 1,843 | 34,299 |
| extreme-archive | 10 | 1.1 | 0.0 | 36.1 | 31.6 | 31.6 | 103,780 | 5,108 | 108,888 |
| vault-combination | 10 | 1.0 | 0.0 | 36.4 | 35.3 | 35.3 | 64,720 | 3,621 | 68,341 |
| backtracking-vault | 10 | 1.0 | 0.0 | 24.4 | 20.0 | 20.0 | 42,340 | 2,568 | 44,908 |
| **Global** | 80 | 1.2 | 0.0 | 26.2 | 23.3 | 23.3 | 53,406 | 2,903 | 56,309 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 6,441 | 5.8 | 4.9 | 4.9 |
| color-locks | 10 | 4 | 40% | 6.0 | 166,424 | 86.5 | 75.2 | 75.2 |
| apartment-keys | 10 | 6 | 60% | 1.7 | 45,536 | 29.5 | 27.8 | 27.8 |
| library-search | 10 | 4 | 40% | 2.5 | 234,258 | 83.0 | 75.8 | 75.8 |
| office-sequence | 10 | 1 | 10% | 10.0 | 342,990 | 214.0 | 174.0 | 174.0 |
| extreme-archive | 10 | 2 | 20% | 5.5 | 544,439 | 180.5 | 158.0 | 158.0 |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| **Global** | 80 | 27 | 34% | 3.5 | 166,842 | 77.6 | 69.0 | 69.0 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 22.8 | 47,199 | 1,493 | 48,691 |
| history_compaction | 3.4 | 6,208 | 1,410 | 7,618 |
| **Total** | 26.2 | 53,406 | 2,903 | 56,309 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.1 | 0.0 | 1.0 | 1.0 | 1.8 | 4.9 |
| color-locks | 13.7 | 0.0 | 4.2 | 3.3 | 8.9 | 30.1 |
| apartment-keys | 1.2 | 8.1 | 3.9 | 0.9 | 2.6 | 16.7 |
| library-search | 24.6 | 0.0 | 1.3 | 1.3 | 3.1 | 30.3 |
| office-sequence | 2.3 | 6.6 | 5.0 | 2.8 | 0.7 | 17.4 |
| extreme-archive | 29.3 | 0.0 | 1.1 | 1.0 | 0.2 | 31.6 |
| vault-combination | 6.2 | 8.0 | 11.9 | 3.6 | 5.6 | 35.3 |
| backtracking-vault | 4.3 | 4.8 | 5.9 | 1.6 | 3.4 | 20.0 |
| **Global** | 10.3 | 3.4 | 4.3 | 1.9 | 3.3 | 23.3 |

## planner_summary / nova-lite / multi_attempt

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 9.4 | 6.7 | 6.7 | 11,558 | 740 | 12,298 |
| color-locks | 10 | 1.0 | 0.0 | 23.8 | 21.3 | 21.3 | 42,699 | 2,971 | 45,670 |
| apartment-keys | 10 | 1.1 | 0.0 | 17.0 | 13.3 | 13.3 | 24,772 | 1,369 | 26,141 |
| library-search | 10 | 1.0 | 0.0 | 26.0 | 24.9 | 24.9 | 64,222 | 3,475 | 67,697 |
| office-sequence | 10 | 1.2 | 0.0 | 38.0 | 32.3 | 32.3 | 65,826 | 3,495 | 69,321 |
| extreme-archive | 10 | 1.1 | 0.0 | 36.2 | 31.8 | 31.8 | 110,239 | 5,577 | 115,816 |
| vault-combination | 10 | 1.0 | 0.0 | 34.9 | 31.2 | 31.2 | 63,656 | 4,171 | 67,828 |
| backtracking-vault | 10 | 1.2 | 0.0 | 38.8 | 32.0 | 32.0 | 70,114 | 4,186 | 74,300 |
| **Global** | 80 | 1.1 | 0.0 | 28.0 | 24.2 | 24.2 | 56,636 | 3,248 | 59,884 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 9 | 90% | 1.1 | 13,664 | 10.4 | 7.4 | 7.4 |
| color-locks | 10 | 2 | 20% | 5.0 | 228,352 | 119.0 | 106.5 | 106.5 |
| apartment-keys | 10 | 8 | 80% | 1.4 | 32,676 | 21.2 | 16.6 | 16.6 |
| library-search | 10 | 6 | 60% | 1.7 | 112,828 | 43.3 | 41.5 | 41.5 |
| office-sequence | 10 | 3 | 30% | 4.0 | 231,069 | 126.7 | 107.7 | 107.7 |
| extreme-archive | 10 | 1 | 10% | 11.0 | 1,158,155 | 362.0 | 318.0 | 318.0 |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| **Global** | 80 | 29 | 36% | 3.0 | 165,197 | 77.3 | 66.7 | 66.7 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 23.2 | 49,004 | 1,475 | 50,479 |
| history_compaction | 3.8 | 6,914 | 1,591 | 8,505 |
| planning | 1.0 | 718 | 182 | 900 |
| **Total** | 28.0 | 56,636 | 3,248 | 59,884 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 2.4 | 0.0 | 1.3 | 0.9 | 2.1 | 6.7 |
| color-locks | 7.3 | 0.0 | 2.0 | 2.7 | 9.3 | 21.3 |
| apartment-keys | 1.0 | 5.4 | 4.2 | 1.0 | 1.7 | 13.3 |
| library-search | 19.1 | 0.0 | 1.3 | 1.9 | 2.6 | 24.9 |
| office-sequence | 3.3 | 13.1 | 10.0 | 3.3 | 2.6 | 32.3 |
| extreme-archive | 27.9 | 0.0 | 3.7 | 0.1 | 0.1 | 31.8 |
| vault-combination | 3.6 | 13.9 | 8.2 | 2.2 | 3.3 | 31.2 |
| backtracking-vault | 7.2 | 7.0 | 6.5 | 2.5 | 8.8 | 32.0 |
| **Global** | 9.0 | 4.9 | 4.7 | 1.8 | 3.8 | 24.2 |

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
