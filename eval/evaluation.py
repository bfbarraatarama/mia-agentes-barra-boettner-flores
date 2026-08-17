"""Evaluación derivada de corridas persistidas de M3."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from eval import persistence
from eval.metrics import METRICS
from eval.run_execution import is_run_complete


def _resolve_metrics(
    evaluation_config: dict[str, Any],
) -> dict[str, Any]:
    """Resuelve las métricas declaradas por una evaluación."""

    resolved = {}

    for metric_name in evaluation_config["metrics"]:
        if metric_name not in METRICS:
            raise ValueError(
                f"Métrica de evaluación desconocida: {metric_name!r}."
            )

        resolved[metric_name] = METRICS[metric_name]

    return resolved


def create_evaluation(
    eval_id: str,
    run_id: str,
    evaluation_config: dict[str, Any],
    *,
    runs_dir: Path = persistence.RUNS_DIR,
    evaluations_dir: Path = persistence.EVALUATIONS_DIR,
) -> None:
    """Crea una evaluación nueva sobre una corrida completa."""

    try:
        manifest = persistence.load_run_manifest(
            run_id,
            results_dir=runs_dir,
        )
        run_result = persistence.load_run_results(
            run_id,
            results_dir=runs_dir,
        )
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"No se puede crear el eval_id {eval_id!r}: "
            f"el run_id {run_id!r} no tiene ambos artefactos."
        ) from error

    if not is_run_complete(
        manifest,
        run_result,
    ):
        raise ValueError(
            f"No se puede crear el eval_id {eval_id!r}: "
            f"el run_id {run_id!r} no está completo."
        )

    persistence.initialize_evaluation(
        eval_id=eval_id,
        run_id=run_id,
        evaluation_config=evaluation_config,
        results_dir=evaluations_dir,
    )


def start_evaluation(
    eval_id: str,
    run_id: str,
    evaluation_config: dict[str, Any],
    *,
    runs_dir: Path = persistence.RUNS_DIR,
    evaluations_dir: Path = persistence.EVALUATIONS_DIR,
) -> dict[str, Any]:
    """Crea y ejecuta una evaluación sobre una corrida completa."""

    metric_functions = _resolve_metrics(
        evaluation_config
    )

    create_evaluation(
        eval_id=eval_id,
        run_id=run_id,
        evaluation_config=evaluation_config,
        runs_dir=runs_dir,
        evaluations_dir=evaluations_dir,
    )

    run_result = persistence.load_run_results(
        run_id,
        results_dir=runs_dir,
    )

    results = []

    for case in run_result["results"]:
        metrics = {
            metric_name: metric_function(case["trials"])
            for metric_name, metric_function
            in metric_functions.items()
        }

        results.append({
            "agent_config": case["agent_config"],
            "llm_config": case["llm_config"],
            "trial_config": case["trial_config"],
            "scenario": case["scenario"],
            "metrics": metrics,
        })

    evaluation_result = {
        "eval_id": eval_id,
        "run_id": run_id,
        "results": results,
    }

    persistence.write_evaluation_results(
        eval_id,
        evaluation_result,
        results_dir=evaluations_dir,
    )

    return evaluation_result