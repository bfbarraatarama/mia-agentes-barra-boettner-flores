"""Compactación de historial para ejecuciones de horizonte largo (M3).

Dos variantes de compactor para `MyAgent(history_compactor=...)`:

- `deterministic_history_compactor`: pliega cada acción consumida en una
  línea `acción → resultado`, deduplicando repeticiones. Sin LLM: costo
  cero y sin nuevos modos de falla. Aísla cuánto aporta *comprimir*
  frente a *resumir con abstracción*.
- `make_llm_history_compactor(agent)`: resume con el propio LLM del
  agente a un estado estructurado (`TrajectorySummary`). Los hechos
  literales (códigos, llaves, errores) se piden textuales, porque el
  modo de falla propio de un resumidor es omitir el dato que después
  resulta clave.
"""

from __future__ import annotations

import json
from typing import Any, Callable

from pydantic import BaseModel, Field

from mia_agents.tool_schema import final_result_tool_schema


class TrajectorySummary(BaseModel):
    """Estado acumulado que sobrevive a la compactación del historial."""

    discovered_facts: list[str] = Field(
        description=(
            "Hechos descubiertos del mundo: objetos, ubicaciones, "
            "relaciones, y códigos o combinaciones copiados textualmente."
        ),
    )
    attempted_actions: list[str] = Field(
        description=(
            "Acciones ya intentadas y su resultado, incluidas las fallidas."
        ),
    )
    open_subgoals: list[str] = Field(
        description="Subobjetivos pendientes o plan parcial.",
    )
    dead_ends: list[str] = Field(
        description="Caminos que ya se sabe que no funcionan y por qué.",
    )


_DETERMINISTIC_OBSERVATION_CHARS = 200
_TRANSCRIPT_OBSERVATION_CHARS = 1000


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text

    return text[: max_chars - 1] + "…"


def _render_action_lines(
    messages: list[dict[str, Any]],
    *,
    max_observation_chars: int,
) -> list[str]:
    """Convierte mensajes descartados en líneas acción → resultado."""

    calls_by_id: dict[str, str] = {}
    lines: list[str] = []

    for message in messages:
        role = message.get("role")

        if role == "assistant" and message.get("tool_calls"):
            for call in message["tool_calls"]:
                function = call.get("function", {})
                calls_by_id[call.get("id")] = (
                    f"{function.get('name')}"
                    f"({function.get('arguments') or ''})"
                )

            continue

        if role == "tool":
            action = calls_by_id.get(
                message.get("tool_call_id"),
                f"{message.get('name', '?')}(…)",
            )
            observation = _truncate(
                message.get("content") or "",
                max_observation_chars,
            )
            lines.append(f"- {action} → {observation}")
            continue

        content = message.get("content")

        if content:
            lines.append(
                f"- [{role}] "
                f"{_truncate(content, max_observation_chars)}"
            )

    return lines


def deterministic_history_compactor(
    messages: list[dict[str, Any]],
) -> str:
    """Compacta mensajes descartados sin LLM, deduplicando repeticiones."""

    lines = _render_action_lines(
        messages,
        max_observation_chars=_DETERMINISTIC_OBSERVATION_CHARS,
    )

    counted: dict[str, int] = {}

    for line in lines:
        counted[line] = counted.get(line, 0) + 1

    rendered = [
        line if count == 1 else f"{line} (x{count})"
        for line, count in counted.items()
    ]

    return "\n".join(rendered) or "(sin acciones registradas)"


def format_trajectory_summary(summary: TrajectorySummary) -> str:
    """Renderiza el estado estructurado como texto para el historial."""

    sections = (
        ("Hechos descubiertos", summary.discovered_facts),
        ("Acciones ya intentadas", summary.attempted_actions),
        ("Subobjetivos pendientes", summary.open_subgoals),
        ("Callejones sin salida", summary.dead_ends),
    )

    lines: list[str] = []

    for title, items in sections:
        if not items:
            continue

        lines.append(f"{title}:")
        lines.extend(f"- {item}" for item in items)

    return "\n".join(lines) or "(sin información relevante)"


_COMPACTION_PROMPT = (
    "Estás comprimiendo el historial de un agente que resuelve una tarea "
    "con herramientas, para liberar espacio de contexto. Este es el "
    "fragmento de historial que será descartado:\n\n"
    "{transcript}\n\n"
    "Registrá en final_result el estado necesario para continuar la "
    "tarea sin ese fragmento. No inventes información que no esté en el "
    "fragmento. Copiá textualmente códigos, claves, combinaciones y "
    "mensajes de error de herramientas."
)


def make_llm_history_compactor(
    agent: Any,
    *,
    max_repair_attempts: int = 1,
) -> Callable[[list[dict[str, Any]]], str]:
    """Crea un compactor que resume con el propio LLM del agente.

    Reusa la maquinaria de structured_call del agente, que arma su
    propio contexto y no toca `agent._history`, por lo que es seguro
    invocarla desde adentro del trimming. Los tokens se acumulan en el
    AgentResult del run activo vía `_run_response_callback`.
    """

    final_tool = final_result_tool_schema(TrajectorySummary)

    def validate_call(final_call: Any) -> TrajectorySummary:
        args = json.loads(final_call.arguments)
        return TrajectorySummary.model_validate(args)

    def compact(messages: list[dict[str, Any]]) -> str:
        transcript = "\n".join(
            _render_action_lines(
                messages,
                max_observation_chars=_TRANSCRIPT_OBSERVATION_CHARS,
            )
        )

        summary = agent._structured_call_with_repair(
            prompt=_COMPACTION_PROMPT.format(transcript=transcript),
            tools=[final_tool],
            validate_call=validate_call,
            max_repair_attempts=max_repair_attempts,
            response_callback=agent._run_response_callback,
            purpose="history_compaction",
        )

        return format_trajectory_summary(summary)

    return compact
