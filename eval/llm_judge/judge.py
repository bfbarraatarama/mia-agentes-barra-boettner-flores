"""Ejecución ciega del LLM-as-judge sobre criterios cualitativos."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Self

from pydantic import model_validator

from mia_agents.protocols import Agent

from eval.llm_judge.models import (
    JudgeCasePrediction,
    JudgeCriterionDecision,
    QualitativeCase,
)
from eval.llm_judge.presentation import (
    CasePresentation,
    build_case_presentation,
)
from eval.llm_judge.rubric import (
    BOUNDARY_RULES,
    CRITERIA_BY_ID,
    CRITERION_IDS,
    DIMENSION_DESCRIPTION,
    DIMENSION_ID,
    DIMENSION_NAME,
    MATERIALITY_RULE,
    RUBRIC_VERSION,
    CriterionId,
)


JUDGE_SYSTEM_PROMPT = (
    "Actuás exclusivamente como evaluador cualitativo ciego. "
    "Debés aplicar la rúbrica y la evidencia proporcionadas sin "
    "incorporar conocimiento externo ni inferir metadata experimental."
)

JUDGE_PROMPT_VERSION = "planning-criterion-judge-v1"
JUDGE_PREDICTION_SCHEMA_VERSION = 1


def _judge_criterion_decision_schema(
    valid_evidence_refs: set[str],
) -> type[JudgeCriterionDecision]:
    """Construye el schema del criterio con evidencia válida para este caso."""

    class _ValidatedJudgeCriterionDecision(
        JudgeCriterionDecision
    ):
        @model_validator(mode="after")
        def _validate_evidence_refs(self) -> Self:
            invalid_evidence_refs = [
                evidence_ref
                for evidence_ref in self.evidence_refs
                if evidence_ref not in valid_evidence_refs
            ]

            if invalid_evidence_refs:
                raise ValueError(
                    "El judge devolvió referencias de evidencia "
                    "inexistentes: "
                    f"{invalid_evidence_refs}."
                )

            return self

    return _ValidatedJudgeCriterionDecision


def build_judge_prompt(
    presentation: CasePresentation,
    criterion_id: CriterionId,
) -> str:
    """Construye el prompt ciego para evaluar un único criterio."""

    criterion = CRITERIA_BY_ID[
        criterion_id
    ]

    boundary_rules = "\n".join(
        f"- {rule}"
        for rule in BOUNDARY_RULES
    )

    guidance = "\n".join(
        f"- {item}"
        for item in criterion.guidance
    )

    guidance_section = (
        (
            "\nAclaraciones específicas:\n"
            f"{guidance}\n"
        )
        if guidance
        else ""
    )

    applicability_section = ""

    if criterion.applicability == "conditional":
        triggers = "\n".join(
            f"- {trigger} {explanation}"
            for trigger, explanation
            in criterion.applicability_triggers
        )
        notes = "\n".join(
            f"- {note}"
            for note
            in criterion.applicability_notes
        )

        applicability_section = (
            "\nAplicabilidad del criterio:\n"
            f"{criterion.applicability_description}\n\n"
            "Tipos de disparador:\n"
            f"{triggers}\n\n"
            "Notas de aplicabilidad:\n"
            f"{notes}\n"
        )

    return (
        "Actuás como evaluador ciego de la calidad de planificación "
        "de un agente.\n\n"
        "Evaluá exclusivamente el criterio indicado. Basate únicamente "
        "en la presentación canónica del trial y en la rúbrica incluida "
        "a continuación. No agregues información externa ni supongas "
        "hechos que la evidencia no establece.\n\n"
        f"Dimensión {DIMENSION_ID} — {DIMENSION_NAME}\n"
        f"{DIMENSION_DESCRIPTION}\n\n"
        "Regla de materialidad:\n"
        f"{MATERIALITY_RULE}\n\n"
        "Reglas de frontera:\n"
        f"{boundary_rules}\n\n"
        f"Criterio {criterion.id} — {criterion.name}\n"
        f"Pregunta: {criterion.question}\n\n"
        f"PASS: {criterion.pass_description}\n\n"
        f"FAIL: {criterion.fail_description}\n"
        f"{guidance_section}"
        f"{applicability_section}\n"
        "Presentación canónica del trial:\n"
        f"{presentation.text}\n\n"
        "Devolvé:\n"
        "- verdict: PASS o FAIL;\n"
        "- reason: una justificación concreta basada en la trayectoria;\n"
        "- evidence_refs: una o más referencias canónicas que sostengan "
        "el veredicto.\n\n"
        "Las evidence_refs deben existir literalmente en la presentación. "
        "No decidas por la mera presencia de un disparador de aplicabilidad: "
        "los disparadores sólo indican dónde existe una oportunidad que "
        "debe evaluarse."
    )


def judge_prompt_fingerprint() -> str:
    """Identifica el contenido efectivo de la política del judge."""

    sentinel_presentation = CasePresentation(
        version="__presentation_version__",
        text="__canonical_case_presentation__",
        evidence_refs=(
            "__evidence_ref__",
        ),
    )

    payload = {
        "system_prompt": JUDGE_SYSTEM_PROMPT,
        "criterion_prompts": {
            criterion_id: build_judge_prompt(
                sentinel_presentation,
                criterion_id,
            )
            for criterion_id in CRITERION_IDS
        },
        "decision_schema": (
            JudgeCriterionDecision.model_json_schema()
        ),
    }

    serialized_payload = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
    )

    return sha256(
        serialized_payload.encode(
            "utf-8"
        )
    ).hexdigest()


def judge_case_criterion(
    agent: Agent,
    case: QualitativeCase,
    criterion_id: CriterionId,
    *,
    max_repair_attempts: int = 2,
) -> JudgeCriterionDecision:
    """Evalúa un criterio aplicable usando la presentación canónica."""

    applicability = (
        case.criteria_applicability[
            criterion_id
        ]
    )

    if not applicability.applicable:
        raise ValueError(
            f"El criterio {criterion_id} no aplica "
            f"al caso {case.case_id!r}."
        )

    presentation = (
        build_case_presentation(
            case
        )
    )
    prompt = build_judge_prompt(
        presentation,
        criterion_id,
    )
    decision_schema = (
        _judge_criterion_decision_schema(
            set(
                presentation.evidence_refs
            )
        )
    )

    decision = agent.structured_call(
        prompt,
        decision_schema,
        max_repair_attempts=max_repair_attempts,
    )

    return JudgeCriterionDecision.model_validate(
        decision.model_dump()
    )


def judge_case(
    agent: Agent,
    case: QualitativeCase,
    *,
    max_repair_attempts: int = 2,
) -> dict[CriterionId, JudgeCriterionDecision]:
    """Evalúa independientemente todos los criterios aplicables de un caso."""

    decisions = {}

    for criterion_id in CRITERION_IDS:
        applicability = (
            case.criteria_applicability[
                criterion_id
            ]
        )

        if not applicability.applicable:
            continue

        decisions[criterion_id] = (
            judge_case_criterion(
                agent,
                case,
                criterion_id,
                max_repair_attempts=max_repair_attempts,
            )
        )

    return decisions


def build_judge_case_prediction(
    case: QualitativeCase,
    decisions: dict[
        CriterionId,
        JudgeCriterionDecision,
    ],
) -> JudgeCasePrediction:
    """Construye y valida la predicción reproducible de un caso."""

    applicable_criteria = {
        criterion_id
        for criterion_id, applicability
        in case.criteria_applicability.items()
        if applicability.applicable
    }
    predicted_criteria = set(
        decisions
    )

    if predicted_criteria != applicable_criteria:
        missing = sorted(
            applicable_criteria
            - predicted_criteria
        )
        unexpected = sorted(
            predicted_criteria
            - applicable_criteria
        )

        raise ValueError(
            "La predicción del judge debe contener exactamente "
            "los criterios aplicables. "
            f"Faltantes: {missing}; "
            f"no aplicables: {unexpected}."
        )

    presentation = build_case_presentation(
        case
    )
    valid_evidence_refs = set(
        presentation.evidence_refs
    )

    for criterion_id, decision in decisions.items():
        invalid_refs = (
            set(decision.evidence_refs)
            - valid_evidence_refs
        )

        if invalid_refs:
            raise ValueError(
                f"El criterio {criterion_id} contiene referencias "
                "de evidencia inexistentes: "
                f"{sorted(invalid_refs)}."
            )

    return JudgeCasePrediction(
        schema_version=JUDGE_PREDICTION_SCHEMA_VERSION,
        case_schema_version=case.schema_version,
        case_view_version=case.case_view_version,
        presentation_version=presentation.version,
        rubric_version=RUBRIC_VERSION,
        judge_prompt_version=JUDGE_PROMPT_VERSION,
        case_id=case.case_id,
        criteria=decisions,
    )