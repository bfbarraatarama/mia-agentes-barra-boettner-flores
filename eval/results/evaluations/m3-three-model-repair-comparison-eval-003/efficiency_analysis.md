# Análisis de consumo y eficiencia — M3

**Run:** `m3-nova-tool-repair-comparison-run-003`

## minimal / nova-lite

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 6.5 | 5.5 | 5.5 | 7,404 | 342 | 7,747 |
| color-locks | 10 | 1.0 | 0.0 | 27.6 | 29.2 | 29.2 | 92,525 | 1,976 | 94,501 |
| apartment-keys | 10 | 1.0 | 0.0 | 13.6 | 12.8 | 12.8 | 21,746 | 701 | 22,448 |
| library-search | 10 | 1.0 | 0.0 | 19.0 | 21.2 | 21.2 | 76,375 | 1,370 | 77,745 |
| office-sequence | 10 | 1.0 | 0.0 | 40.0 | 41.0 | 41.0 | 117,302 | 1,905 | 119,207 |
| extreme-archive | 10 | 1.0 | 0.0 | 22.6 | 23.6 | 23.6 | 187,606 | 1,841 | 189,448 |
| vault-combination | 10 | 1.0 | 0.0 | 33.5 | 43.7 | 43.7 | 102,268 | 2,075 | 104,344 |
| backtracking-vault | 10 | 1.0 | 0.0 | 33.8 | 33.1 | 33.1 | 96,674 | 1,890 | 98,564 |
| **Global** | 80 | 1.0 | 0.0 | 24.6 | 26.3 | 26.3 | 87,738 | 1,512 | 89,250 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 7,747 | 6.5 | 5.5 | 5.5 |
| color-locks | 10 | 6 | 60% | 1.7 | 157,503 | 46.0 | 48.7 | 48.7 |
| apartment-keys | 10 | 10 | 100% | 1.0 | 22,448 | 13.6 | 12.8 | 12.8 |
| library-search | 10 | 9 | 90% | 1.1 | 86,384 | 21.1 | 23.6 | 23.6 |
| office-sequence | 10 | 7 | 70% | 1.4 | 170,296 | 57.1 | 58.6 | 58.6 |
| extreme-archive | 10 | 10 | 100% | 1.0 | 189,448 | 22.6 | 23.6 | 23.6 |
| vault-combination | 10 | 4 | 40% | 2.5 | 260,860 | 83.8 | 109.2 | 109.2 |
| backtracking-vault | 10 | 9 | 90% | 1.1 | 109,516 | 37.6 | 36.8 | 36.8 |
| **Global** | 80 | 65 | 81% | 1.2 | 109,847 | 30.2 | 32.3 | 32.3 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 24.6 | 87,738 | 1,512 | 89,250 |
| **Total** | 24.6 | 87,738 | 1,512 | 89,250 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.4 | 0.0 | 1.2 | 1.0 | 1.9 | 5.5 |
| color-locks | 10.5 | 0.0 | 6.0 | 3.1 | 9.6 | 29.2 |
| apartment-keys | 1.3 | 5.6 | 3.4 | 1.0 | 1.5 | 12.8 |
| library-search | 13.4 | 0.0 | 1.3 | 1.9 | 4.6 | 21.2 |
| office-sequence | 3.1 | 22.3 | 10.2 | 2.7 | 2.7 | 41.0 |
| extreme-archive | 20.3 | 0.0 | 1.2 | 1.0 | 1.1 | 23.6 |
| vault-combination | 3.0 | 20.5 | 7.6 | 4.9 | 7.7 | 43.7 |
| backtracking-vault | 7.6 | 10.0 | 5.2 | 4.1 | 6.2 | 33.1 |
| **Global** | 7.6 | 7.3 | 4.5 | 2.5 | 4.4 | 26.3 |

## minimal_tool_repair / nova-lite

### Consumo por escenario

*Valores promedio por trial. **Attempts**: número de veces que el agente intentó resolver el escenario dentro del mismo trial. **Retries**: número de llamadas al LLM que debieron reintentarse por cualquier error en la respuesta del proveedor (timeout, rate limit, respuesta malformada, etc.).*

| Escenario | Trials | Attempts | Retries | LLM calls | Tools | Steps | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 1.0 | 0.0 | 5.8 | 4.8 | 4.8 | 6,147 | 308 | 6,455 |
| color-locks | 10 | 1.0 | 0.0 | 32.6 | 33.0 | 33.0 | 106,828 | 2,433 | 109,262 |
| apartment-keys | 10 | 1.0 | 0.0 | 21.5 | 21.4 | 21.4 | 47,923 | 1,095 | 49,019 |
| library-search | 10 | 1.0 | 0.0 | 25.4 | 28.5 | 28.5 | 133,934 | 1,938 | 135,872 |
| office-sequence | 10 | 1.0 | 0.0 | 35.3 | 36.2 | 36.2 | 99,259 | 1,731 | 100,990 |
| extreme-archive | 10 | 1.0 | 0.0 | 26.2 | 25.4 | 25.4 | 198,644 | 2,080 | 200,725 |
| vault-combination | 10 | 1.0 | 0.0 | 36.0 | 38.6 | 38.6 | 108,919 | 2,028 | 110,947 |
| backtracking-vault | 10 | 1.0 | 0.0 | 33.4 | 34.3 | 34.3 | 97,463 | 1,951 | 99,415 |
| **Global** | 80 | 1.0 | 0.0 | 27.0 | 27.8 | 27.8 | 99,890 | 1,695 | 101,586 |

### Eficiencia por escenario

*Las métricas por éxito se calculan como el consumo total de todos los trials dividido por la cantidad de trials exitosos.*

| Escenario | Trials | Successes | Success rate | Attempts / success | Tokens / success | LLM calls / success | Tools / success | Steps / success |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| study-with-key | 10 | 10 | 100% | 1.0 | 6,455 | 5.8 | 4.8 | 4.8 |
| color-locks | 10 | 4 | 40% | 2.5 | 273,156 | 81.5 | 82.5 | 82.5 |
| apartment-keys | 10 | 9 | 90% | 1.1 | 54,466 | 23.9 | 23.8 | 23.8 |
| library-search | 10 | 6 | 60% | 1.7 | 226,454 | 42.3 | 47.5 | 47.5 |
| office-sequence | 10 | 7 | 70% | 1.4 | 144,272 | 50.4 | 51.7 | 51.7 |
| extreme-archive | 10 | 8 | 80% | 1.2 | 250,907 | 32.8 | 31.8 | 31.8 |
| vault-combination | 10 | 2 | 20% | 5.0 | 554,737 | 180.0 | 193.0 | 193.0 |
| backtracking-vault | 10 | 7 | 70% | 1.4 | 142,021 | 47.7 | 49.0 | 49.0 |
| **Global** | 80 | 53 | 66% | 1.5 | 153,337 | 40.8 | 41.9 | 41.9 |

### Consumo LLM por purpose

*Valores promedio por trial, global.*

| Purpose | LLM calls | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|---:|
| agent | 27.0 | 99,890 | 1,695 | 101,586 |
| **Total** | 27.0 | 99,890 | 1,695 | 101,586 |

### Uso de herramientas por escenario

*Executions promedio por trial.*

| Escenario | examine | go | look | take | use | Total |
|---|---:|---:|---:|---:|---:|---:|
| study-with-key | 1.2 | 0.0 | 1.0 | 1.0 | 1.6 | 4.8 |
| color-locks | 18.8 | 0.0 | 2.4 | 2.4 | 9.4 | 33.0 |
| apartment-keys | 1.0 | 12.7 | 3.7 | 1.0 | 3.0 | 21.4 |
| library-search | 21.2 | 0.0 | 2.1 | 1.9 | 3.3 | 28.5 |
| office-sequence | 2.5 | 20.9 | 6.7 | 2.7 | 3.4 | 36.2 |
| extreme-archive | 22.3 | 0.0 | 1.2 | 0.9 | 1.0 | 25.4 |
| vault-combination | 3.3 | 19.0 | 6.5 | 4.5 | 5.3 | 38.6 |
| backtracking-vault | 6.2 | 10.5 | 6.3 | 4.5 | 6.8 | 34.3 |
| **Global** | 9.6 | 7.9 | 3.7 | 2.4 | 4.2 | 27.8 |
