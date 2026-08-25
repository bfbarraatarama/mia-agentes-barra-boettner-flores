"""Contratos de datos de la evaluación cualitativa mediante LLM-as-judge."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from eval.llm_judge.rubric import CRITERION_IDS, CriterionId


CaseSplit = Literal["dev", "holdout"]
InternalContextKind = Literal["plan", "summary"]
ApplicabilityTriggerKind = Literal[
    "attempt_continuation",
    "error_before_later_decision",
    "repeated_effective_action",
    "consecutive_exact_repetition",
]


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


class QualitativeInternalContext(_StrictModel):
    """Representación interna producida por el sistema durante la trayectoria."""

    context_id: str = Field(min_length=1)
    kind: InternalContextKind
    content: str
    preserved_raw_round_refs: list[str] = Field(default_factory=list)


class QualitativeIteration(_StrictModel):
    """Una iteración del agente y las acciones decididas en ella."""

    iteration_index: int = Field(ge=1)
    context_before_decision: list[QualitativeInternalContext] = Field(
        default_factory=list
    )
    assistant_content: str | None = None
    context_after_decision: list[QualitativeInternalContext] = Field(
        default_factory=list
    )
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


class ApplicabilityTriggerComponent(_StrictModel):
    """Condición programática que contribuye a una oportunidad de adaptación."""

    kind: ApplicabilityTriggerKind
    evidence_refs: list[str] = Field(min_length=1)


class ApplicabilityTrigger(_StrictModel):
    """Oportunidad de adaptación agrupada por decisión posterior."""

    target_ref: str = Field(min_length=1)
    components: list[ApplicabilityTriggerComponent] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_components(self) -> ApplicabilityTrigger:
        kinds = [
            component.kind
            for component in self.components
        ]

        if len(kinds) != len(set(kinds)):
            raise ValueError(
                "Un trigger agrupado de Q1.4 no puede repetir "
                "el mismo tipo de componente."
            )

        return self


class CriterionApplicability(_StrictModel):
    """Aplicabilidad determinística de un criterio para un caso."""

    applicable: bool
    reason: str | None = None
    triggers: list[ApplicabilityTrigger] = Field(default_factory=list)


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

        if self.schema_version >= 4:
            q1_4 = self.criteria_applicability["Q1.4"]

            if q1_4.applicable != bool(q1_4.triggers):
                raise ValueError(
                    "En schema_version >= 4, Q1.4 debe ser aplicable "
                    "si y sólo si contiene triggers determinísticos."
                )

            target_refs = [
                trigger.target_ref
                for trigger in q1_4.triggers
            ]

            if len(target_refs) != len(set(target_refs)):
                raise ValueError(
                    "Los triggers agrupados de Q1.4 deben tener "
                    "targets únicos."
                )

            if self.schema_version >= 5:
                legacy_repetitions = [
                    component
                    for trigger in q1_4.triggers
                    for component in trigger.components
                    if component.kind == "repeated_effective_action"
                ]

                if legacy_repetitions:
                    raise ValueError(
                        "En schema_version >= 5, las repeticiones de Q1.4 "
                        "deben usar consecutive_exact_repetition."
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


JudgeVerdict = Literal["PASS", "FAIL"]


class JudgeCriterionDecision(_StrictModel):
    """Decisión estructurada del LLM judge para un criterio aplicable."""

    verdict: JudgeVerdict
    reason: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)


class JudgeCasePrediction(_StrictModel):
    """Predicción cualitativa reproducible del judge para un caso."""

    schema_version: int = Field(ge=1)
    case_schema_version: int = Field(ge=1)
    case_view_version: str = Field(min_length=1)
    presentation_version: str = Field(min_length=1)
    rubric_version: str = Field(min_length=1)
    judge_prompt_version: str = Field(min_length=1)
    case_id: str = Field(min_length=1)
    criteria: dict[
        CriterionId,
        JudgeCriterionDecision,
    ]


HumanVerdict = Literal["PASS", "FAIL"]


class HumanCriterionAnnotation(_StrictModel):
    """Anotación humana de un criterio cualitativo aplicable."""

    verdict: HumanVerdict
    reason: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)


class HumanAnnotation(_StrictModel):
    """Anotación humana ciega de un caso cualitativo."""

    schema_version: int = Field(ge=1)
    case_schema_version: int = Field(ge=1)
    case_view_version: str = Field(min_length=1)
    presentation_version: str = Field(min_length=1)
    rubric_version: str = Field(min_length=1)
    case_id: str = Field(min_length=1)
    annotator_id: str = Field(min_length=1)
    criteria: dict[
        CriterionId,
        HumanCriterionAnnotation,
    ]