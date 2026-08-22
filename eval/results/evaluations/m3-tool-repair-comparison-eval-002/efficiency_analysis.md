# Análisis de consumo y eficiencia — M3

**Run:** `m3-tool-repair-comparison-run-002`

## minimal / llama3.1

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 3.6 | 3.9 | 3.9 | 1,423 | 195 | 1,618 |
| color-locks | 10 | 1.0 | 0.0 | 19.3 | 34.4 | 34.4 | 26,545 | 779 | 27,325 |
| apartment-keys | 10 | 1.0 | 0.0 | 26.2 | 32.1 | 32.1 | 36,463 | 575 | 37,039 |
| library-search | 10 | 1.0 | 0.0 | 6.5 | 5.9 | 5.9 | 2,410 | 319 | 2,730 |
| office-sequence | 10 | 1.0 | 0.0 | 33.4 | 64.8 | 64.8 | 58,434 | 1,287 | 59,721 |
| extreme-archive | 10 | 1.0 | 0.0 | 10.4 | 9.6 | 9.6 | 10,749 | 247 | 10,997 |
| vault-combination | 10 | 1.0 | 0.0 | 2.9 | 4.0 | 4.0 | 1,350 | 316 | 1,666 |
| backtracking-vault | 10 | 1.0 | 0.0 | 7.2 | 7.3 | 7.3 | 8,436 | 212 | 8,649 |
| **Global** | 80 | 1.0 | 0.0 | 13.7 | 20.2 | 20.2 | 18,226 | 491 | 18,718 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1 | 10% | 10.0 | 16,188 | 36.0 | 39.0 | 39.0 |
| color-locks | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| apartment-keys | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| library-search | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| office-sequence | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| extreme-archive | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| **Global** | 80 | 1 | 1% | 80.0 | 1,497,483 | 1,095.0 | 1,620.0 | 1,620.0 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 13.7 | 18,226 | 491 | 18,718 |
| **Total** | 13.7 | 18,226 | 491 | 18,718 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.7 | 0.0 | 1.2 | 0.7 | 0.3 | 3.9 |
| color-locks | 18.7 | 0.0 | 0.0 | 13.2 | 2.5 | 34.4 |
| apartment-keys | 8.7 | 5.6 | 7.2 | 6.8 | 3.8 | 32.1 |
| library-search | 5.6 | 0.0 | 0.0 | 0.2 | 0.1 | 5.9 |
| office-sequence | 27.1 | 19.9 | 0.0 | 13.7 | 4.1 | 64.8 |
| extreme-archive | 9.6 | 0.0 | 0.0 | 0.0 | 0.0 | 9.6 |
| vault-combination | 0.1 | 2.1 | 1.0 | 0.8 | 0.0 | 4.0 |
| backtracking-vault | 0.1 | 1.8 | 2.8 | 1.8 | 0.8 | 7.3 |
| **Global** | 8.9 | 3.7 | 1.5 | 4.7 | 1.4 | 20.2 |

## minimal_tool_repair / llama3.1

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 6.1 | 4.5 | 4.5 | 2,674 | 203 | 2,878 |
| color-locks | 10 | 1.0 | 0.0 | 19.0 | 33.4 | 33.4 | 24,828 | 747 | 25,575 |
| apartment-keys | 10 | 1.0 | 0.0 | 27.7 | 32.1 | 32.1 | 35,407 | 560 | 35,967 |
| library-search | 10 | 1.0 | 0.0 | 6.5 | 5.5 | 5.5 | 2,391 | 254 | 2,645 |
| office-sequence | 10 | 1.0 | 0.0 | 26.1 | 65.8 | 65.8 | 46,001 | 1,314 | 47,315 |
| extreme-archive | 10 | 1.0 | 0.0 | 2.0 | 1.0 | 1.0 | 735 | 36 | 771 |
| vault-combination | 10 | 1.0 | 0.0 | 38.6 | 31.6 | 31.6 | 48,571 | 693 | 49,265 |
| backtracking-vault | 10 | 1.0 | 0.0 | 33.6 | 30.2 | 30.2 | 44,700 | 668 | 45,368 |
| **Global** | 80 | 1.0 | 0.0 | 19.9 | 25.5 | 25.5 | 25,663 | 559 | 26,223 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1 | 10% | 10.0 | 28,788 | 61.0 | 45.0 | 45.0 |
| color-locks | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| apartment-keys | 10 | 2 | 20% | 5.0 | 179,838 | 138.5 | 160.5 | 160.5 |
| library-search | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| office-sequence | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| extreme-archive | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| **Global** | 80 | 3 | 4% | 26.7 | 699,293 | 532.0 | 680.3 | 680.3 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 18.3 | 24,677 | 528 | 25,206 |
| tool_call_repair | 1.6 | 985 | 31 | 1,016 |
| **Total** | 19.9 | 25,663 | 559 | 26,223 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 2.3 | 0.0 | 1.3 | 0.5 | 0.4 | 4.5 |
| color-locks | 18.5 | 0.0 | 0.0 | 13.0 | 1.9 | 33.4 |
| apartment-keys | 9.4 | 5.7 | 8.6 | 5.7 | 2.7 | 32.1 |
| library-search | 5.5 | 0.0 | 0.0 | 0.0 | 0.0 | 5.5 |
| office-sequence | 24.6 | 21.8 | 0.0 | 11.9 | 7.5 | 65.8 |
| extreme-archive | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| vault-combination | 14.6 | 6.1 | 6.5 | 4.3 | 0.1 | 31.6 |
| backtracking-vault | 11.3 | 5.0 | 6.1 | 4.6 | 3.2 | 30.2 |
| **Global** | 10.9 | 4.8 | 2.8 | 5.0 | 2.0 | 25.5 |

## minimal / qwen2.5:7b

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 5.0 | 4.0 | 4.0 | 2,970 | 157 | 3,128 |
| color-locks | 10 | 1.0 | 0.0 | 16.5 | 15.5 | 15.5 | 20,424 | 726 | 21,150 |
| apartment-keys | 10 | 1.0 | 0.0 | 25.0 | 24.1 | 24.1 | 38,238 | 1,295 | 39,533 |
| library-search | 10 | 1.0 | 0.0 | 19.9 | 18.9 | 18.9 | 35,949 | 1,235 | 37,184 |
| office-sequence | 10 | 1.0 | 0.0 | 20.7 | 19.8 | 19.8 | 32,680 | 1,011 | 33,692 |
| extreme-archive | 10 | 1.0 | 0.0 | 10.1 | 9.1 | 9.1 | 33,631 | 698 | 34,329 |
| vault-combination | 10 | 1.0 | 0.0 | 17.3 | 16.3 | 16.3 | 25,088 | 1,209 | 26,297 |
| backtracking-vault | 10 | 1.0 | 0.0 | 21.5 | 20.5 | 20.5 | 40,062 | 1,612 | 41,674 |
| **Global** | 80 | 1.0 | 0.0 | 17.0 | 16.0 | 16.0 | 28,630 | 993 | 29,623 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 3,128 | 5.0 | 4.0 | 4.0 |
| color-locks | 10 | 7 | 70% | 1.4 | 30,215 | 23.6 | 22.1 | 22.1 |
| apartment-keys | 10 | 4 | 40% | 2.5 | 98,833 | 62.5 | 60.2 | 60.2 |
| library-search | 10 | 1 | 10% | 10.0 | 371,846 | 199.0 | 189.0 | 189.0 |
| office-sequence | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| extreme-archive | 10 | 3 | 30% | 3.3 | 114,431 | 33.7 | 30.3 | 30.3 |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| **Global** | 80 | 25 | 31% | 3.2 | 94,796 | 54.4 | 51.3 | 51.3 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 17.0 | 28,630 | 993 | 29,623 |
| **Total** | 17.0 | 28,630 | 993 | 29,623 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.0 | 0.0 | 1.0 | 1.0 | 1.0 | 4.0 |
| color-locks | 5.0 | 0.0 | 1.2 | 4.1 | 5.2 | 15.5 |
| apartment-keys | 6.1 | 8.7 | 4.1 | 1.0 | 4.2 | 24.1 |
| library-search | 6.3 | 0.0 | 1.1 | 6.3 | 5.2 | 18.9 |
| office-sequence | 2.5 | 6.3 | 5.2 | 2.3 | 3.5 | 19.8 |
| extreme-archive | 5.6 | 0.0 | 1.0 | 1.9 | 0.6 | 9.1 |
| vault-combination | 5.5 | 3.8 | 3.0 | 2.7 | 1.3 | 16.3 |
| backtracking-vault | 5.7 | 2.6 | 2.7 | 2.8 | 6.7 | 20.5 |
| **Global** | 4.7 | 2.7 | 2.4 | 2.8 | 3.5 | 16.0 |

## minimal_tool_repair / qwen2.5:7b

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 5.0 | 4.0 | 4.0 | 2,971 | 169 | 3,141 |
| color-locks | 10 | 1.0 | 0.0 | 16.1 | 15.1 | 15.1 | 20,288 | 741 | 21,029 |
| apartment-keys | 10 | 1.0 | 0.0 | 21.7 | 20.8 | 20.8 | 32,008 | 1,045 | 33,053 |
| library-search | 10 | 1.0 | 0.0 | 20.3 | 19.4 | 19.4 | 40,371 | 1,317 | 41,689 |
| office-sequence | 10 | 1.0 | 0.0 | 23.1 | 22.2 | 22.2 | 36,818 | 1,060 | 37,879 |
| extreme-archive | 10 | 1.0 | 0.0 | 14.6 | 13.6 | 13.6 | 43,047 | 1,098 | 44,146 |
| vault-combination | 10 | 1.0 | 0.0 | 16.5 | 15.5 | 15.5 | 23,954 | 1,060 | 25,014 |
| backtracking-vault | 10 | 1.0 | 0.0 | 25.0 | 24.3 | 24.3 | 53,886 | 1,959 | 55,845 |
| **Global** | 80 | 1.0 | 0.0 | 17.8 | 16.9 | 16.9 | 31,668 | 1,056 | 32,725 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 3,141 | 5.0 | 4.0 | 4.0 |
| color-locks | 10 | 7 | 70% | 1.4 | 30,042 | 23.0 | 21.6 | 21.6 |
| apartment-keys | 10 | 3 | 30% | 3.3 | 110,179 | 72.3 | 69.3 | 69.3 |
| library-search | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| office-sequence | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| extreme-archive | 10 | 2 | 20% | 5.0 | 220,731 | 73.0 | 68.0 | 68.0 |
| vault-combination | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 10 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| **Global** | 80 | 22 | 28% | 3.6 | 119,000 | 64.7 | 61.3 | 61.3 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 17.8 | 31,661 | 1,056 | 32,717 |
| tool_call_repair | 0.0 | 7 | 0 | 7 |
| **Total** | 17.8 | 31,668 | 1,056 | 32,725 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.0 | 0.0 | 1.0 | 1.0 | 1.0 | 4.0 |
| color-locks | 5.3 | 0.0 | 1.1 | 3.9 | 4.8 | 15.1 |
| apartment-keys | 5.5 | 7.4 | 5.0 | 1.3 | 1.6 | 20.8 |
| library-search | 5.8 | 0.0 | 1.1 | 6.6 | 5.9 | 19.4 |
| office-sequence | 5.2 | 8.2 | 4.6 | 2.4 | 1.8 | 22.2 |
| extreme-archive | 5.9 | 0.0 | 1.1 | 3.6 | 3.0 | 13.6 |
| vault-combination | 4.8 | 6.2 | 3.3 | 0.8 | 0.4 | 15.5 |
| backtracking-vault | 6.4 | 1.8 | 3.0 | 6.1 | 7.0 | 24.3 |
| **Global** | 5.0 | 3.0 | 2.5 | 3.2 | 3.2 | 16.9 |
