# Análisis de consumo y eficiencia — M3

**Run:** `m3-baseline-run-001`

## minimal / llama3.1

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 5 | 1.0 | 0.0 | 3.0 | 2.6 | 2.6 | 1,049 | 170 | 1,220 |
| color-locks | 5 | 1.0 | 0.0 | 20.2 | 39.0 | 39.0 | 27,440 | 891 | 28,331 |
| apartment-keys | 5 | 1.0 | 0.0 | 22.4 | 27.8 | 27.8 | 25,179 | 505 | 25,685 |
| library-search | 5 | 1.0 | 0.0 | 8.0 | 7.0 | 7.0 | 3,311 | 313 | 3,625 |
| office-sequence | 5 | 1.0 | 0.0 | 31.2 | 64.4 | 64.4 | 53,083 | 1,261 | 54,345 |
| extreme-archive | 5 | 1.0 | 0.0 | 9.8 | 9.0 | 9.0 | 8,999 | 188 | 9,187 |
| vault-combination | 5 | 1.0 | 0.0 | 3.0 | 2.0 | 2.0 | 1,300 | 136 | 1,437 |
| backtracking-vault | 5 | 1.0 | 0.0 | 4.2 | 5.6 | 5.6 | 2,303 | 183 | 2,487 |
| **Global** | 40 | 1.0 | 0.0 | 12.7 | 19.7 | 19.7 | 15,333 | 456 | 15,789 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| color-locks | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| apartment-keys | 5 | 3 | 60% | 1.7 | 42,808 | 37.3 | 46.3 | 46.3 |
| library-search | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| office-sequence | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| extreme-archive | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| vault-combination | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| **Global** | 40 | 3 | 8% | 13.3 | 210,532 | 169.7 | 262.3 | 262.3 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| unknown | 12.7 | 15,333 | 456 | 15,789 |
| **Total** | 12.7 | 15,333 | 456 | 15,789 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.2 | 0.0 | 1.0 | 0.2 | 0.2 | 2.6 |
| color-locks | 17.2 | 0.0 | 0.0 | 16.0 | 5.8 | 39.0 |
| apartment-keys | 5.2 | 6.8 | 7.2 | 4.0 | 4.6 | 27.8 |
| library-search | 7.0 | 0.0 | 0.0 | 0.0 | 0.0 | 7.0 |
| office-sequence | 29.2 | 21.8 | 0.0 | 9.4 | 4.0 | 64.4 |
| extreme-archive | 9.0 | 0.0 | 0.0 | 0.0 | 0.0 | 9.0 |
| vault-combination | 0.0 | 0.0 | 1.0 | 1.0 | 0.0 | 2.0 |
| backtracking-vault | 0.2 | 2.6 | 2.0 | 0.8 | 0.0 | 5.6 |
| **Global** | 8.6 | 3.9 | 1.4 | 3.9 | 1.8 | 19.7 |

## minimal / qwen2.5:7b

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 5 | 1.0 | 0.0 | 5.0 | 4.0 | 4.0 | 2,971 | 154 | 3,126 |
| color-locks | 5 | 1.0 | 0.0 | 17.8 | 16.8 | 16.8 | 23,423 | 909 | 24,332 |
| apartment-keys | 5 | 1.0 | 0.0 | 29.0 | 28.2 | 28.2 | 50,697 | 1,498 | 52,195 |
| library-search | 5 | 1.0 | 0.0 | 16.2 | 15.2 | 15.2 | 24,694 | 1,009 | 25,703 |
| office-sequence | 5 | 1.0 | 0.0 | 20.8 | 19.8 | 19.8 | 27,849 | 889 | 28,738 |
| extreme-archive | 5 | 1.0 | 0.0 | 15.0 | 14.0 | 14.0 | 42,006 | 1,327 | 43,334 |
| vault-combination | 5 | 1.0 | 0.0 | 16.0 | 15.0 | 15.0 | 24,053 | 1,032 | 25,086 |
| backtracking-vault | 5 | 1.0 | 0.0 | 16.6 | 15.6 | 15.6 | 26,361 | 1,137 | 27,499 |
| **Global** | 40 | 1.0 | 0.0 | 17.1 | 16.1 | 16.1 | 27,757 | 994 | 28,751 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 5 | 5 | 100% | 1.0 | 3,126 | 5.0 | 4.0 | 4.0 |
| color-locks | 5 | 2 | 40% | 2.5 | 60,830 | 44.5 | 42.0 | 42.0 |
| apartment-keys | 5 | 1 | 20% | 5.0 | 260,976 | 145.0 | 141.0 | 141.0 |
| library-search | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| office-sequence | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| extreme-archive | 5 | 1 | 20% | 5.0 | 216,671 | 75.0 | 70.0 | 70.0 |
| vault-combination | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| backtracking-vault | 5 | 0 | 0% | N/A | N/A | N/A | N/A | N/A |
| **Global** | 40 | 9 | 22% | 4.4 | 127,786 | 75.8 | 71.4 | 71.4 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| unknown | 17.1 | 27,757 | 994 | 28,751 |
| **Total** | 17.1 | 27,757 | 994 | 28,751 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.0 | 0.0 | 1.0 | 1.0 | 1.0 | 4.0 |
| color-locks | 5.2 | 0.0 | 1.2 | 4.6 | 5.8 | 16.8 |
| apartment-keys | 5.0 | 7.6 | 8.8 | 2.2 | 4.6 | 28.2 |
| library-search | 5.8 | 0.0 | 1.8 | 6.2 | 1.4 | 15.2 |
| office-sequence | 4.4 | 9.2 | 3.8 | 1.8 | 0.6 | 19.8 |
| extreme-archive | 4.8 | 0.0 | 1.4 | 3.4 | 4.4 | 14.0 |
| vault-combination | 4.8 | 5.6 | 2.0 | 1.0 | 1.6 | 15.0 |
| backtracking-vault | 6.4 | 1.6 | 1.6 | 2.2 | 3.8 | 15.6 |
| **Global** | 4.7 | 3.0 | 2.7 | 2.8 | 2.9 | 16.1 |
