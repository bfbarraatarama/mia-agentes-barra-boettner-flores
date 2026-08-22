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


PRESENTATION_VERSION = "planning-evidence-v1"


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
            evidence_refs.append(iteration_ref)

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
                "assistant_content": iteration.assistant_content,
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

    presentation_data = {
        "evidence_rules": list(EVIDENCE_RULES),
        "case_id": case.case_id,
        "task": case.task,
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