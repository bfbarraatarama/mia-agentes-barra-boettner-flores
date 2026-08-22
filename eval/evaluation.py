"""Evaluación derivada de corridas persistidas de M3."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from eval import persistence
from eval.analyses import ANALYSES
from eval.metrics import METRICS
from eval.run_execution import is_run_complete


_CONFIG_SECTIONS = (
    ("agent_config", "agent_configs"),
    ("llm_config", "llm_configs"),
    ("trial_config", "trial_configs"),
    ("scenario", "scenario_metadata"),
)


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


def _resolve_analyses(
    evaluation_config: dict[str, Any],
) -> dict[str, Any]:
    """Resuelve los análisis declarados por una evaluación."""

    resolved = {}

    for analysis_name in evaluation_config.get("analyses", []):
        if analysis_name not in ANALYSES:
            raise ValueError(
                "Análisis de evaluación desconocido: "
                f"{analysis_name!r}."
            )

        resolved[analysis_name] = ANALYSES[analysis_name]

    return resolved


def _validate_run_ids(run_ids: list[str]) -> None:
    """Valida la colección de runs fuente de una evaluación."""

    if not run_ids:
        raise ValueError(
            "run_ids debe contener al menos un run_id."
        )

    if len(set(run_ids)) != len(run_ids):
        raise ValueError(
            "run_ids no puede contener duplicados."
        )


def _load_complete_runs(
    eval_id: str,
    run_ids: list[str],
    runs_dir: Path,
) -> list[dict[str, Any]]:
    """Carga los runs completos que alimentan una evaluación."""

    sources = []

    for run_id in run_ids:
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

        sources.append({
            "run_id": run_id,
            "manifest": manifest,
            "result": run_result,
        })

    return sources


def _validate_compatible_manifests(
    run_sources: list[dict[str, Any]],
) -> None:
    """Evita reutilizar un nombre para definiciones distintas."""

    seen: dict[tuple[str, str], Any] = {}

    for source in run_sources:
        manifest = source["manifest"]

        for config_kind, section_name in _CONFIG_SECTIONS:
            for name, definition in manifest.get(
                section_name,
                {},
            ).items():
                key = (config_kind, name)

                if key not in seen:
                    seen[key] = definition
                    continue

                if seen[key] != definition:
                    raise ValueError(
                        f"Definición incompatible de {config_kind} "
                        f"{name!r}."
                    )


def _group_cases(
    run_sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Agrupa trials de la misma condición lógica entre runs."""

    grouped: dict[
        tuple[str, str, str, str],
        dict[str, Any],
    ] = {}

    for source in run_sources:
        run_id = source["run_id"]

        for case in source["result"]["results"]:
            key = (
                case["agent_config"],
                case["llm_config"],
                case["trial_config"],
                case["scenario"],
            )

            if key not in grouped:
                grouped[key] = {
                    "agent_config": case["agent_config"],
                    "llm_config": case["llm_config"],
                    "trial_config": case["trial_config"],
                    "scenario": case["scenario"],
                    "source_run_ids": [],
                    "trials": [],
                }

            group = grouped[key]

            if run_id not in group["source_run_ids"]:
                group["source_run_ids"].append(run_id)

            for trial in case["trials"]:
                trial_with_source = dict(trial)
                trial_with_source["source_run_id"] = run_id
                group["trials"].append(trial_with_source)

    return list(grouped.values())


def create_evaluation(
    eval_id: str,
    run_ids: list[str],
    evaluation_config: dict[str, Any],
    *,
    runs_dir: Path = persistence.RUNS_DIR,
    evaluations_dir: Path = persistence.EVALUATIONS_DIR,
) -> None:
    """Crea una evaluación nueva sobre una o más corridas completas."""

    _validate_run_ids(run_ids)

    run_sources = _load_complete_runs(
        eval_id,
        run_ids,
        runs_dir,
    )

    _validate_compatible_manifests(run_sources)

    persistence.initialize_evaluation(
        eval_id=eval_id,
        run_ids=run_ids,
        evaluation_config=evaluation_config,
        results_dir=evaluations_dir,
    )


def start_evaluation(
    eval_id: str,
    run_ids: list[str],
    evaluation_config: dict[str, Any],
    *,
    runs_dir: Path = persistence.RUNS_DIR,
    evaluations_dir: Path = persistence.EVALUATIONS_DIR,
) -> dict[str, Any]:
    """Crea y ejecuta una evaluación sobre una o más corridas completas."""

    metric_functions = _resolve_metrics(
        evaluation_config
    )
    analysis_functions = _resolve_analyses(
        evaluation_config
    )

    _validate_run_ids(run_ids)

    create_evaluation(
        eval_id=eval_id,
        run_ids=run_ids,
        evaluation_config=evaluation_config,
        runs_dir=runs_dir,
        evaluations_dir=evaluations_dir,
    )

    run_sources = _load_complete_runs(
        eval_id,
        run_ids,
        runs_dir,
    )

    grouped_cases = _group_cases(run_sources)

    results = []

    for case in grouped_cases:
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
            "source_run_ids": case["source_run_ids"],
            "trial_count": len(case["trials"]),
            "metrics": metrics,
        })

    analyses = {
        analysis_name: analysis_function(
            run_sources,
        )
        for analysis_name, analysis_function
        in analysis_functions.items()
    }

    evaluation_result = {
        "eval_id": eval_id,
        "run_ids": list(run_ids),
        "results": results,
        "analyses": analyses,
    }

    persistence.write_evaluation_results(
        eval_id,
        evaluation_result,
        results_dir=evaluations_dir,
    )

    return evaluation_result