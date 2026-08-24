"""Presentación canónica de evidencia para evaluadores cualitativos."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from eval.llm_judge.models import (
    QualitativeCase,
    ToolCallView,
)
from eval.llm_judge.rubric import EVIDENCE_RULES


PRESENTATION_VERSION = "planning-evidence-v5"


@dataclass(frozen=True)
class CasePresentation:
    """Evidencia canónica compartida por humanos y LLM judges."""

    version: str
    text: str
    evidence_refs: tuple[str, ...]


def _tool_call_data(
    tool_call: ToolCallView,
) -> dict[str, Any]:
    """Construye la representación canónica de una tool call."""

    return {
        "tool": tool_call.tool,
        "arguments_raw": tool_call.arguments_raw,
        "arguments": tool_call.arguments,
    }


def build_case_presentation(
    case: QualitativeCase,
) -> CasePresentation:
    """Construye la presentación ciega y determinística de un caso."""

    evidence_refs = []
    attempts = []

    for attempt in case.attempts:
        attempt_ref = f"a{attempt.attempt_index}"
        user_message_ref = f"{attempt_ref}.user_message"
        termination_ref = f"{attempt_ref}.termination"

        evidence_refs.append(user_message_ref)

        iterations = []

        for iteration in attempt.iterations:
            iteration_ref = (
                f"{attempt_ref}.i{iteration.iteration_index}"
            )

            context_before_decision = []

            for context in iteration.context_before_decision:
                evidence_refs.append(context.context_id)
                context_before_decision.append({
                    "ref": context.context_id,
                    "kind": context.kind,
                    "content": context.content,
                })

            evidence_refs.append(iteration_ref)

            context_after_decision = []

            for context in iteration.context_after_decision:
                evidence_refs.append(context.context_id)
                context_after_decision.append({
                    "ref": context.context_id,
                    "kind": context.kind,
                    "content": context.content,
                })

            actions = []

            for action in iteration.actions:
                evidence_refs.append(action.action_id)

                action_data: dict[str, Any] = {
                    "ref": action.action_id,
                    "proposed_action": _tool_call_data(
                        action.proposed_action,
                    ),
                    "execution": None,
                }

                if action.execution is not None:
                    action_data["execution"] = {
                        "action": _tool_call_data(
                            action.execution.action,
                        ),
                        "differs_from_proposal": (
                            action.execution.differs_from_proposal
                        ),
                        "observation": {
                            "content": (
                                action.execution.observation.content
                            ),
                            "error": (
                                action.execution.observation.error
                            ),
                            "is_error": (
                                action.execution.observation.is_error
                            ),
                        },
                    }

                actions.append(action_data)

            iterations.append({
                "ref": iteration_ref,
                "context_before_decision": context_before_decision,
                "assistant_content": iteration.assistant_content,
                "context_after_decision": context_after_decision,
                "actions": actions,
            })

        evidence_refs.append(termination_ref)

        attempts.append({
            "attempt_index": attempt.attempt_index,
            "user_message": {
                "ref": user_message_ref,
                "content": attempt.user_message,
            },
            "iterations": iterations,
            "termination": {
                "ref": termination_ref,
                "answer": attempt.termination.answer,
                "error": attempt.termination.error,
            },
        })

    q1_4 = case.criteria_applicability["Q1.4"]
    evidence_ref_set = set(evidence_refs)
    q1_4_triggers = []

    for trigger in q1_4.triggers:
        referenced_evidence = [
            trigger.target_ref,
            *[
                evidence_ref
                for component in trigger.components
                for evidence_ref in component.evidence_refs
            ],
        ]
        unknown_refs = [
            evidence_ref
            for evidence_ref in referenced_evidence
            if evidence_ref not in evidence_ref_set
        ]

        if unknown_refs:
            raise ValueError(
                "Un trigger de Q1.4 referencia evidencia inexistente: "
                f"{unknown_refs!r}."
            )

        q1_4_triggers.append({
            "target_ref": trigger.target_ref,
            "components": [
                {
                    "kind": component.kind,
                    "evidence_refs": list(
                        component.evidence_refs
                    ),
                }
                for component in trigger.components
            ],
        })

    presentation_data = {
        "evidence_rules": list(EVIDENCE_RULES),
        "case_id": case.case_id,
        "task": case.task,
        "q1_4_applicability": {
            "applicable": q1_4.applicable,
            "reason": q1_4.reason,
            "triggers": q1_4_triggers,
        },
        "attempts": attempts,
    }

    return CasePresentation(
        version=PRESENTATION_VERSION,
        text=json.dumps(
            presentation_data,
            indent=2,
            ensure_ascii=False,
        ),
        evidence_refs=tuple(evidence_refs),
    )