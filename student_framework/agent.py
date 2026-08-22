"""Implementación de su agente.

Completen `register_tool` y `run` para el Milestone 1.
En el Milestone 2 amplíen `MyAgent` para que sea estatal y respete
`max_history_messages`.

Los tests de conformidad en `tests/conformance/test_m1.py` y
`test_m2.py` describen con precisión qué comportamientos deben funcionar
— léanlos antes de empezar.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from mia_agents.protocols import LLMClient
from mia_agents.types import AgentResult, ToolSchema, AgentStep
import json
from mia_agents.tool_schema import final_result_tool_schema
from pydantic import ValidationError
import inspect

class MyAgent:
    def __init__(
        self,
        llm_client: LLMClient,
        system_prompt: str = "Eres un asistente útil.",
        max_iterations: int = 10,
        max_history_messages: int = 50,
        tool_call_repair_max_attempts: int = 0,
        trace_callback: Callable[[dict[str, Any]], None] | None = None,
        history_compactor: Callable[[list[dict[str, Any]]], str] | None = None,
        compaction_keep_recent_rounds: int = 2,
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
        history_compactor : Callable | None
            Compactor opcional de historial (M3). Recibe la lista de
            mensajes que van a descartarse y devuelve un resumen en
            texto que los reemplaza como un único mensaje. Con None se
            conserva la política M2 de eliminación plana.
        compaction_keep_recent_rounds : int
            Cantidad de rondas de herramientas recientes del turno
            activo que la compactación intra-turno conserva en crudo.
        """
        self._llm = llm_client
        self._system = system_prompt
        self._max_iterations = max_iterations
        self._max_history_messages = max_history_messages
        if tool_call_repair_max_attempts < 0:
            raise ValueError(
                "tool_call_repair_max_attempts no puede ser negativo."
            )

        self._tool_call_repair_max_attempts = tool_call_repair_max_attempts

        if compaction_keep_recent_rounds < 0:
            raise ValueError(
                "compaction_keep_recent_rounds no puede ser negativo."
            )

        self._history_compactor = history_compactor
        self._compaction_keep_recent_rounds = compaction_keep_recent_rounds
        self._schemas: dict[str, ToolSchema] = {}
        self._tools: dict[str, Callable[..., str]] = {}
        self._history: list[dict[str, Any]] = []
        self._trace_callback = trace_callback
        self._run_response_callback: Callable[[Any], None] | None = None


    def set_history_compactor(
        self,
        history_compactor: Callable[[list[dict[str, Any]]], str] | None,
    ) -> None:
        """Configura el compactor después de la construcción.

        Necesario cuando el compactor usa el propio agente (p. ej. el
        resumidor por LLM) y no puede existir antes que la instancia.
        """
        self._history_compactor = history_compactor


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


    def _validate_tool_call(
        self,
        tool_call: Any,
    ) -> dict[str, Any]:
        if tool_call.name not in self._tools:
            raise ValueError(f"Herramienta desconocida: {tool_call.name}")

        try:
            kwargs = (
                json.loads(tool_call.arguments)
                if tool_call.arguments
                else {}
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Argumentos JSON inválidos: {e}") from e

        if not isinstance(kwargs, dict):
            raise ValueError(
                "Los argumentos de la herramienta deben ser un objeto JSON."
            )

        tool_function = self._tools[tool_call.name]

        try:
            inspect.signature(tool_function).bind(**kwargs)
        except TypeError as e:
            raise ValueError(str(e)) from e

        return kwargs


    def _repair_tool_call(
        self,
        tool_call: Any,
        error: str,
        max_attempts: int,
        response_callback: Callable[[Any], None] | None = None,
    ) -> Any:
        if max_attempts < 1:
            raise ValueError("max_attempts debe ser al menos 1.")

        tools = list(self._schemas.values())

        if not tools:
            raise ValueError(
                "No hay herramientas registradas disponibles para reparar la llamada."
            )

        prompt = (
            "Repará exclusivamente la siguiente llamada a herramienta para que "
            "respete alguna de las herramientas disponibles.\n\n"
            f"Herramienta original: {tool_call.name}\n"
            f"Argumentos originales: {tool_call.arguments}\n"
            f"Error detectado: {error}\n\n"
            "Preservá la intención de la llamada original. Podés cambiar la "
            "herramienta si la intención corresponde a otra de las disponibles. "
            "No avances la tarea ni agregues una acción nueva. Invocá una única "
            "herramienta disponible con argumentos válidos."
        )

        def validate_call(repaired_call: Any) -> Any:
            self._validate_tool_call(repaired_call)
            return repaired_call

        return self._structured_call_with_repair(
            prompt=prompt,
            tools=tools,
            validate_call=validate_call,
            max_repair_attempts=max_attempts - 1,
            response_callback=response_callback,
            purpose="tool_call_repair",
        )


    def _clip(self, history: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Recorta el historial a una ventana deslizante de los últimos mensajes"""
        if self._max_history_messages <= 0:
            return []
        return history[-self._max_history_messages:]


    def _compact_messages(
        self,
        evicted: list[dict[str, Any]],
    ) -> str | None:
        """Ejecuta el compactor sobre mensajes a descartar.

        Devuelve None si el compactor falla; el llamador decide el
        fallback (eliminación plana en la eviction, abortar en la
        compactación intra-turno). Un compactor roto degrada a la
        política M2, nunca corta el run con una excepción propia.
        """

        if self._history_compactor is None:
            return None

        try:
            summary = str(self._history_compactor(deepcopy(evicted)))

        except Exception as error:
            if self._trace_callback is not None:
                self._trace_callback({
                    "type": "history_compaction",
                    "evicted_messages": len(evicted),
                    "error": error,
                })

            return None

        if self._trace_callback is not None:
            self._trace_callback({
                "type": "history_compaction",
                "evicted_messages": len(evicted),
                "summary_chars": len(summary),
            })

        return summary


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

            # end - start >= 2: con un solo mensaje, reemplazarlo por
            # un resumen no reduce el historial y este while no
            # terminaría nunca.
            if (
                self._history_compactor is not None
                and end - start >= 2
            ):
                summary = self._compact_messages(
                    self._history[start:end]
                )

                if summary is not None:
                    # Rol user: con rol assistant sin tool_calls, el
                    # resumen sería la "respuesta final" que la segunda
                    # pasada elimina primero.
                    self._history[start:end] = [{
                        "role": "user",
                        "content": (
                            "[Resumen de contexto previo]\n"
                            f"{summary}"
                        ),
                    }]
                    protected_start -= end - start - 1
                    continue

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


    def _closed_tool_rounds(
        self,
        active_turn_start: int,
    ) -> list[tuple[int, int]]:
        """Encuentra las rondas de herramientas cerradas del turno activo.

        Una ronda es un mensaje assistant con tool_calls seguido de sus
        mensajes tool. Devuelve rangos [start, end) en orden.
        """

        rounds: list[tuple[int, int]] = []
        index = active_turn_start + 1

        while index < len(self._history):
            message = self._history[index]

            if (
                message.get("role") == "assistant"
                and message.get("tool_calls")
            ):
                end = index + 1

                while (
                    end < len(self._history)
                    and self._history[end].get("role") == "tool"
                ):
                    end += 1

                rounds.append((index, end))
                index = end
                continue

            index += 1

        return rounds


    def _compact_active_turn(
        self,
        *,
        active_turn_start: int,
        target_length: int,
    ) -> bool:
        """Compacta rondas ya consumidas del turno activo.

        Este es el caso que la política M2 no cubre: cuando todo el
        historial pertenece al turno activo, no hay trazas cerradas
        eliminables y el run moriría por presupuesto. Se reemplazan las
        rondas más viejas (junto con cualquier resumen previo
        intercalado) por un único mensaje de resumen, conservando las
        últimas compaction_keep_recent_rounds rondas en crudo. Si aun
        así no alcanza, una segunda pasada compacta todas las rondas.

        Las rondas se reemplazan siempre completas (assistant con
        tool_calls junto a todos sus resultados), así no quedan
        mensajes tool huérfanos ni respuestas multi-tool-call partidas.
        """

        if self._history_compactor is None:
            return False

        for keep_rounds in (self._compaction_keep_recent_rounds, 0):
            if len(self._history) <= target_length:
                return True

            rounds = self._closed_tool_rounds(active_turn_start)
            compactable = (
                rounds[:-keep_rounds] if keep_rounds > 0 else rounds
            )

            if not compactable:
                continue

            # Desde el primer mensaje posterior al user del turno: así
            # un resumen intra-turno anterior queda incluido y los
            # resúmenes se fusionan en vez de acumularse.
            start = active_turn_start + 1
            end = compactable[-1][1]

            if end - start < 2:
                continue

            summary = self._compact_messages(
                self._history[start:end]
            )

            if summary is None:
                return False

            self._history[start:end] = [{
                "role": "user",
                "content": (
                    "[Resumen de progreso del intento actual]\n"
                    f"{summary}"
                ),
            }]

        return len(self._history) <= target_length


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
        purpose: str = "agent",
    ):
        """Llama al LLM y reintenta únicamente ante errores transitorios."""

        for attempt in range(max_retries + 1):
            messages_snapshot = (
                deepcopy(messages)
                if self._trace_callback is not None
                else None
            )

            try:
                response = self._llm.chat(
                    messages=messages,
                    tools=tools,
                    system=system,
                )

            except Exception as error:
                if self._trace_callback is not None:
                    self._trace_callback({
                        "type": "llm_call",
                        "purpose": purpose,
                        "retry_index": attempt,
                        "messages": messages_snapshot,
                        "error": error,
                    })

                if not self._is_transient_error(error):
                    raise

                if attempt == max_retries:
                    raise

            else:
                if self._trace_callback is not None:
                    self._trace_callback({
                        "type": "llm_call",
                        "purpose": purpose,
                        "retry_index": attempt,
                        "messages": messages_snapshot,
                        "response": response,
                    })

                return response


    def _tool_with_retry(
        self,
        tool_name: str,
        tool_function: Callable[..., str],
        kwargs: dict[str, Any],
        max_retries: int = 2,
    ) -> str:
        """Ejecuta una herramienta y reintenta ante errores transitorios."""

        for attempt in range(max_retries + 1):
            arguments_snapshot = (
                deepcopy(kwargs)
                if self._trace_callback is not None
                else None
            )

            try:
                output = str(tool_function(**kwargs))

            except Exception as error:
                if self._trace_callback is not None:
                    self._trace_callback({
                        "type": "tool_execution",
                        "retry_index": attempt,
                        "tool_name": tool_name,
                        "arguments": arguments_snapshot,
                        "error": error,
                    })

                if not self._is_transient_error(error):
                    raise

                if attempt == max_retries:
                    raise

            else:
                if self._trace_callback is not None:
                    self._trace_callback({
                        "type": "tool_execution",
                        "retry_index": attempt,
                        "tool_name": tool_name,
                        "arguments": arguments_snapshot,
                        "output": output,
                    })

                return output

        raise RuntimeError("No se pudo ejecutar la herramienta.")                


    def _prepare_run_tool_context(
        self,
        *,
        active_turn_start: int,
        tool_call_count: int,
    ) -> int | None:
        """Libera espacio para una nueva ronda de herramientas.

        Devuelve el índice actualizado del comienzo del turno activo.
        Devuelve None si el turno no puede continuar dentro del límite.
        """

        messages_to_add = 1 + tool_call_count
        target_length = (
            self._max_history_messages
            - messages_to_add
        )

        if target_length < 0:
            return None

        history_length_before_trim = len(self._history)

        history_was_trimmed = self._trim_run_history(
            target_length=target_length,
            protected_start=active_turn_start,
        )

        # El trim solo remueve antes del turno activo; el ajuste va
        # antes de la compactación intra-turno, que remueve después y
        # no debe desplazar el índice.
        removed_messages = (
            history_length_before_trim
            - len(self._history)
        )
        active_turn_start -= removed_messages

        if not history_was_trimmed:
            history_was_trimmed = self._compact_active_turn(
                active_turn_start=active_turn_start,
                target_length=target_length,
            )

        if not history_was_trimmed:
            return None

        return active_turn_start


    def _trim_closed_run_history(self) -> None:
        """Reserva espacio para el próximo mensaje user."""

        history_was_trimmed = self._trim_run_history(
            target_length=self._max_history_messages - 1,
        )

        if not history_was_trimmed:
            raise RuntimeError(
                "No se pudo reducir el historial cerrado "
                "hasta la longitud objetivo."
            )


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

        def accumulate_response_tokens(response: Any) -> None:
            nonlocal total_in, total_out

            if response.input_tokens is not None or total_in is not None:
                total_in = (total_in or 0) + (response.input_tokens or 0)
            if response.output_tokens is not None or total_out is not None:
                total_out = (total_out or 0) + (response.output_tokens or 0)

        # Visible para el compactor por LLM, que corre dentro del
        # trimming y no puede recibir la clausura por parámetro; sin
        # esto sus tokens quedarían fuera de AgentResult.
        self._run_response_callback = accumulate_response_tokens

        steps : list[AgentStep] = []
        for _ in range(self._max_iterations):
            messages = self._clip(self._history)
            response = self._chat_with_retry(messages=messages, tools=list(self._schemas.values()), system= self._system)

            accumulate_response_tokens(response)

            if not response.tool_calls:
                self._history.append({
                    "role": "assistant",
                    "content": response.content,
                })

                self._trim_closed_run_history()

                return AgentResult(
                    answer=response.content,
                    steps=steps,
                    input_tokens=total_in,
                    output_tokens=total_out,
                )

            effective_tool_calls = response.tool_calls

            if self._tool_call_repair_max_attempts > 0:
                effective_tool_calls = []

                for tool_call in response.tool_calls:
                    effective_tool_call = tool_call

                    try:
                        self._validate_tool_call(tool_call)
                    except ValueError as e:
                        try:
                            effective_tool_call = self._repair_tool_call(
                                tool_call=tool_call,
                                error=str(e),
                                max_attempts=self._tool_call_repair_max_attempts,
                                response_callback=accumulate_response_tokens,
                            )
                        except ValueError:
                            pass

                    effective_tool_calls.append(effective_tool_call)

            prepared_turn_start = self._prepare_run_tool_context(
                active_turn_start=active_turn_start,
                tool_call_count=len(effective_tool_calls),
            )

            if prepared_turn_start is None:
                error_message = (
                    "Se requirió una herramienta, pero el contexto necesario para continuar no cabe en max_history_messages="
                    f"{self._max_history_messages}."
                )

                self._history.append({
                    "role": "assistant",
                    "content": error_message,
                })

                self._trim_closed_run_history()

                return AgentResult(
                    answer=error_message,
                    steps=steps,
                    input_tokens=total_in,
                    output_tokens=total_out,
                    error=error_message,
                )

            active_turn_start = prepared_turn_start

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
                    for tool in effective_tool_calls
                ],
            })

            for tool_call in effective_tool_calls:
                error = None
                tool_output = ""

                try:
                    kwargs = json.loads(tool_call.arguments) if tool_call.arguments else {}

                    tool_function = self._tools.get(tool_call.name)

                    if tool_function is None:
                        error = f"Herramienta desconocida: {tool_call.name}"
                    else:
                        tool_output = self._tool_with_retry(
                                tool_name=tool_call.name,
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


        message = (
            f"Se alcanzó el límite de {self._max_iterations} iteraciones sin obtener una respuesta final."
        )

        self._history.append({
            "role": "assistant",
            "content": message,
        })

        self._trim_closed_run_history()

        return AgentResult(
            answer=message,
            steps=steps,
            error=message,
            input_tokens=total_in,
            output_tokens=total_out,
        )


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


    def _structured_call_with_repair(
        self,
        prompt: str,
        tools: list[ToolSchema],
        validate_call: Callable[[Any], Any],
        max_repair_attempts: int = 2,
        response_callback: Callable[[Any], None] | None = None,
        purpose: str = "structured_call",
    ) -> Any:
        
        if self._max_history_messages < 1:
            raise ValueError(
                "max_history_messages debe ser al menos 1 para structured_call()."
            )

        tool_names = {tool.name for tool in tools}
        tool_names_text = ", ".join(tool.name for tool in tools)

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
                tools=tools,
                system=self._system,
                purpose=purpose,
            )

            if response_callback is not None:
                response_callback(response)

            final_call = next(
                (tc for tc in response.tool_calls if tc.name in tool_names),
                None,
            )

            if final_call is None:
                if len(tools) == 1:
                    last_error = (
                        f"El modelo respondió con texto libre en lugar de invocar {tools[0].name}."
                    )
                    instruction = (
                        f"Tenés que invocar la herramienta {tools[0].name}."
                    )
                else:
                    last_error = (
                        "El modelo no invocó ninguna de las herramientas disponibles: "
                        f"{tool_names_text}."
                    )
                    instruction = (
                        "Tenés que invocar una de las herramientas disponibles: "
                        f"{tool_names_text}."
                    )

                repair_blocks.append([
                    {
                        "role": "assistant",
                        "content": response.content or "",
                    },
                    self._structured_call_repair_message(
                        prompt=prompt,
                        error=last_error,
                        instruction=instruction,
                    ),
                ])
                continue

            try:
                return validate_call(final_call)
            except (json.JSONDecodeError, ValidationError, ValueError) as e:
                last_error = str(e)

                if len(tools) == 1:
                    instruction = (
                        f"Intentá de nuevo e invocá {tools[0].name} con el formato correcto."
                    )
                else:
                    instruction = (
                        "Intentá de nuevo e invocá una de las herramientas disponibles "
                        f"con el formato correcto: {tool_names_text}."
                    )

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
                        "name": final_call.name,
                        "content": (
                            f"Error de validación: {last_error}"
                        ),
                    },
                    self._structured_call_repair_message(
                        prompt=prompt,
                        error=last_error,
                        instruction=instruction,
                    ),
                ])

        raise ValueError(f"structured_call falló tras {max_repair_attempts + 1} intentos: {last_error}")


    def structured_call(
        self,
        prompt: str,
        schema: Any,
        max_repair_attempts: int = 2,
    ) -> Any:
        final_tool = final_result_tool_schema(schema)

        def validate_call(final_call: Any) -> Any:
            args = json.loads(final_call.arguments)
            return schema.model_validate(args)

        return self._structured_call_with_repair(
            prompt=prompt,
            tools=[final_tool],
            validate_call=validate_call,
            max_repair_attempts=max_repair_attempts,
        )