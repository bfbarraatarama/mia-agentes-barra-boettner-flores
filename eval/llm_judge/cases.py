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


QUALITATIVE_CASE_SCHEMA_VERSION = 1
CASE_VIEW_VERSION = "trajectory-planning-v1"


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
) -> list[dict[str, Any]]:
    """Selecciona una respuesta exitosa por iteración lógica del agente."""

    return [
        event
        for event in trace
        if (
            event.get("type") == "llm_call"
            and event.get("purpose") == "agent"
            and event.get("response") is not None
        )
    ]


def _build_attempt(attempt: dict[str, Any]) -> QualitativeAttempt:
    """Reconstruye iteraciones lógicas y acciones efectivas de un attempt."""

    agent_result = attempt["agent_result"]
    steps = agent_result["steps"]
    agent_calls = _successful_agent_calls(attempt["trace"])
    step_index = 0
    iterations = []

    for iteration_position, llm_call in enumerate(agent_calls):
        iteration_index = iteration_position + 1
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
            assistant_content=response.get("content"),
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

    attempts = [
        _build_attempt(attempt)
        for attempt in raw_attempts
    ]

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