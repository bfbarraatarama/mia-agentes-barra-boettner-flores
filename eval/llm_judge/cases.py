"""Normalización de trials persistidos para evaluación cualitativa."""

from __future__ import annotations

import json
from typing import Any

from eval.llm_judge.models import (
    ActionObservation,
    AttemptTermination,
    CriterionApplicability,
    QualitativeAction,
    QualitativeAttempt,
    QualitativeCase,
    QualitativeInternalContext,
    QualitativeIteration,
    ToolCallView,
    ActionExecution,
)
from eval.llm_judge.rubric import (
    Q1_4_CONTINUATION_TRIGGER,
    Q1_4_ERROR_TRIGGER,
    Q1_4_NO_TRIGGER_REASON,
    Q1_4_REPETITION_TRIGGER,
)


QUALITATIVE_CASE_SCHEMA_VERSION = 2
CASE_VIEW_VERSION = "trajectory-planning-v2"


def _parse_arguments(arguments_raw: str | None) -> dict[str, Any] | None:
    """Parsea argumentos JSON sólo cuando representan un objeto."""

    if not arguments_raw:
        return {}

    try:
        arguments = json.loads(arguments_raw)
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(arguments, dict):
        return None

    return arguments


def _tool_call_view(
    tool: str,
    arguments_raw: str | None,
) -> ToolCallView:
    """Construye la vista normalizada de una llamada a herramienta."""

    return ToolCallView(
        tool=tool,
        arguments_raw=arguments_raw,
        arguments=_parse_arguments(arguments_raw),
    )


def _tool_calls_differ(
    proposed: ToolCallView,
    effective: ToolCallView,
) -> bool:
    """Compara intención propuesta y llamada efectiva de forma estructural."""

    if proposed.tool != effective.tool:
        return True

    if proposed.arguments is not None and effective.arguments is not None:
        return proposed.arguments != effective.arguments

    return proposed.arguments_raw != effective.arguments_raw


def _observation_from_step(step: dict[str, Any]) -> ActionObservation:
    """Normaliza la observación final correspondiente a un AgentStep."""

    content = step.get("tool_output")
    error = step.get("error")
    semantic_error = (
        isinstance(content, str)
        and content.lstrip().startswith("Error:")
    )

    return ActionObservation(
        content=content or None,
        error=error,
        is_error=error is not None or semantic_error,
    )


def _successful_agent_calls(
    trace: list[dict[str, Any]],
) -> list[tuple[int, dict[str, Any]]]:
    """Selecciona una respuesta exitosa por iteración lógica del agente."""

    return [
        (trace_index, event)
        for trace_index, event in enumerate(trace)
        if (
            event.get("type") == "llm_call"
            and event.get("purpose") == "agent"
            and event.get("response") is not None
        )
    ]


def _planning_contexts(
    events: list[dict[str, Any]],
    *,
    attempt_index: int,
    iteration_index: int,
) -> list[QualitativeInternalContext]:
    """Normaliza planes validados producidos antes de una decisión."""

    planning_calls = [
        event
        for event in events
        if (
            event.get("type") == "llm_call"
            and event.get("purpose") == "planning"
            and event.get("response") is not None
        )
    ]
    planning_events = [
        event
        for event in events
        if event.get("type") == "planning"
    ]

    if planning_calls and not planning_events:
        raise ValueError(
            "La traza contiene planificación exitosa sin el plan "
            "validado utilizado por el agente."
        )

    contexts = []

    for context_index, event in enumerate(
        planning_events,
        start=1,
    ):
        plan = event.get("plan")

        if (
            not isinstance(plan, dict)
            or not isinstance(plan.get("steps"), list)
        ):
            raise ValueError(
                "El evento planning no contiene un plan estructurado válido."
            )

        descriptions = []

        for step in plan["steps"]:
            if (
                not isinstance(step, dict)
                or not isinstance(step.get("description"), str)
            ):
                raise ValueError(
                    "El evento planning contiene un paso inválido."
                )

            descriptions.append(step["description"])

        if not descriptions:
            raise ValueError(
                "El evento planning debe contener al menos un paso."
            )

        contexts.append(QualitativeInternalContext(
            context_id=(
                f"a{attempt_index}.i{iteration_index}."
                f"plan{context_index}"
            ),
            kind="plan",
            content="\n".join(
                f"{index}. {description}"
                for index, description in enumerate(
                    descriptions,
                    start=1,
                )
            ),
        ))

    return contexts


def _summary_contexts(
    events: list[dict[str, Any]],
    *,
    attempt_index: int,
    iteration_index: int,
) -> list[QualitativeInternalContext]:
    """Normaliza summaries producidos después de una decisión."""

    contexts = []

    for event in events:
        if (
            event.get("type") != "history_compaction"
            or event.get("error") is not None
        ):
            continue

        summary = event.get("summary")

        if not isinstance(summary, str):
            raise ValueError(
                "La traza contiene una compactación exitosa sin el "
                "summary utilizado por el agente."
            )

        contexts.append(QualitativeInternalContext(
            context_id=(
                f"a{attempt_index}.i{iteration_index}."
                f"summary{len(contexts) + 1}"
            ),
            kind="summary",
            content=summary,
        ))

    return contexts


def _build_attempt(
    attempt: dict[str, Any],
    *,
    later_attempt_has_decision: bool,
) -> QualitativeAttempt:
    """Reconstruye iteraciones lógicas y acciones efectivas de un attempt."""

    agent_result = attempt["agent_result"]
    steps = agent_result["steps"]
    trace = attempt["trace"]
    agent_calls = _successful_agent_calls(trace)
    step_index = 0
    iterations = []

    for iteration_position, (trace_index, llm_call) in enumerate(
        agent_calls
    ):
        iteration_index = iteration_position + 1
        previous_trace_index = (
            agent_calls[iteration_position - 1][0]
            if iteration_position > 0
            else -1
        )
        next_trace_index = (
            agent_calls[iteration_position + 1][0]
            if iteration_position + 1 < len(agent_calls)
            else len(trace)
        )
        has_later_decision = (
            iteration_position + 1 < len(agent_calls)
            or later_attempt_has_decision
        )

        context_before_decision = _planning_contexts(
            trace[previous_trace_index + 1:trace_index],
            attempt_index=attempt["attempt_index"],
            iteration_index=iteration_index,
        )
        context_after_decision = (
            _summary_contexts(
                trace[trace_index + 1:next_trace_index],
                attempt_index=attempt["attempt_index"],
                iteration_index=iteration_index,
            )
            if has_later_decision
            else []
        )

        response = llm_call["response"]
        proposed_calls = response.get("tool_calls") or []
        actions = []

        remaining_steps = len(steps) - step_index

        if (
            proposed_calls
            and 0 < remaining_steps < len(proposed_calls)
        ):
            raise ValueError(
                "Una iteración contiene sólo una parte de las acciones "
                "esperadas en agent_result.steps."
            )

        actions_were_executed = (
            not proposed_calls
            or remaining_steps >= len(proposed_calls)
        )

        if (
            proposed_calls
            and not actions_were_executed
            and iteration_position != len(agent_calls) - 1
        ):
            raise ValueError(
                "Una iteración no final contiene acciones propuestas "
                "que no fueron ejecutadas."
            )

        for action_index, proposed_call in enumerate(
            proposed_calls,
            start=1,
        ):
            proposed_action = _tool_call_view(
                proposed_call["name"],
                proposed_call.get("arguments"),
            )

            execution = None

            if actions_were_executed:
                step = steps[step_index]
                step_index += 1

                effective_action = _tool_call_view(
                    step["tool_name"],
                    step.get("tool_input"),
                )

                execution = ActionExecution(
                    action=effective_action,
                    differs_from_proposal=_tool_calls_differ(
                        proposed_action,
                        effective_action,
                    ),
                    observation=_observation_from_step(step),
                )

            actions.append(QualitativeAction(
                action_id=(
                    f"a{attempt['attempt_index']}."
                    f"i{iteration_index}.action{action_index}"
                ),
                proposed_action=proposed_action,
                execution=execution,
            ))

        iterations.append(QualitativeIteration(
            iteration_index=iteration_index,
            context_before_decision=context_before_decision,
            assistant_content=response.get("content"),
            context_after_decision=context_after_decision,
            actions=actions,
        ))

    if step_index != len(steps):
        raise ValueError(
            "agent_result.steps contiene acciones que no pudieron asociarse "
            "a una iteración del agente."
        )

    return QualitativeAttempt(
        attempt_index=attempt["attempt_index"],
        user_message=attempt["user_message"],
        iterations=iterations,
        termination=AttemptTermination(
            answer=agent_result["answer"],
            error=agent_result.get("error"),
        ),
    )


def _action_key(
    action: QualitativeAction,
) -> tuple[str, str | None, str | None, str | None]:
    """Construye una clave estable para comparar acciones ejecutadas."""

    if action.execution is None:
        raise ValueError(
            "No se puede construir una clave para una acción no ejecutada."
        )

    effective_action = action.execution.action
    arguments = effective_action.arguments

    if arguments is not None:
        arguments_key = json.dumps(
            arguments,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        )
    else:
        arguments_key = effective_action.arguments_raw

    return (
        effective_action.tool,
        arguments_key,
        action.execution.observation.content,
        action.execution.observation.error,
    )


def _q1_4_applicability(
    attempts: list[QualitativeAttempt],
) -> CriterionApplicability:
    """Determina si el trial contiene una oportunidad observable de adaptación."""

    if len(attempts) > 1:
        return CriterionApplicability(
            applicable=True,
            reason=Q1_4_CONTINUATION_TRIGGER,
        )

    attempt = attempts[0]
    seen_actions: set[
        tuple[str, str | None, str | None, str | None]
    ] = set()

    for iteration_position, iteration in enumerate(attempt.iterations):
        iteration_action_keys = []

        for action in iteration.actions:
            if action.execution is None:
                continue

            if (
                action.execution.observation.is_error
                and iteration_position < len(attempt.iterations) - 1
            ):
                return CriterionApplicability(
                    applicable=True,
                    reason=Q1_4_ERROR_TRIGGER,
                )

            action_key = _action_key(action)

            if action_key in seen_actions:
                return CriterionApplicability(
                    applicable=True,
                    reason=Q1_4_REPETITION_TRIGGER,
                )

            iteration_action_keys.append(action_key)

        seen_actions.update(iteration_action_keys)

    return CriterionApplicability(
        applicable=False,
        reason=Q1_4_NO_TRIGGER_REASON,
    )

def build_qualitative_case(
    trial: dict[str, Any],
    *,
    case_id: str,
) -> QualitativeCase:
    """Construye la vista ciega y normalizada de un trial persistido."""

    raw_attempts = trial.get("attempts") or []

    if not raw_attempts:
        raise ValueError("El trial debe contener al menos un attempt.")

    attempts = []

    for attempt_position, attempt in enumerate(raw_attempts):
        later_attempt_has_decision = any(
            _successful_agent_calls(later_attempt["trace"])
            for later_attempt in raw_attempts[attempt_position + 1:]
        )

        attempts.append(_build_attempt(
            attempt,
            later_attempt_has_decision=later_attempt_has_decision,
        ))

    return QualitativeCase(
        schema_version=QUALITATIVE_CASE_SCHEMA_VERSION,
        case_view_version=CASE_VIEW_VERSION,
        case_id=case_id,
        task=raw_attempts[0]["user_message"],
        criteria_applicability={
            "Q1.1": CriterionApplicability(applicable=True),
            "Q1.2": CriterionApplicability(applicable=True),
            "Q1.3": CriterionApplicability(applicable=True),
            "Q1.4": _q1_4_applicability(attempts),
        },
        attempts=attempts,
    )