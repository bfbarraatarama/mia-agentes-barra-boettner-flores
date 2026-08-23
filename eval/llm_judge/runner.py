"""Ejecución reanudable de evaluaciones mediante LLM-as-judge."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from mia_agents.protocols import Agent

from eval.configs.llm_configs import build_llm_client
from eval.llm_judge.judge import (
    build_judge_case_prediction,
    judge_case_criterion,
)
from eval.llm_judge.models import (
    CaseSplit,
    JudgeCasePrediction,
)
from eval.llm_judge.persistence import (
    RESULTS_DIR,
    append_judge_trace_event,
    clear_judge_case_progress,
    create_judge_evaluation,
    load_judge_case_predictions,
    load_judge_evaluation_progress,
    load_qualitative_cases,
    require_current_judge_evaluation,
    save_judge_case_prediction,
    save_judge_criterion_progress,
)
from eval.llm_judge.rubric import CRITERION_IDS
from student_framework import build_agent


def _build_judge_agent(
    manifest: dict,
    *,
    trace_callback: Callable[
        [dict[str, Any]],
        None,
    ],
) -> Agent:
    """Reconstruye el judge desde la configuración efectiva persistida."""

    llm_client = build_llm_client(
        dict(
            manifest[
                "judge"
            ][
                "effective_llm_config"
            ]
        )
    )

    return build_agent({
        "llm_client": llm_client,
        "system_prompt": manifest[
            "judge"
        ][
            "system_prompt"
        ],
        "register_default_tools": False,
        "trace_callback": trace_callback,
    })


def _run_judge_evaluation(
    manifest: dict,
    *,
    results_dir: Path,
) -> list[JudgeCasePrediction]:
    """Completa únicamente casos y criterios aún pendientes."""

    dataset_id = manifest[
        "dataset_id"
    ]
    judge_eval_id = manifest[
        "judge_eval_id"
    ]
    case_ids = list(
        manifest[
            "case_ids"
        ]
    )

    cases = load_qualitative_cases(
        dataset_id,
        results_dir=results_dir,
    )
    cases_by_id = {
        case.case_id: case
        for case in cases
    }

    missing_case_ids = [
        case_id
        for case_id in case_ids
        if case_id not in cases_by_id
    ]

    if missing_case_ids:
        raise ValueError(
            "La evaluación del judge referencia casos "
            f"inexistentes: {missing_case_ids}."
        )

    predictions = load_judge_case_predictions(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )
    predictions_by_id = {
        prediction.case_id: prediction
        for prediction in predictions
    }

    progress = load_judge_evaluation_progress(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    for completed_case_id in (
        set(progress)
        & set(predictions_by_id)
    ):
        clear_judge_case_progress(
            dataset_id,
            judge_eval_id,
            completed_case_id,
            results_dir=results_dir,
        )

    pending_case_ids = [
        case_id
        for case_id in case_ids
        if case_id not in predictions_by_id
    ]

    if not pending_case_ids:
        return [
            predictions_by_id[
                case_id
            ]
            for case_id in case_ids
        ]

    progress = load_judge_evaluation_progress(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    trace_context: dict[str, str | None] = {
        "case_id": None,
        "criterion_id": None,
    }

    def trace_callback(
        event: dict[str, Any],
    ) -> None:
        case_id = trace_context[
            "case_id"
        ]
        criterion_id = trace_context[
            "criterion_id"
        ]

        if (
            case_id is None
            or criterion_id is None
        ):
            raise RuntimeError(
                "Se recibió una traza del judge fuera "
                "de un criterio activo."
            )

        append_judge_trace_event(
            dataset_id,
            judge_eval_id,
            case_id,
            criterion_id,
            event,
            results_dir=results_dir,
        )

    agent = _build_judge_agent(
        manifest,
        trace_callback=trace_callback,
    )
    max_repair_attempts = manifest[
        "judge"
    ][
        "max_repair_attempts"
    ]

    for case_id in pending_case_ids:
        case = cases_by_id[
            case_id
        ]
        decisions = dict(
            progress.get(
                case_id,
                {},
            )
        )

        for criterion_id in CRITERION_IDS:
            applicability = (
                case.criteria_applicability[
                    criterion_id
                ]
            )

            if (
                not applicability.applicable
                or criterion_id in decisions
            ):
                continue

            trace_context[
                "case_id"
            ] = case_id
            trace_context[
                "criterion_id"
            ] = criterion_id

            try:
                decision = judge_case_criterion(
                    agent,
                    case,
                    criterion_id,
                    max_repair_attempts=(
                        max_repair_attempts
                    ),
                )
            finally:
                trace_context[
                    "case_id"
                ] = None
                trace_context[
                    "criterion_id"
                ] = None

            save_judge_criterion_progress(
                dataset_id,
                judge_eval_id,
                case_id,
                criterion_id,
                decision,
                results_dir=results_dir,
            )
            decisions[
                criterion_id
            ] = decision

        prediction = (
            build_judge_case_prediction(
                case,
                decisions,
            )
        )

        save_judge_case_prediction(
            dataset_id,
            judge_eval_id,
            prediction,
            results_dir=results_dir,
        )
        clear_judge_case_progress(
            dataset_id,
            judge_eval_id,
            case_id,
            results_dir=results_dir,
        )
        predictions_by_id[
            case_id
        ] = prediction

    return [
        predictions_by_id[
            case_id
        ]
        for case_id in case_ids
    ]


def start_judge_evaluation(
    dataset_id: str,
    judge_eval_id: str,
    *,
    split: CaseSplit,
    judge_llm_config: str,
    max_repair_attempts: int = 2,
    results_dir: Path = RESULTS_DIR,
) -> list[JudgeCasePrediction]:
    """Crea y ejecuta una evaluación nueva del judge."""

    create_judge_evaluation(
        dataset_id,
        judge_eval_id,
        split=split,
        judge_llm_config=judge_llm_config,
        max_repair_attempts=max_repair_attempts,
        results_dir=results_dir,
    )

    manifest = require_current_judge_evaluation(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    return _run_judge_evaluation(
        manifest,
        results_dir=results_dir,
    )


def resume_judge_evaluation(
    dataset_id: str,
    judge_eval_id: str,
    *,
    results_dir: Path = RESULTS_DIR,
) -> list[JudgeCasePrediction]:
    """Reanuda una evaluación usando exclusivamente su manifest."""

    manifest = require_current_judge_evaluation(
        dataset_id,
        judge_eval_id,
        results_dir=results_dir,
    )

    return _run_judge_evaluation(
        manifest,
        results_dir=results_dir,
    )