# Análisis de consumo y eficiencia — M3

**Run:** `m3-final-run-008`

## planner / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 20 | 1.0 | 0.0 | 7.3 | 5.4 | 5.4 | 7,995 | 488 | 8,483 |
| color-locks | 20 | 1.9 | 0.0 | 49.0 | 50.4 | 50.4 | 211,747 | 3,660 | 215,407 |
| apartment-keys | 20 | 1.2 | 0.0 | 29.6 | 28.4 | 28.4 | 76,560 | 1,548 | 78,109 |
| library-search | 20 | 3.5 | 0.0 | 38.5 | 39.5 | 39.5 | 253,694 | 2,840 | 256,534 |
| office-sequence | 20 | 1.4 | 0.0 | 55.0 | 55.0 | 55.0 | 188,605 | 3,002 | 191,608 |
| extreme-archive | 20 | 1.1 | 0.0 | 26.4 | 25.4 | 25.4 | 202,717 | 1,846 | 204,563 |
| vault-combination | 20 | 1.9 | 0.0 | 77.1 | 80.8 | 80.8 | 293,915 | 4,634 | 298,549 |
| backtracking-vault | 20 | 1.8 | 0.0 | 67.5 | 69.2 | 69.2 | 235,487 | 3,801 | 239,288 |
| **Global** | 160 | 1.7 | 0.0 | 43.8 | 44.2 | 44.2 | 183,840 | 2,727 | 186,567 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 20 | 20 | 100% | 1.0 | 8,483 | 7.3 | 5.4 | 5.4 |
| color-locks | 20 | 12 | 60% | 3.1 | 359,012 | 81.7 | 83.9 | 83.9 |
| apartment-keys | 20 | 16 | 80% | 1.5 | 97,636 | 37.1 | 35.4 | 35.4 |
| library-search | 20 | 13 | 65% | 5.5 | 394,667 | 59.1 | 60.8 | 60.8 |
| office-sequence | 20 | 14 | 70% | 1.9 | 273,725 | 78.6 | 78.6 | 78.6 |
| extreme-archive | 20 | 20 | 100% | 1.1 | 204,563 | 26.4 | 25.4 | 25.4 |
| vault-combination | 20 | 3 | 15% | 13.0 | 1,990,324 | 514.0 | 538.3 | 538.3 |
| backtracking-vault | 20 | 8 | 40% | 4.4 | 598,220 | 168.8 | 173.1 | 173.1 |
| **Global** | 160 | 106 | 66% | 2.6 | 281,611 | 66.1 | 66.8 | 66.8 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 42.8 | 183,127 | 2,547 | 185,673 |
| planning | 1.0 | 713 | 181 | 894 |
| **Total** | 43.8 | 183,840 | 2,727 | 186,567 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.9 | 0.0 | 1.0 | 1.0 | 1.6 | 5.4 |
| color-locks | 16.1 | 0.0 | 12.1 | 3.1 | 19.0 | 50.4 |
| apartment-keys | 1.1 | 17.7 | 5.5 | 1.1 | 3.0 | 28.4 |
| library-search | 24.4 | 0.0 | 10.2 | 2.2 | 2.7 | 39.5 |
| office-sequence | 5.9 | 24.6 | 16.8 | 3.6 | 4.2 | 55.0 |
| extreme-archive | 22.1 | 0.0 | 1.1 | 1.1 | 1.1 | 25.4 |
| vault-combination | 7.3 | 35.5 | 22.9 | 3.5 | 11.5 | 80.8 |
| backtracking-vault | 15.3 | 23.8 | 12.4 | 6.2 | 11.4 | 69.2 |
| **Global** | 11.8 | 12.7 | 10.3 | 2.7 | 6.8 | 44.2 |

## baseline_incremental / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 20 | 1.1 | 0.0 | 7.5 | 8.2 | 8.2 | 13,387 | 485 | 13,872 |
| color-locks | 20 | 1.5 | 0.0 | 46.4 | 45.9 | 45.9 | 202,408 | 3,775 | 206,183 |
| apartment-keys | 20 | 1.1 | 0.0 | 16.4 | 15.7 | 15.7 | 35,570 | 920 | 36,490 |
| library-search | 20 | 2.8 | 0.0 | 47.3 | 48.3 | 48.3 | 333,690 | 3,844 | 337,534 |
| office-sequence | 20 | 1.5 | 0.0 | 60.0 | 60.5 | 60.5 | 208,036 | 2,921 | 210,957 |
| extreme-archive | 20 | 1.4 | 0.0 | 37.5 | 36.8 | 36.8 | 377,955 | 3,076 | 381,031 |
| vault-combination | 20 | 1.7 | 0.0 | 60.4 | 62.6 | 62.6 | 223,803 | 3,536 | 227,338 |
| backtracking-vault | 20 | 1.9 | 0.0 | 52.7 | 51.9 | 51.9 | 227,818 | 5,919 | 233,736 |
| **Global** | 160 | 1.6 | 0.0 | 41.0 | 41.2 | 41.2 | 202,833 | 3,059 | 205,893 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 20 | 20 | 100% | 1.1 | 13,872 | 7.5 | 8.2 | 8.2 |
| color-locks | 20 | 13 | 65% | 2.3 | 317,205 | 71.4 | 70.6 | 70.6 |
| apartment-keys | 20 | 19 | 95% | 1.1 | 38,411 | 17.3 | 16.5 | 16.5 |
| library-search | 20 | 10 | 50% | 5.5 | 675,067 | 94.6 | 96.6 | 96.6 |
| office-sequence | 20 | 14 | 70% | 2.1 | 301,367 | 85.7 | 86.4 | 86.4 |
| extreme-archive | 20 | 17 | 85% | 1.6 | 448,272 | 44.1 | 43.3 | 43.3 |
| vault-combination | 20 | 9 | 45% | 3.8 | 505,196 | 134.1 | 139.1 | 139.1 |
| backtracking-vault | 20 | 11 | 55% | 3.4 | 424,975 | 95.8 | 94.3 | 94.3 |
| **Global** | 160 | 113 | 71% | 2.3 | 291,529 | 58.1 | 58.4 | 58.4 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 41.0 | 202,833 | 3,059 | 205,893 |
| **Total** | 41.0 | 202,833 | 3,059 | 205,893 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 4.3 | 0.0 | 1.1 | 1.0 | 1.7 | 8.2 |
| color-locks | 20.9 | 0.0 | 6.7 | 3.4 | 14.9 | 45.9 |
| apartment-keys | 1.1 | 7.8 | 3.5 | 1.0 | 2.2 | 15.7 |
| library-search | 38.2 | 0.0 | 5.0 | 1.6 | 3.4 | 48.3 |
| office-sequence | 6.2 | 28.1 | 18.6 | 2.6 | 5.0 | 60.5 |
| extreme-archive | 25.1 | 0.0 | 6.8 | 1.1 | 3.9 | 36.8 |
| vault-combination | 6.2 | 29.6 | 14.8 | 3.7 | 8.2 | 62.6 |
| backtracking-vault | 10.7 | 17.2 | 15.7 | 2.6 | 5.7 | 51.9 |
| **Global** | 14.1 | 10.3 | 9.1 | 2.1 | 5.6 | 41.2 |

## planner_incremental / nova-lite / multi_attempt_recovery

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de intentos adicionales de llamadas al LLM debidos a errores transitorios (timeout, 5xx, rate limit, excepciones de red).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 20 | 1.0 | 0.0 | 9.8 | 7.0 | 7.0 | 18,436 | 642 | 19,079 |
| color-locks | 20 | 2.8 | 0.0 | 44.2 | 41.5 | 41.5 | 188,508 | 3,265 | 191,773 |
| apartment-keys | 20 | 1.1 | 0.0 | 20.6 | 18.5 | 18.5 | 49,217 | 1,421 | 50,638 |
| library-search | 20 | 1.9 | 0.0 | 37.0 | 35.4 | 35.4 | 217,620 | 2,790 | 220,410 |
| office-sequence | 20 | 1.1 | 0.0 | 42.0 | 41.6 | 41.6 | 144,395 | 2,675 | 147,070 |
| extreme-archive | 20 | 1.6 | 0.0 | 33.4 | 32.9 | 32.9 | 303,304 | 2,603 | 305,907 |
| vault-combination | 20 | 1.8 | 0.0 | 67.5 | 69.7 | 69.7 | 259,953 | 4,275 | 264,227 |
| backtracking-vault | 20 | 2.0 | 0.0 | 55.0 | 54.3 | 54.3 | 204,295 | 3,578 | 207,873 |
| **Global** | 160 | 1.6 | 0.0 | 38.7 | 37.6 | 37.6 | 173,216 | 2,656 | 175,872 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 20 | 19 | 95% | 1.1 | 20,083 | 10.4 | 7.4 | 7.4 |
| color-locks | 20 | 12 | 60% | 4.7 | 319,622 | 73.7 | 69.2 | 69.2 |
| apartment-keys | 20 | 19 | 95% | 1.2 | 53,303 | 21.6 | 19.5 | 19.5 |
| library-search | 20 | 11 | 55% | 3.4 | 400,745 | 67.4 | 64.4 | 64.4 |
| office-sequence | 20 | 19 | 95% | 1.1 | 154,811 | 44.3 | 43.8 | 43.8 |
| extreme-archive | 20 | 16 | 80% | 2.1 | 382,383 | 41.7 | 41.1 | 41.1 |
| vault-combination | 20 | 7 | 35% | 5.0 | 754,936 | 192.7 | 199.0 | 199.0 |
| backtracking-vault | 20 | 11 | 55% | 3.6 | 377,951 | 100.0 | 98.7 | 98.7 |
| **Global** | 160 | 114 | 71% | 2.3 | 246,838 | 54.3 | 52.8 | 52.8 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 36.6 | 171,052 | 2,389 | 173,440 |
| planning | 2.1 | 2,164 | 267 | 2,432 |
| **Total** | 38.7 | 173,216 | 2,656 | 175,872 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.8 | 0.0 | 2.8 | 0.9 | 1.6 | 7.0 |
| color-locks | 17.9 | 0.0 | 9.9 | 3.5 | 10.2 | 41.5 |
| apartment-keys | 1.4 | 9.1 | 4.0 | 1.0 | 3.0 | 18.5 |
| library-search | 22.3 | 0.0 | 6.3 | 1.6 | 5.2 | 35.4 |
| office-sequence | 2.6 | 20.2 | 13.2 | 3.0 | 2.5 | 41.6 |
| extreme-archive | 25.1 | 0.0 | 4.4 | 1.4 | 2.0 | 32.9 |
| vault-combination | 7.2 | 27.7 | 17.6 | 4.8 | 12.3 | 69.7 |
| backtracking-vault | 15.8 | 14.4 | 10.2 | 7.7 | 6.2 | 54.3 |
| **Global** | 11.8 | 8.9 | 8.6 | 3.0 | 5.4 | 37.6 |
