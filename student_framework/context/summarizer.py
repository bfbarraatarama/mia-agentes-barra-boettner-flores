"""Compactación de historial para ejecuciones de horizonte largo (M3).

Dos variantes de compactor para `MyAgent(history_compactor=...)`:

- `deterministic_history_compactor`: pliega cada acción consumida en una
  línea `acción → resultado`, deduplicando repeticiones. Las observaciones
  largas conservan un prefijo acotado, por lo que la estrategia es
  deliberadamente lossy; si dos observaciones distintas colisionan tras
  truncarse, ambas se conservan completas para no fusionarlas. Sin LLM:
  costo cero y sin nuevos modos de falla. Aísla cuánto aporta *comprimir*
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


class StrategicTrajectorySummary(BaseModel):
    """Estado estratégico vigente reconstruido durante la compactación."""

    current_subgoal: str | None = Field(
        description=(
            "Subobjetivo vigente. Usar null si no hay uno identificable."
        ),
    )
    current_strategy: str | None = Field(
        description=(
            "Estrategia actualmente razonable para avanzar hacia el "
            "subobjetivo. Usar null si la evidencia no sostiene ninguna."
        ),
    )
    confirmed_facts: list[str] = Field(
        description=(
            "Hechos confirmados del mundo, incluidos códigos, claves, "
            "combinaciones y relaciones relevantes copiados textualmente."
        ),
    )
    negative_evidence: list[str] = Field(
        description=(
            "Observaciones que contradicen hipótesis, estrategias o "
            "acciones que parecían viables."
        ),
    )
    attempted_actions: list[str] = Field(
        description=(
            "Acciones ya intentadas y su resultado, incluidas las fallidas."
        ),
    )
    dead_ends: list[str] = Field(
        description=(
            "Caminos descartados que no deberían repetirse y la evidencia "
            "que permite descartarlos."
        ),
    )
    open_questions: list[str] = Field(
        description=(
            "Incertidumbres, alternativas todavía viables o preguntas que "
            "deben resolverse para decidir cómo continuar."
        ),
    )
    progress: list[str] = Field(
        description=(
            "Progreso ya consolidado hacia el objetivo o subobjetivos "
            "completados que no deben volver a tratarse como pendientes."
        ),
    )
    additional_context: list[str] = Field(
        description=(
            "Información relevante para continuar que no encaja con claridad "
            "en los campos anteriores."
        ),
    )


_DETERMINISTIC_OBSERVATION_CHARS = 200
_TRANSCRIPT_OBSERVATION_CHARS = 1000


def _truncate(text: str, max_chars: int | None) -> str:
    if max_chars is None or len(text) <= max_chars:
        return text

    return text[: max_chars - 1] + "…"


def _render_action_lines(
    messages: list[dict[str, Any]],
    *,
    max_observation_chars: int | None,
) -> list[str]:
    """Convierte mensajes descartados en líneas acción → resultado."""

    calls_by_id: dict[str, str] = {}
    lines: list[str] = []

    for message in messages:
        role = message.get("role")

        if role == "assistant" and message.get("tool_calls"):
            content = message.get("content")
            if content:
                lines.append(
                    f"- [{role}] "
                    f"{_truncate(content, max_observation_chars)}"
                )

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
    """Compacta mensajes descartados sin LLM.

    Deduplica sólo representaciones completas iguales. Para mantener
    acotado el resumen, las observaciones ordinarias se representan por
    su prefijo de `_DETERMINISTIC_OBSERVATION_CHARS` caracteres. Si dos
    observaciones distintas producirían la misma representación truncada,
    se conservan completas para evitar una deduplicación falsa.
    """

    full_lines = _render_action_lines(
        messages,
        max_observation_chars=None,
    )
    compact_lines = _render_action_lines(
        messages,
        max_observation_chars=_DETERMINISTIC_OBSERVATION_CHARS,
    )

    counted: dict[str, tuple[str, int]] = {}
    compact_groups: dict[str, set[str]] = {}

    for full_line, compact_line in zip(full_lines, compact_lines):
        compact_groups.setdefault(compact_line, set()).add(full_line)

        if full_line in counted:
            rendered_line, count = counted[full_line]
            counted[full_line] = (rendered_line, count + 1)
        else:
            counted[full_line] = (compact_line, 1)

    rendered = []

    for full_line, (compact_line, count) in counted.items():
        if len(compact_groups[compact_line]) > 1:
            line = full_line
        else:
            line = compact_line

        rendered.append(
            line if count == 1 else f"{line} (x{count})"
        )

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


def format_strategic_trajectory_summary(
    summary: StrategicTrajectorySummary,
) -> str:
    """Renderiza el estado estratégico vigente para el historial."""

    lines: list[str] = []

    if summary.current_subgoal:
        lines.extend([
            "Subobjetivo vigente:",
            f"- {summary.current_subgoal}",
        ])

    if summary.current_strategy:
        lines.extend([
            "Estrategia vigente:",
            f"- {summary.current_strategy}",
        ])

    sections = (
        ("Hechos confirmados", summary.confirmed_facts),
        ("Evidencia negativa", summary.negative_evidence),
        ("Acciones ya intentadas", summary.attempted_actions),
        ("Callejones sin salida", summary.dead_ends),
        ("Preguntas abiertas", summary.open_questions),
        ("Progreso consolidado", summary.progress),
        ("Contexto adicional", summary.additional_context),
    )

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


_STRATEGIC_COMPACTION_PROMPT = (
    "Estás reconstruyendo el estado estratégico vigente de un agente que "
    "resuelve una tarea con herramientas.\n\n"
    "A partir del historial, registrá en final_result el estado necesario "
    "para continuar, no una narración de lo ocurrido.\n\n"
    "- Conservá los hechos confirmados, las acciones relevantes ya realizadas "
    "y sus resultados, el progreso alcanzado y los caminos descartados.\n"
    "- Conservá la evidencia negativa y las incertidumbres o alternativas "
    "que todavía sean relevantes para decidir cómo continuar.\n"
    "- Identificá el subobjetivo y la estrategia vigentes. Evaluá si siguen "
    "siendo razonables según la evidencia acumulada.\n"
    "- Si el agente está estancado, repite acciones sin progreso o la "
    "estrategia dejó de ser adecuada, replanteá el subobjetivo o la estrategia "
    "y proponé una alternativa respaldada por lo observado, evitando repetir "
    "acciones que ya fallaron bajo las mismas condiciones.\n\n"
    "No inventes información ausente del historial. Copiá textualmente "
    "códigos, claves, combinaciones y mensajes de error relevantes.\n\n"
    "Historial:\n\n"
    "{transcript}"
)


def make_llm_history_compactor(
    agent: Any,
    *,
    max_repair_attempts: int = 1,
    profile: str | None = None,
) -> Callable[[list[dict[str, Any]]], str]:
    """Crea un compactor que resume con el propio LLM del agente.

    Reusa la maquinaria de structured_call del agente, que arma su
    propio contexto y no toca `agent._history`, por lo que es seguro
    invocarla desde adentro del trimming. Los tokens se acumulan en el
    AgentResult del run activo vía `_run_response_callback`.
    """

    if profile is None:
        summary_model: type[BaseModel] = TrajectorySummary
        prompt_template = _COMPACTION_PROMPT
        formatter: Callable[[Any], str] = format_trajectory_summary
    elif profile == "strategic_v1":
        summary_model = StrategicTrajectorySummary
        prompt_template = _STRATEGIC_COMPACTION_PROMPT
        formatter = format_strategic_trajectory_summary
    else:
        raise ValueError(
            f"history_compaction_profile desconocido: {profile!r}. "
            "Valores válidos: 'strategic_v1'."
        )

    final_tool = final_result_tool_schema(summary_model)

    def validate_call(final_call: Any) -> BaseModel:
        args = json.loads(final_call.arguments)
        return summary_model.model_validate(args)

    def compact(messages: list[dict[str, Any]]) -> str:
        transcript = "\n".join(
            _render_action_lines(
                messages,
                max_observation_chars=_TRANSCRIPT_OBSERVATION_CHARS,
            )
        )

        summary = agent._structured_call_with_repair(
            prompt=prompt_template.format(transcript=transcript),
            tools=[final_tool],
            validate_call=validate_call,
            max_repair_attempts=max_repair_attempts,
            response_callback=agent._run_response_callback,
            purpose="history_compaction",
        )

        return formatter(summary)

    return compact
