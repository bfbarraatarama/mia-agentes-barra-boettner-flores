"""Contratos de datos de la evaluación cualitativa mediante LLM-as-judge."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from eval.llm_judge.rubric import CRITERION_IDS, CriterionId


CaseSplit = Literal["dev", "holdout"]


class _StrictModel(BaseModel):
    """Base común para artefactos cualitativos con schema cerrado."""

    model_config = ConfigDict(extra="forbid")


class ToolCallView(_StrictModel):
    """Representación normalizada de una llamada a herramienta."""

    tool: str
    arguments_raw: str | None = None
    arguments: dict[str, Any] | None = None


class ActionObservation(_StrictModel):
    """Resultado observable de una acción efectivamente ejecutada."""

    content: str | None = None
    error: str | None = None
    is_error: bool = False


class ActionExecution(_StrictModel):
    """Ejecución efectiva de una acción propuesta."""

    action: ToolCallView
    differs_from_proposal: bool
    observation: ActionObservation


class QualitativeAction(_StrictModel):
    """Acción propuesta por el agente y su eventual ejecución."""

    action_id: str = Field(min_length=1)
    proposed_action: ToolCallView
    execution: ActionExecution | None = None


class QualitativeIteration(_StrictModel):
    """Una iteración del agente y las acciones decididas en ella."""

    iteration_index: int = Field(ge=1)
    assistant_content: str | None = None
    actions: list[QualitativeAction] = Field(default_factory=list)


class AttemptTermination(_StrictModel):
    """Forma observable en que terminó un attempt."""

    answer: str
    error: str | None = None


class QualitativeAttempt(_StrictModel):
    """Secuencia normalizada de iteraciones pertenecientes a un attempt."""

    attempt_index: int = Field(ge=1)
    user_message: str
    iterations: list[QualitativeIteration] = Field(default_factory=list)
    termination: AttemptTermination


class CriterionApplicability(_StrictModel):
    """Aplicabilidad determinística de un criterio para un caso."""

    applicable: bool
    reason: str | None = None


class QualitativeCase(_StrictModel):
    """Trial completo presentado de forma ciega a humanos y LLM judge."""

    schema_version: int = Field(ge=1)
    case_view_version: str = Field(min_length=1)
    case_id: str = Field(min_length=1)
    task: str
    criteria_applicability: dict[
        CriterionId,
        CriterionApplicability,
    ]
    attempts: list[QualitativeAttempt] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_criteria_applicability(self) -> QualitativeCase:
        if set(self.criteria_applicability) != set(CRITERION_IDS):
            raise ValueError(
                "criteria_applicability debe definir exactamente "
                "Q1.1, Q1.2, Q1.3 y Q1.4."
            )

        return self


class CaseSource(_StrictModel):
    """Procedencia separada de un caso para mantener ciega su evaluación."""

    case_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    agent_config: str = Field(min_length=1)
    llm_config: str = Field(min_length=1)
    trial_config: str = Field(min_length=1)
    scenario: str = Field(min_length=1)
    trial_index: int = Field(ge=1)
    split: CaseSplit