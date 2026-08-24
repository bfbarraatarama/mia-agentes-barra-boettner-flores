"""Reportes derivados de evaluaciones cualitativas y LLM-as-judge."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from eval.llm_judge.comparison import (
    AgreementStats,
    HumanAgreementReport,
    JudgeAgreementReport,
)
from eval.llm_judge.models import CaseSplit
from eval.llm_judge.persistence import (
    RESULTS_DIR,
    load_judge_case_predictions,
    load_judge_evaluation_manifest,
    load_judge_evaluation_progress,
    load_judge_trace,
)
from eval.llm_judge.rubric import (
    CRITERION_IDS,
    CriterionId,
)


@dataclass(frozen=True)
class JudgeTraceSummary:
    """Resumen operativo de las inferencias efectivamente realizadas."""

    trace_events: int
    llm_calls: int
    successful_llm_calls: int
    failed_llm_calls: int
    repair_llm_calls: int
    input_tokens: int | None
    output_tokens: int | None


@dataclass(frozen=True)
class JudgeEvaluationStatus:
    """Estado reconstruible de una evaluación del judge."""

    dataset_id: str
    judge_eval_id: str
    split: CaseSplit
    judge_llm_config: str
    effective_llm_config: dict[str, Any]
    max_repair_attempts: int
    total_cases: int
    completed_case_ids: tuple[str, ...]
    pending_case_ids: tuple[str, ...]
    checkpointed_criteria: dict[
        str,
        tuple[CriterionId, ...],
    ]
    completed_with_checkpoint_case_ids: tuple[str, ...]
    trace: JudgeTraceSummary


def _is_repair_llm_call(
    event: dict[str, Any],
) -> bool:
    """Indica si una llamada fue realizada después de un error de validación."""

    messages = event.get(
        "messages",
        [],
    )

    if not isinstance(
        messages,
        list,
    ):
        return False

    return any(
        isinstance(message, dict)
        and message.get("role") == "tool"
        and str(
            message.get(
                "content",
                "",
            )
        ).startswith(
            "Error de validación:"
        )
        for message in messages
    )


def _complete_token_total(
    successful_calls: list[
        dict[str, Any]
    ],
    token_field: str,
) -> int | None:
    """Suma tokens sólo cuando todas las respuestas los informan."""

    values = []

    for event in successful_calls:
        response = event.get(
            "response"
        )

        if not isinstance(
            response,
            dict,
        ):
            return None

        value = response.get(
            token_field
        )

        if type(value) is not int:
            return None

        values.append(
            value
        )

    return sum(
        values
    )


def build_judge_evaluation_status(
    dataset_id: str,
    judge_eval_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> JudgeEvaluationStatus:
    """Reconstruye estado, progreso y costo desde los artefactos fuente."""

    manifest = load_judge_evaluation_manifest(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    predictions = load_judge_case_predictions(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    progress = load_judge_evaluation_progress(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    trace = load_judge_trace(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    case_ids = tuple(
        manifest[
            "case_ids"
        ]
    )
    expected_case_ids = set(
        case_ids
    )
    completed_case_id_set = {
        prediction.case_id
        for prediction in predictions
    }

    unexpected_completed = (
        completed_case_id_set
        - expected_case_ids
    )

    if unexpected_completed:
        raise ValueError(
            "La evaluación contiene predicciones para "
            "case_id fuera de su manifest: "
            f"{sorted(unexpected_completed)}."
        )

    completed_case_ids = tuple(
        case_id
        for case_id in case_ids
        if case_id in completed_case_id_set
    )
    pending_case_ids = tuple(
        case_id
        for case_id in case_ids
        if case_id not in completed_case_id_set
    )

    checkpointed_criteria = {
        case_id: tuple(
            criterion_id
            for criterion_id in CRITERION_IDS
            if criterion_id in criteria
        )
        for case_id, criteria in progress.items()
        if criteria
    }

    completed_with_checkpoint_case_ids = tuple(
        case_id
        for case_id in case_ids
        if (
            case_id in completed_case_id_set
            and case_id in checkpointed_criteria
        )
    )

    llm_calls = [
        event
        for event in trace
        if event.get("type") == "llm_call"
    ]
    successful_llm_calls = [
        event
        for event in llm_calls
        if "response" in event
    ]
    failed_llm_calls = [
        event
        for event in llm_calls
        if "error" in event
    ]

    return JudgeEvaluationStatus(
        dataset_id=dataset_id,
        judge_eval_id=judge_eval_id,
        split=manifest["split"],
        judge_llm_config=manifest[
            "judge"
        ][
            "llm_config"
        ],
        effective_llm_config=dict(
            manifest[
                "judge"
            ][
                "effective_llm_config"
            ]
        ),
        max_repair_attempts=manifest[
            "judge"
        ][
            "max_repair_attempts"
        ],
        total_cases=len(
            case_ids
        ),
        completed_case_ids=completed_case_ids,
        pending_case_ids=pending_case_ids,
        checkpointed_criteria=checkpointed_criteria,
        completed_with_checkpoint_case_ids=(
            completed_with_checkpoint_case_ids
        ),
        trace=JudgeTraceSummary(
            trace_events=len(
                trace
            ),
            llm_calls=len(
                llm_calls
            ),
            successful_llm_calls=len(
                successful_llm_calls
            ),
            failed_llm_calls=len(
                failed_llm_calls
            ),
            repair_llm_calls=sum(
                _is_repair_llm_call(
                    event
                )
                for event in llm_calls
            ),
            input_tokens=_complete_token_total(
                successful_llm_calls,
                "input_tokens",
            ),
            output_tokens=_complete_token_total(
                successful_llm_calls,
                "output_tokens",
            ),
        ),
    )


def _metric_text(
    value: float | None,
) -> str:
    if value is None:
        return "N/A"

    return f"{value:.3f}"


def _token_text(
    value: int | None,
) -> str:
    if value is None:
        return "N/A (conteo incompleto)"

    return str(
        value
    )


def render_judge_evaluation_status(
    status: JudgeEvaluationStatus,
) -> str:
    """Renderiza el estado operativo de una evaluación del judge."""

    effective_config = json.dumps(
        status.effective_llm_config,
        ensure_ascii=False,
        sort_keys=True,
    )
    checkpoint_count = sum(
        len(criteria)
        for criteria
        in status.checkpointed_criteria.values()
    )

    lines = [
        "LLM-as-judge — estado de evaluación",
        (
            f"- Dataset: {status.dataset_id}"
        ),
        (
            f"- Judge evaluation: {status.judge_eval_id}"
        ),
        (
            f"- Split: {status.split}"
        ),
        (
            "- Configuración nominal del judge: "
            f"{status.judge_llm_config}"
        ),
        (
            "- Configuración efectiva: "
            f"{effective_config}"
        ),
        (
            "- Máximo de reparaciones por criterio: "
            f"{status.max_repair_attempts}"
        ),
        (
            "- Casos completos: "
            f"{len(status.completed_case_ids)}"
            f"/{status.total_cases}"
        ),
        (
            "- Casos pendientes: "
            + (
                ", ".join(
                    status.pending_case_ids
                )
                if status.pending_case_ids
                else "ninguno"
            )
        ),
        (
            "- Criterios checkpointed: "
            f"{checkpoint_count} "
            f"en {len(status.checkpointed_criteria)} casos"
        ),
        (
            "- Llamadas LLM: "
            f"{status.trace.llm_calls} "
            f"(respuesta={status.trace.successful_llm_calls}, "
            f"error={status.trace.failed_llm_calls}, "
            f"repair={status.trace.repair_llm_calls})"
        ),
        (
            "- Tokens de entrada: "
            f"{_token_text(status.trace.input_tokens)}"
        ),
        (
            "- Tokens de salida: "
            f"{_token_text(status.trace.output_tokens)}"
        ),
    ]

    if status.completed_with_checkpoint_case_ids:
        lines.append(
            "- Advertencia: hay checkpoints residuales "
            "para casos ya consolidados: "
            + ", ".join(
                status.completed_with_checkpoint_case_ids
            )
        )

    return "\n".join(
        lines
    )


def _render_agreement_stats(
    stats: AgreementStats,
    *,
    first_label: str,
    second_label: str,
) -> list[str]:
    confusion = stats.confusion

    return [
        (
            f"n={stats.n}; "
            f"agreement={_metric_text(stats.agreement)}; "
            f"kappa={_metric_text(stats.cohen_kappa)}"
        ),
        (
            f"  {first_label}=PASS / {second_label}=PASS: "
            f"{confusion.first_pass_second_pass}"
        ),
        (
            f"  {first_label}=PASS / {second_label}=FAIL: "
            f"{confusion.first_pass_second_fail}"
        ),
        (
            f"  {first_label}=FAIL / {second_label}=PASS: "
            f"{confusion.first_fail_second_pass}"
        ),
        (
            f"  {first_label}=FAIL / {second_label}=FAIL: "
            f"{confusion.first_fail_second_fail}"
        ),
    ]


def render_judge_agreement_report(
    report: JudgeAgreementReport,
) -> str:
    """Renderiza la comparación entre referencia humana y judge."""

    lines = [
        "Acuerdo humano ↔ LLM judge",
        f"- Dataset: {report.dataset_id}",
        f"- Judge evaluation: {report.judge_eval_id}",
        f"- Anotador humano: {report.annotator_id}",
        f"- Split: {report.split}",
        "",
        "Global (humano en filas, judge en columnas):",
        *_render_agreement_stats(
            report.overall,
            first_label="humano",
            second_label="judge",
        ),
        "",
        "Por criterio:",
    ]

    for criterion_id in CRITERION_IDS:
        lines.append(
            f"- {criterion_id}: "
            + _render_agreement_stats(
                report.by_criterion[
                    criterion_id
                ],
                first_label="humano",
                second_label="judge",
            )[0]
        )

    return "\n".join(
        lines
    )


def render_human_agreement_report(
    report: HumanAgreementReport,
) -> str:
    """Renderiza el acuerdo inter-anotador."""

    lines = [
        "Acuerdo humano ↔ humano",
        f"- Dataset: {report.dataset_id}",
        f"- Anotador A: {report.annotator_a_id}",
        f"- Anotador B: {report.annotator_b_id}",
        f"- Split: {report.split}",
        "",
        "Global (A en filas, B en columnas):",
        *_render_agreement_stats(
            report.overall,
            first_label="A",
            second_label="B",
        ),
        "",
        "Por criterio:",
    ]

    for criterion_id in CRITERION_IDS:
        lines.append(
            f"- {criterion_id}: "
            + _render_agreement_stats(
                report.by_criterion[
                    criterion_id
                ],
                first_label="A",
                second_label="B",
            )[0]
        )

    return "\n".join(
        lines
    )