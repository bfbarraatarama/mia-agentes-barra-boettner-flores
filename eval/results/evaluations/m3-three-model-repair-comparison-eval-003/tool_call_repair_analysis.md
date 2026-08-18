# Análisis de reparación de tool calls — M3

**Runs:** `m3-tool-repair-comparison-run-002`, `m3-nova-tool-repair-comparison-run-003`

## Resumen

| Métrica | Valor |
|---|---:|
| Trials totales | 480 |
| Trials con reparación | 33 |
| Llamadas físicas de reparación | 133 |
| Respuestas del LLM | 133 |
| Errores de llamada | 0 |
| Llamadas con usage completo | 133 |
| Llamadas sin usage completo | 0 |
| Tokens de entrada reportados | 79448 |
| Tokens de salida reportados | 2505 |
| Cobertura de tokens completa | sí |

## Por sistema

### `minimal` / `llama3.1`

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Trials con reparación | 0 |
| Llamadas físicas de reparación | 0 |
| Respuestas del LLM | 0 |
| Errores de llamada | 0 |
| Llamadas con usage completo | 0 |
| Llamadas sin usage completo | 0 |
| Tokens de entrada reportados | 0 |
| Tokens de salida reportados | 0 |
| Cobertura de tokens completa | sí |

### `minimal` / `qwen2.5:7b`

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Trials con reparación | 0 |
| Llamadas físicas de reparación | 0 |
| Respuestas del LLM | 0 |
| Errores de llamada | 0 |
| Llamadas con usage completo | 0 |
| Llamadas sin usage completo | 0 |
| Tokens de entrada reportados | 0 |
| Tokens de salida reportados | 0 |
| Cobertura de tokens completa | sí |

### `minimal` / `nova-lite`

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Trials con reparación | 0 |
| Llamadas físicas de reparación | 0 |
| Respuestas del LLM | 0 |
| Errores de llamada | 0 |
| Llamadas con usage completo | 0 |
| Llamadas sin usage completo | 0 |
| Tokens de entrada reportados | 0 |
| Tokens de salida reportados | 0 |
| Cobertura de tokens completa | sí |

### `minimal_tool_repair` / `llama3.1`

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Trials con reparación | 32 |
| Llamadas físicas de reparación | 132 |
| Respuestas del LLM | 132 |
| Errores de llamada | 0 |
| Llamadas con usage completo | 132 |
| Llamadas sin usage completo | 0 |
| Tokens de entrada reportados | 78867 |
| Tokens de salida reportados | 2490 |
| Cobertura de tokens completa | sí |

### `minimal_tool_repair` / `qwen2.5:7b`

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Trials con reparación | 1 |
| Llamadas físicas de reparación | 1 |
| Respuestas del LLM | 1 |
| Errores de llamada | 0 |
| Llamadas con usage completo | 1 |
| Llamadas sin usage completo | 0 |
| Tokens de entrada reportados | 581 |
| Tokens de salida reportados | 15 |
| Cobertura de tokens completa | sí |

### `minimal_tool_repair` / `nova-lite`

| Métrica | Valor |
|---|---:|
| Trials | 80 |
| Trials con reparación | 0 |
| Llamadas físicas de reparación | 0 |
| Respuestas del LLM | 0 |
| Errores de llamada | 0 |
| Llamadas con usage completo | 0 |
| Llamadas sin usage completo | 0 |
| Tokens de entrada reportados | 0 |
| Tokens de salida reportados | 0 |
| Cobertura de tokens completa | sí |
