"""Implementación de su agente.

Completen `register_tool` y `run` para el Milestone 1.
En el Milestone 2 amplíen `MyAgent` para que sea estatal y respete
`max_history_messages`.

Los tests de conformidad en `tests/conformance/test_m1.py` y
`test_m2.py` describen con precisión qué comportamientos deben funcionar
— léanlos antes de empezar.
"""

from __future__ import annotations

from typing import Any, Callable

from mia_agents.protocols import LLMClient
from mia_agents.types import AgentResult, ToolSchema, AgentStep
import json
from mia_agents.tool_schema import final_result_tool_schema, FINAL_RESULT_TOOL_NAME
from pydantic import ValidationError

class MyAgent:
    def __init__(
        self,
        llm_client: LLMClient,
        system_prompt: str = "Eres un asistente útil.",
        max_iterations: int = 10,
        max_history_messages: int = 50,
    ) -> None:
        """Inicializa el agente.

        Parameters
        ----------
        llm_client : LLMClient
            Cliente LLM (real o mock) que el agente utilizará.
        system_prompt : str
            System prompt por defecto.
        max_iterations : int
            Tope de iteraciones del bucle del agente (M1).
        max_history_messages : int
            Número máximo de mensajes que se permiten en la lista
            `messages` enviada al LLM en una única llamada. En M1 este
            valor es ignorado; el agente sólo necesita aceptarlo en su
            constructor. En M2 deben respetarlo: la longitud de la
            lista de mensajes pasada a `self._llm.chat(...)` no puede
            superar este número en ninguna llamada, sin importar la
            estrategia de memoria que elijan.
        """
        self._llm = llm_client
        self._system = system_prompt
        self._max_iterations = max_iterations
        self._max_history_messages = max_history_messages
        self._schemas: dict[str, ToolSchema] = {}
        self._tools: dict[str, Callable[..., str]] = {}
        self._history: list[dict[str, Any]] = []


    def register_tool(
        self,
        tool: Callable[..., str],
        schema: ToolSchema,
    ) -> None:
        """Registra una herramienta callable junto a su esquema.

        El esquema suele obtenerse con `ToolSchema.from_callable(fn)`. En
        `run`, pasá `tools=list(self._schemas.values())`; el cliente LLM
        aplica `to_llm_spec()` al llamar al proveedor.

        El callable se invoca con kwargs que coinciden con la firma.
        Debe devolver una cadena.
        """
        self._schemas[schema.name] = schema
        self._tools[schema.name] = tool

    def _clip(self, history: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Recorta el historial a una ventana deslizante de los últimos mensajes"""
        if self._max_history_messages <= 0:
            return []
        return history[-self._max_history_messages:]

    def _is_transient_error(self, error: Exception) -> bool:
        """Indica si un error parece temporal y puede reintentarse."""

        if isinstance(error, (TimeoutError, ConnectionError)):
            return True

        error_name = type(error).__name__.lower()

        transient_names = (
            "timeout",
            "connection",
            "ratelimit",
            "rate_limit",
            "throttling",
            "serviceunavailable",
        )

        if any(name in error_name for name in transient_names):
            return True

        status_code = getattr(error, "status_code", None)

        if status_code == 429:
            return True

        if isinstance(status_code, int) and 500 <= status_code <= 599:
            return True

        return False    

    def _chat_with_retry(
        self,
        *,
        messages: list[dict[str, Any]],
        tools: list[ToolSchema] | None = None,
        system: str | None = None,
        max_retries: int = 2,
    ):
        """Llama al LLM y reintenta únicamente ante errores transitorios."""

        for attempt in range(max_retries + 1):
            try:
                return self._llm.chat(
                    messages=messages,
                    tools=tools,
                    system=system,
                )

            except Exception as error:
                if not self._is_transient_error(error):
                    raise

                if attempt == max_retries:
                    raise

    def _tool_with_retry(
        self,
        tool_function: Callable[..., str],
        kwargs: dict[str, Any],
        max_retries: int = 2,
    ) -> str:
        """Ejecuta una herramienta y reintenta ante errores transitorios."""

        for attempt in range(max_retries + 1):
            try:
                return str(tool_function(**kwargs))

            except Exception as error:
                if not self._is_transient_error(error):
                    raise

                if attempt == max_retries:
                    raise

        raise RuntimeError("No se pudo ejecutar la herramienta.")                

    def run(self, user_message: str) -> AgentResult:
        """Ejecuta el bucle del agente hasta una respuesta final o hasta max_iterations.

        Comportamiento esperado (consulta tests/conformance/test_m1.py
        para el contrato exacto del M1):
          - Llama a `self._llm.chat(..., tools=list(self._schemas.values()))`.
          - Si la respuesta contiene tool_calls, ejecuta cada uno y vuelca
            los resultados en la siguiente llamada al chat.
          - Si la respuesta solo contiene texto (sin `tool_calls`),
            devuélvelo en `AgentResult.answer`. En M1 no uses la tool
            sintética `final_result`; ese patrón es de M2 (ver README y
            ENUNCIADO_M2.md).
          - Limita el bucle a `self._max_iterations` y termina de forma
            limpia cuando se alcance.
          - Registra cada invocación de herramienta como un `AgentStep`
            dentro de `result.steps`.

        En el M2, además, llamadas sucesivas sobre la misma instancia
        deben continuar la conversación, y la longitud de la lista de
        mensajes enviada al LLM no debe superar `self._max_history_messages`.
        Acumula los tokens de entrada/salida reportados por los
        `LLMResponse` y exponlos en `AgentResult.input_tokens` /
        `AgentResult.output_tokens`.
        """
        self._history.append({'role': 'user', 'content': user_message})
        total_in: int | None = None
        total_out: int | None = None

        steps : list[AgentStep] = []
        for _ in range(self._max_iterations):
            messages = self._clip(self._history)
            response = self._chat_with_retry(messages=messages, tools=list(self._schemas.values()), system= self._system)

            if response.input_tokens is not None or total_in is not None:
                total_in = (total_in or 0) + (response.input_tokens or 0)
            if response.output_tokens is not None or total_out is not None:
                total_out = (total_out or 0) + (response.output_tokens or 0)

            if not response.tool_calls:
                return AgentResult(
                    answer=response.content,
                    steps=steps,
                    input_tokens=total_in,
                    output_tokens=total_out)

            self._history.append({
                'role': 'assistant',
                'content': response.content,
                'tool_calls': [ { 'id': tool.id, 'name': tool.name, 'arguments': tool.arguments } for tool in response.tool_calls ]
            })

            for tool_call in response.tool_calls:
                error = None
                tool_output = ""

                try:
                    kwargs = json.loads(tool_call.arguments) if tool_call.arguments else {}

                    tool_function = self._tools.get(tool_call.name)

                    if tool_function is None:
                        error = f"Herramienta desconocida: {tool_call.name}"
                    else:
                        tool_output = self._tool_with_retry(
                                tool_function=tool_function,
                                kwargs=kwargs,
                            )

                except Exception as e:
                    error = str(e)

                step = AgentStep(
                    tool_name=tool_call.name,
                    tool_input=tool_call.arguments,
                    tool_output=tool_output,
                    error=error,
                )

                steps.append(step)

                self._history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.name,
                    "content": tool_output if error is None else error,
                })          


        return AgentResult(answer='', steps=steps, input_tokens=total_in, output_tokens=total_out)

    def structured_call(
        self,
        prompt: str,
        schema: Any,
        max_repair_attempts: int = 2,
    ) -> Any:
        
        final_tool = final_result_tool_schema(schema)
        messages = [{"role": "user", "content": prompt}]
        last_error: str = "Sin respuesta"

        for _ in range(max_repair_attempts + 1):
            response = self._chat_with_retry(
                messages=self._clip(messages),
                tools=[final_tool],
                system=self._system,
            )

            final_call = next(
                (tc for tc in response.tool_calls if tc.name == FINAL_RESULT_TOOL_NAME),
                None,
            )

            if final_call is None:
                last_error = "El modelo respondió con texto libre en lugar de invocar final_result."
                messages.append({"role": "assistant", "content": response.content or ""})
                messages.append({
                    "role": "user",
                    "content": f"Error: {last_error} Debes invocar la herramienta final_result.",
                })
                continue

            try:
                args = json.loads(final_call.arguments)
                return schema.model_validate(args)
            except (json.JSONDecodeError, ValidationError) as e:
                last_error = str(e)
                messages.append({
                    "role": "assistant",
                    "content": response.content,
                    "tool_calls": [{
                        "id": final_call.id,
                        "type": "function",
                        "function": {
                            "name": final_call.name,
                            "arguments": final_call.arguments,
                        },
                    }],
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": final_call.id,
                    "name": FINAL_RESULT_TOOL_NAME,
                    "content": f"Error de validación: {last_error}",
                })
                messages.append({
                    "role": "user",
                    "content": f"La respuesta no es válida: {last_error}. Intenta de nuevo con el formato correcto.",
                })

        raise ValueError(f"structured_call falló tras {max_repair_attempts + 1} intentos: {last_error}")
