"""Normalización de trials persistidos para evaluación cualitativa."""

from __future__ import annotations

import json
from typing import Any

from eval.llm_judge.models import (
    ActionObservation,
    ApplicabilityTrigger,
    ApplicabilityTriggerComponent,
    ApplicabilityTriggerKind,
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
from eval.llm_judge.rubric import Q1_4_NO_TRIGGER_REASON


QUALITATIVE_CASE_SCHEMA_VERSION = 6
CASE_VIEW_VERSION = "trajectory-planning-v6"

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


def _iteration_has_raw_round(
    iteration: QualitativeIteration,
) -> bool:
    """Indica si la iteración llegó a persistirse como ronda assistant+tool."""

    return (
        bool(iteration.actions)
        and all(
            action.execution is not None
            for action in iteration.actions
        )
    )


def _preserved_raw_round_refs(
    messages: list[dict[str, Any]],
    *,
    summary: str,
    prior_iterations: list[tuple[str, QualitativeIteration]],
    current_iteration_ref: str,
) -> list[str]:
    """Identifica las rondas crudas que seguían disponibles junto al summary."""

    summary_message_index = next(
        (
            index
            for index, message in enumerate(messages)
            if (
                isinstance(message.get("content"), str)
                and summary in message["content"]
            )
        ),
        None,
    )

    if summary_message_index is None:
        return []

    raw_round_count = sum(
        1
        for message in messages[summary_message_index + 1:]
        if (
            message.get("role") == "assistant"
            and bool(message.get("tool_calls"))
        )
    )
    current_iteration = next(
        iteration
        for iteration_ref, iteration in prior_iterations
        if iteration_ref == current_iteration_ref
    )
    current_round_count = (
        1
        if _iteration_has_raw_round(current_iteration)
        else 0
    )
    preserved_count = raw_round_count - current_round_count

    if preserved_count < 0:
        raise ValueError(
            "El contexto posterior al summary no contiene la ronda "
            "cruda de la iteración que produjo la compactación."
        )

    previous_raw_round_refs = [
        iteration_ref
        for iteration_ref, iteration in prior_iterations
        if (
            iteration_ref != current_iteration_ref
            and _iteration_has_raw_round(iteration)
        )
    ]

    if preserved_count > len(previous_raw_round_refs):
        raise ValueError(
            "El contexto posterior al summary contiene más rondas "
            "crudas que las reconstruibles desde la trayectoria."
        )

    if preserved_count == 0:
        return []

    return previous_raw_round_refs[-preserved_count:]


def _attach_summary_contexts(
    raw_attempts: list[dict[str, Any]],
    attempts: list[QualitativeAttempt],
) -> None:
    """Adjunta sólo summaries realmente disponibles en una decisión posterior."""

    decisions = []

    for attempt_position, raw_attempt in enumerate(raw_attempts):
        agent_calls = _successful_agent_calls(raw_attempt["trace"])
        normalized_attempt = attempts[attempt_position]

        for iteration_position, (trace_index, llm_call) in enumerate(
            agent_calls
        ):
            decisions.append((
                attempt_position,
                trace_index,
                llm_call,
                normalized_attempt.iterations[iteration_position],
            ))

    prior_iterations: list[tuple[str, QualitativeIteration]] = []

    for decision_position, decision in enumerate(decisions):
        (
            attempt_position,
            trace_index,
            _,
            iteration,
        ) = decision
        attempt = attempts[attempt_position]
        iteration_ref = (
            f"a{attempt.attempt_index}."
            f"i{iteration.iteration_index}"
        )
        prior_iterations.append((
            iteration_ref,
            iteration,
        ))

        if decision_position + 1 >= len(decisions):
            continue

        next_decision = decisions[decision_position + 1]
        next_attempt_position = next_decision[0]
        next_trace_index = next_decision[1]
        next_llm_call = next_decision[2]
        trace = raw_attempts[attempt_position]["trace"]
        end = (
            next_trace_index
            if next_attempt_position == attempt_position
            else len(trace)
        )
        events = trace[trace_index + 1:end]
        next_messages = next_llm_call.get("messages") or []
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

            if not any(
                isinstance(message.get("content"), str)
                and summary in message["content"]
                for message in next_messages
            ):
                continue

            contexts.append(QualitativeInternalContext(
                context_id=(
                    f"{iteration_ref}."
                    f"summary{len(contexts) + 1}"
                ),
                kind="summary",
                content=summary,
                preserved_raw_round_refs=(
                    _preserved_raw_round_refs(
                        next_messages,
                        summary=summary,
                        prior_iterations=prior_iterations,
                        current_iteration_ref=iteration_ref,
                    )
                ),
            ))

        iteration.context_after_decision = contexts


def _build_attempt(
    attempt: dict[str, Any],
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
        context_before_decision = _planning_contexts(
            trace[previous_trace_index + 1:trace_index],
            attempt_index=attempt["attempt_index"],
            iteration_index=iteration_index,
        )
        context_after_decision = []

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


def _next_decision_ref(
    attempts: list[QualitativeAttempt],
    *,
    attempt_position: int,
    iteration_position: int,
) -> str | None:
    """Ubica la primera decisión posterior observable dentro del trial."""

    attempt = attempts[attempt_position]

    if iteration_position + 1 < len(attempt.iterations):
        next_iteration = attempt.iterations[
            iteration_position + 1
        ]
        return (
            f"a{attempt.attempt_index}."
            f"i{next_iteration.iteration_index}"
        )

    for later_attempt in attempts[attempt_position + 1:]:
        if later_attempt.iterations:
            next_iteration = later_attempt.iterations[0]
            return (
                f"a{later_attempt.attempt_index}."
                f"i{next_iteration.iteration_index}"
            )

    return None


def _add_q1_4_component(
    grouped_components: dict[
        str,
        dict[ApplicabilityTriggerKind, list[str]],
    ],
    target_order: list[str],
    *,
    target_ref: str,
    kind: ApplicabilityTriggerKind,
    evidence_refs: list[str],
) -> None:
    """Acumula una condición elemental en su oportunidad de adaptación."""

    if target_ref not in grouped_components:
        grouped_components[target_ref] = {}
        target_order.append(target_ref)

    component_refs = grouped_components[
        target_ref
    ].setdefault(
        kind,
        [],
    )

    for evidence_ref in evidence_refs:
        if evidence_ref not in component_refs:
            component_refs.append(
                evidence_ref
            )


def _q1_4_applicability(
    attempts: list[QualitativeAttempt],
) -> CriterionApplicability:
    """Agrupa oportunidades observables de adaptación por decisión posterior."""

    grouped_components: dict[
        str,
        dict[ApplicabilityTriggerKind, list[str]],
    ] = {}
    target_order: list[str] = []

    previous_action_key: (
        tuple[str, str | None, str | None, str | None]
        | None
    ) = None
    previous_action_ref: str | None = None
    previous_attempt_index: int | None = None
    previous_iteration_index: int | None = None
    active_repetition_target_ref: str | None = None

    for attempt_position, attempt in enumerate(attempts):
        for iteration_position, iteration in enumerate(
            attempt.iterations
        ):
            iteration_ref = (
                f"a{attempt.attempt_index}."
                f"i{iteration.iteration_index}"
            )
            next_decision_ref = _next_decision_ref(
                attempts,
                attempt_position=attempt_position,
                iteration_position=iteration_position,
            )

            for action in iteration.actions:
                if action.execution is None:
                    continue

                if (
                    action.execution.observation.is_error
                    and next_decision_ref is not None
                ):
                    _add_q1_4_component(
                        grouped_components,
                        target_order,
                        target_ref=next_decision_ref,
                        kind="error_before_later_decision",
                        evidence_refs=[
                            action.action_id,
                        ],
                    )

                action_key = _action_key(
                    action
                )
                comes_from_later_decision = (
                    previous_action_ref is not None
                    and (
                        previous_attempt_index
                        != attempt.attempt_index
                        or previous_iteration_index
                        != iteration.iteration_index
                    )
                )
                repeats_previous_action = (
                    comes_from_later_decision
                    and previous_action_key == action_key
                )

                if repeats_previous_action:
                    if active_repetition_target_ref is None:
                        active_repetition_target_ref = iteration_ref

                        _add_q1_4_component(
                            grouped_components,
                            target_order,
                            target_ref=active_repetition_target_ref,
                            kind="consecutive_exact_repetition",
                            evidence_refs=[
                                previous_action_ref,
                                action.action_id,
                            ],
                        )
                    else:
                        _add_q1_4_component(
                            grouped_components,
                            target_order,
                            target_ref=active_repetition_target_ref,
                            kind="consecutive_exact_repetition",
                            evidence_refs=[
                                action.action_id,
                            ],
                        )
                else:
                    active_repetition_target_ref = None

                previous_action_key = action_key
                previous_action_ref = action.action_id
                previous_attempt_index = attempt.attempt_index
                previous_iteration_index = iteration.iteration_index

        if attempt_position + 1 < len(attempts):
            next_attempt = attempts[
                attempt_position + 1
            ]

            if next_attempt.iterations:
                first_iteration = next_attempt.iterations[0]
                target_ref = (
                    f"a{next_attempt.attempt_index}."
                    f"i{first_iteration.iteration_index}"
                )
            else:
                target_ref = (
                    f"a{next_attempt.attempt_index}."
                    "user_message"
                )

            _add_q1_4_component(
                grouped_components,
                target_order,
                target_ref=target_ref,
                kind="attempt_continuation",
                evidence_refs=[
                    f"a{attempt.attempt_index}.termination",
                    f"a{next_attempt.attempt_index}.user_message",
                ],
            )

    triggers = [
        ApplicabilityTrigger(
            target_ref=target_ref,
            components=[
                ApplicabilityTriggerComponent(
                    kind=kind,
                    evidence_refs=evidence_refs,
                )
                for kind, evidence_refs in (
                    grouped_components[
                        target_ref
                    ].items()
                )
            ],
        )
        for target_ref in target_order
    ]

    if triggers:
        return CriterionApplicability(
            applicable=True,
            triggers=triggers,
        )

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

    _attach_summary_contexts(
        raw_attempts,
        attempts,
    )

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