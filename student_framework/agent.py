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


    def _trim_run_history(
        self,
        target_length: int,
        protected_start: int | None = None,
    ) -> bool:
        """Reduce el historial de run hasta una longitud objetivo.

        Mientras exista exceso, elimina primero las trazas intermedias
        completas, desde la más antigua. Cuando ya no quedan trazas
        eliminables, alterna la eliminación del user más antiguo y de
        la respuesta final más antigua.

        Los mensajes ubicados desde protected_start permanecen
        protegidos.

        Devuelve True si fue posible alcanzar la longitud objetivo.
        """

        if target_length < 0:
            raise ValueError("target_length no puede ser negativo.")

        if protected_start is None:
            protected_start = len(self._history)

        if not 0 <= protected_start <= len(self._history):
            raise ValueError("protected_start está fuera del historial.")

        def oldest_trace_range(stop: int) -> tuple[int, int] | None:
            """Encuentra la traza completa más antigua antes de stop."""

            index = 0

            while index < stop:
                if self._history[index].get("role") != "user":
                    index += 1
                    continue

                final_index: int | None = None
                cursor = index + 1

                while cursor < stop:
                    message = self._history[cursor]

                    if message.get("role") == "user":
                        break

                    if (
                        message.get("role") == "assistant"
                        and not message.get("tool_calls")
                    ):
                        final_index = cursor
                        break

                    cursor += 1

                if final_index is not None:
                    if final_index > index + 1:
                        return index + 1, final_index

                    index = final_index + 1
                    continue

                index += 1

            return None

        def oldest_user_index(stop: int) -> int | None:
            """Encuentra el user eliminable más antiguo."""

            return next(
                (
                    index
                    for index, message in enumerate(
                        self._history[:stop]
                    )
                    if message.get("role") == "user"
                ),
                None,
            )

        def oldest_final_response_index(stop: int) -> int | None:
            """Encuentra la respuesta final eliminable más antigua."""

            return next(
                (
                    index
                    for index, message in enumerate(
                        self._history[:stop]
                    )
                    if (
                        message.get("role") == "assistant"
                        and not message.get("tool_calls")
                    )
                ),
                None,
            )

        while len(self._history) > target_length:
            trace_range = oldest_trace_range(protected_start)

            if trace_range is None:
                break

            start, end = trace_range
            removed_messages = end - start

            del self._history[start:end]
            protected_start -= removed_messages

        remove_user_next = True

        while len(self._history) > target_length:
            if remove_user_next:
                removable_index = oldest_user_index(protected_start)

                if removable_index is None:
                    removable_index = oldest_final_response_index(
                        protected_start
                    )
            else:
                removable_index = oldest_final_response_index(
                    protected_start
                )

                if removable_index is None:
                    removable_index = oldest_user_index(protected_start)

            if removable_index is None:
                return False

            removed_role = self._history[removable_index].get("role")

            del self._history[removable_index]
            protected_start -= 1

            remove_user_next = removed_role != "user"

        return True


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

        if self._max_history_messages < 1:
            raise ValueError(
                "max_history_messages debe ser al menos 1 para run()."
            )

        self._history.append({
            "role": "user",
            "content": user_message,
        })
        active_turn_start = len(self._history) - 1

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
                self._history.append({
                    "role": "assistant",
                    "content": response.content,
                })

                history_was_trimmed = self._trim_run_history(
                    target_length=self._max_history_messages - 1,
                )

                if not history_was_trimmed:
                    raise RuntimeError(
                        "No se pudo reducir el historial cerrado hasta la longitud objetivo."
                    )

                return AgentResult(
                    answer=response.content,
                    steps=steps,
                    input_tokens=total_in,
                    output_tokens=total_out,
                )

            # Verificación de espacio antes de ejecutar herramientas
            messages_to_add = 1 + len(response.tool_calls)
            target_length = (
                self._max_history_messages
                - messages_to_add
            )

            history_length_before_trim = len(self._history)

            history_was_trimmed = (
                target_length >= 0
                and self._trim_run_history(
                    target_length=target_length,
                    protected_start=active_turn_start,
                )
            )

            if not history_was_trimmed:
                error_message = (
                    "Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages="
                    f"{self._max_history_messages}."
                )

                self._history.append({
                    "role": "assistant",
                    "content": error_message,
                })

                closed_history_was_trimmed = self._trim_run_history(
                    target_length=self._max_history_messages - 1,
                )

                if not closed_history_was_trimmed:
                    raise RuntimeError(
                        "No se pudo reducir el historial cerrado hasta la longitud objetivo."
                    )

                return AgentResult(
                    answer=error_message,
                    steps=steps,
                    input_tokens=total_in,
                    output_tokens=total_out,
                    error=error_message,
                )

            removed_messages = (
                history_length_before_trim
                - len(self._history)
            )
            active_turn_start -= removed_messages

            # Expansión del historial con llamados a herramientas
            self._history.append({
                'role': 'assistant',
                'content': response.content,
                'tool_calls': [
                    {
                        'id': tool.id,
                        'type': 'function',
                        'function': {
                            'name': tool.name,
                            'arguments': tool.arguments,
                        },
                    }
                    for tool in response.tool_calls
                ],
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


    def _structured_call_messages(
        self,
        initial_message: dict[str, Any],
        repair_blocks: list[list[dict[str, Any]]],
    ) -> list[dict[str, Any]]:
        """Construye el contexto de structured_call sin fragmentar bloques.

        El bloque de reparación más reciente tiene prioridad. Después se
        conserva el mensaje inicial y, si todavía hay espacio, se agregan
        bloques anteriores completos desde el más reciente.

        Cuando el bloque más reciente no entra completo, se usa su último
        mensaje user como representación compacta y autosuficiente.
        """

        if not repair_blocks:
            return [initial_message]

        latest_block = repair_blocks[-1]

        if len(latest_block) > self._max_history_messages:
            repair_message = latest_block[-1]

            if self._max_history_messages >= 2:
                return [
                    initial_message,
                    repair_message,
                ]

            return [repair_message]

        selected_blocks = [latest_block]
        remaining_messages = (
            self._max_history_messages
            - len(latest_block)
        )

        include_initial_message = remaining_messages >= 1

        if include_initial_message:
            remaining_messages -= 1

        for block in reversed(repair_blocks[:-1]):
            if len(block) > remaining_messages:
                break

            selected_blocks.append(block)
            remaining_messages -= len(block)

        selected_blocks.reverse()

        messages: list[dict[str, Any]] = []

        if include_initial_message:
            messages.append(initial_message)

        for block in selected_blocks:
            messages.extend(block)

        return messages


    def _structured_call_repair_message(
        self,
        *,
        prompt: str,
        error: str,
        instruction: str,
    ) -> dict[str, str]:
        """Construye un mensaje de reparación autosuficiente."""

        return {
            "role": "user",
            "content": (
                f"Solicitud original:\n{prompt}\n\n"
                f"Error detectado: {error}\n"
                f"{instruction}"
            ),
        }


    def structured_call(
        self,
        prompt: str,
        schema: Any,
        max_repair_attempts: int = 2,
    ) -> Any:
        
        if self._max_history_messages < 1:
            raise ValueError(
                "max_history_messages debe ser al menos 1 para structured_call()."
            )

        final_tool = final_result_tool_schema(schema)
        initial_message = {
            "role": "user",
            "content": prompt,
        }
        repair_blocks: list[list[dict[str, Any]]] = []
        last_error: str = "Sin respuesta"

        for _ in range(max_repair_attempts + 1):
            messages = self._structured_call_messages(
                initial_message=initial_message,
                repair_blocks=repair_blocks,
            )

            response = self._chat_with_retry(
                messages=messages,
                tools=[final_tool],
                system=self._system,
            )

            final_call = next(
                (tc for tc in response.tool_calls if tc.name == FINAL_RESULT_TOOL_NAME),
                None,
            )

            if final_call is None:
                last_error = "El modelo respondió con texto libre en lugar de invocar final_result."

                repair_blocks.append([
                    {
                        "role": "assistant",
                        "content": response.content or "",
                    },
                    self._structured_call_repair_message(
                        prompt=prompt,
                        error=last_error,
                        instruction=(
                            "Tenés que invocar la herramienta final_result."
                        ),
                    ),
                ])
                continue

            try:
                args = json.loads(final_call.arguments)
                return schema.model_validate(args)
            except (json.JSONDecodeError, ValidationError) as e:
                last_error = str(e)

                repair_blocks.append([
                    {
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
                    },
                    {
                        "role": "tool",
                        "tool_call_id": final_call.id,
                        "name": FINAL_RESULT_TOOL_NAME,
                        "content": (
                            f"Error de validación: {last_error}"
                        ),
                    },
                    self._structured_call_repair_message(
                        prompt=prompt,
                        error=last_error,
                        instruction=(
                            "Intentá de nuevo e invocá final_result con el formato correcto."
                        ),
                    ),
                ])

        raise ValueError(f"structured_call falló tras {max_repair_attempts + 1} intentos: {last_error}")
