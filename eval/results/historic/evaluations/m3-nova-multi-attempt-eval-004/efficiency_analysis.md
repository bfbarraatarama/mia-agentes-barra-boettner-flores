# Análisis de consumo y eficiencia — M3

**Run:** `m3-nova-multi-attempt-run-004`

## minimal / nova-lite

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 5.7 | 4.7 | 4.7 | 6,006 | 301 | 6,308 |
| color-locks | 10 | 1.9 | 0.0 | 25.5 | 27.8 | 27.8 | 76,391 | 1,781 | 78,173 |
| apartment-keys | 10 | 1.0 | 0.0 | 16.0 | 16.1 | 16.1 | 30,791 | 879 | 31,670 |
| library-search | 10 | 1.0 | 0.0 | 31.1 | 31.4 | 31.4 | 154,432 | 2,162 | 156,595 |
| office-sequence | 10 | 2.9 | 0.0 | 39.3 | 37.9 | 37.9 | 116,805 | 1,911 | 118,717 |
| extreme-archive | 10 | 1.0 | 0.0 | 27.0 | 26.4 | 26.4 | 214,765 | 2,351 | 217,117 |
| vault-combination | 10 | 1.0 | 0.0 | 34.2 | 45.3 | 45.3 | 105,858 | 2,159 | 108,017 |
| backtracking-vault | 10 | 1.0 | 0.0 | 35.6 | 35.2 | 35.2 | 102,506 | 1,910 | 104,417 |
| **Global** | 80 | 1.4 | 0.0 | 26.8 | 28.1 | 28.1 | 100,944 | 1,682 | 102,626 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 6,308 | 5.7 | 4.7 | 4.7 |
| color-locks | 10 | 8 | 80% | 2.4 | 97,716 | 31.9 | 34.8 | 34.8 |
| apartment-keys | 10 | 9 | 90% | 1.1 | 35,189 | 17.8 | 17.9 | 17.9 |
| library-search | 10 | 4 | 40% | 2.5 | 391,488 | 77.8 | 78.5 | 78.5 |
| office-sequence | 10 | 8 | 80% | 3.6 | 148,396 | 49.1 | 47.4 | 47.4 |
| extreme-archive | 10 | 8 | 80% | 1.2 | 271,396 | 33.8 | 33.0 | 33.0 |
| vault-combination | 10 | 4 | 40% | 2.5 | 270,043 | 85.5 | 113.2 | 113.2 |
| backtracking-vault | 10 | 4 | 40% | 2.5 | 261,043 | 89.0 | 88.0 | 88.0 |
| **Global** | 80 | 55 | 69% | 2.0 | 149,275 | 39.0 | 40.9 | 40.9 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 26.8 | 100,944 | 1,682 | 102,626 |
| **Total** | 26.8 | 100,944 | 1,682 | 102,626 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.1 | 0.0 | 1.0 | 1.0 | 1.6 | 4.7 |
| color-locks | 10.2 | 0.0 | 3.9 | 3.9 | 9.8 | 27.8 |
| apartment-keys | 1.0 | 7.4 | 3.9 | 1.0 | 2.8 | 16.1 |
| library-search | 17.3 | 0.0 | 5.1 | 6.8 | 2.2 | 31.4 |
| office-sequence | 2.2 | 19.8 | 10.4 | 3.2 | 2.3 | 37.9 |
| extreme-archive | 22.0 | 0.0 | 2.8 | 0.8 | 0.8 | 26.4 |
| vault-combination | 4.2 | 19.8 | 6.9 | 6.4 | 8.0 | 45.3 |
| backtracking-vault | 6.2 | 16.3 | 5.7 | 2.5 | 4.5 | 35.2 |
| **Global** | 8.0 | 7.9 | 5.0 | 3.2 | 4.0 | 28.1 |

## minimal_tool_repair / nova-lite

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 6.7 | 5.7 | 5.7 | 7,791 | 369 | 8,160 |
| color-locks | 10 | 1.0 | 0.0 | 27.2 | 28.4 | 28.4 | 90,732 | 1,818 | 92,550 |
| apartment-keys | 10 | 1.0 | 0.0 | 15.5 | 16.6 | 16.6 | 29,154 | 838 | 29,992 |
| library-search | 10 | 1.0 | 0.0 | 34.2 | 33.9 | 33.9 | 191,225 | 2,541 | 193,766 |
| office-sequence | 10 | 1.0 | 0.0 | 38.1 | 39.3 | 39.3 | 111,738 | 1,895 | 113,633 |
| extreme-archive | 10 | 1.0 | 0.0 | 26.0 | 25.1 | 25.1 | 196,690 | 1,918 | 198,609 |
| vault-combination | 10 | 1.0 | 0.0 | 31.8 | 37.1 | 37.1 | 91,175 | 1,848 | 93,023 |
| backtracking-vault | 10 | 1.0 | 0.0 | 33.7 | 33.1 | 33.1 | 100,263 | 1,966 | 102,229 |
| **Global** | 80 | 1.0 | 0.0 | 26.6 | 27.4 | 27.4 | 102,346 | 1,649 | 103,995 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 8,160 | 6.7 | 5.7 | 5.7 |
| color-locks | 10 | 6 | 60% | 1.7 | 154,251 | 45.3 | 47.3 | 47.3 |
| apartment-keys | 10 | 9 | 90% | 1.1 | 33,325 | 17.2 | 18.4 | 18.4 |
| library-search | 10 | 3 | 30% | 3.3 | 645,888 | 114.0 | 113.0 | 113.0 |
| office-sequence | 10 | 7 | 70% | 1.4 | 162,333 | 54.4 | 56.1 | 56.1 |
| extreme-archive | 10 | 9 | 90% | 1.1 | 220,677 | 28.9 | 27.9 | 27.9 |
| vault-combination | 10 | 6 | 60% | 1.7 | 155,039 | 53.0 | 61.8 | 61.8 |
| backtracking-vault | 10 | 6 | 60% | 1.7 | 170,383 | 56.2 | 55.2 | 55.2 |
| **Global** | 80 | 56 | 70% | 1.4 | 148,565 | 38.1 | 39.1 | 39.1 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 26.6 | 102,346 | 1,649 | 103,995 |
| **Total** | 26.6 | 102,346 | 1,649 | 103,995 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.2 | 0.0 | 1.4 | 1.0 | 2.1 | 5.7 |
| color-locks | 9.3 | 0.0 | 6.7 | 3.2 | 9.2 | 28.4 |
| apartment-keys | 1.0 | 8.9 | 3.4 | 1.1 | 2.2 | 16.6 |
| library-search | 24.2 | 0.0 | 2.1 | 1.8 | 5.8 | 33.9 |
| office-sequence | 4.2 | 18.2 | 10.3 | 2.9 | 3.7 | 39.3 |
| extreme-archive | 22.1 | 0.0 | 1.0 | 0.9 | 1.1 | 25.1 |
| vault-combination | 3.8 | 14.4 | 6.7 | 5.0 | 7.2 | 37.1 |
| backtracking-vault | 6.8 | 9.9 | 8.1 | 2.9 | 5.4 | 33.1 |
| **Global** | 9.1 | 6.4 | 5.0 | 2.4 | 4.6 | 27.4 |
