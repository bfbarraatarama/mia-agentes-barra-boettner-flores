"""Ejecución de corridas para M3."""

from __future__ import annotations
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path

from typing import Any

from eval import persistence
from eval.experiment import run_case


def _build_pending_run_plan(
    manifest: dict[str, Any],
    run_result: dict[str, Any],
) -> dict[str, Any]:
    """Construye los trials pendientes definidos por el manifest del run."""

    run = manifest["run"]

    completed_trials_by_case = {
        (
            result["agent_config"],
            result["llm_config"],
            result["trial_config"],
            result["scenario"],
        ): {
            trial["trial_index"]
            for trial in result["trials"]
        }
        for result in run_result["results"]
    }

    cases = []

    for system in run["systems"]:
        for trial_config_name in run["trial_configs"]:
            for scenario_spec in run["scenarios"]:
                case_key = (
                    system["agent_config"],
                    system["llm_config"],
                    trial_config_name,
                    scenario_spec,
                )

                completed_trial_indices = completed_trials_by_case.get(
                    case_key,
                    set(),
                )

                pending_trial_indices = [
                    trial_index
                    for trial_index in range(
                        1,
                        run["trials_per_case"] + 1,
                    )
                    if trial_index not in completed_trial_indices
                ]

                if not pending_trial_indices:
                    continue

                cases.append({
                    "agent_config": system["agent_config"],
                    "llm_config": system["llm_config"],
                    "trial_config": trial_config_name,
                    "scenario": scenario_spec,
                    "trial_indices": pending_trial_indices,
                })

    return {
        "cases": cases,
        "agent_configs": deepcopy(manifest["agent_configs"]),
        "llm_configs": deepcopy(manifest["llm_configs"]),
        "trial_configs": deepcopy(
            manifest["trial_configs"]
        ),
    }


def is_run_complete(
    manifest: dict[str, Any],
    run_result: dict[str, Any],
) -> bool:
    """Indica si todos los trials definidos por el run están persistidos."""

    return not _build_pending_run_plan(
        manifest,
        run_result,
    )["cases"]


def _add_trial_result(
    run_result: dict[str, Any],
    case: dict[str, str],
    trial: dict[str, Any],
) -> None:
    """Incorpora un trial completo al caso correspondiente."""

    case_result = next(
        (
            result
            for result in run_result["results"]
            if (
                result["agent_config"] == case["agent_config"]
                and result["llm_config"] == case["llm_config"]
                and result["trial_config"]
                == case["trial_config"]
                and result["scenario"] == case["scenario"]
            )
        ),
        None,
    )

    if case_result is None:
        case_result = {
            "agent_config": case["agent_config"],
            "llm_config": case["llm_config"],
            "trial_config": case["trial_config"],
            "scenario": case["scenario"],
            "trials": [],
        }
        run_result["results"].append(case_result)

    if any(
        existing_trial["trial_index"] == trial["trial_index"]
        for existing_trial in case_result["trials"]
    ):
        raise ValueError(
            "El trial ya existe en los resultados: "
            f"{case['agent_config']} / "
            f"{case['llm_config']} / "
            f"{case['trial_config']} / "
            f"{case['scenario']} / "
            f"trial {trial['trial_index']}."
        )

    case_result["trials"].append(
        deepcopy(trial)
    )
    case_result["trials"].sort(
        key=lambda item: item["trial_index"]
    )


def _execute_pending_trials(
    run_id: str,
    *,
    results_dir: Path = persistence.RUNS_DIR,
    progress_callback: Callable[
        [int, int, dict[str, str], dict[str, Any]],
        None,
    ] | None = None,
) -> dict[str, Any]:
    """Ejecuta los trials pendientes de una corrida persistida."""

    manifest = persistence.load_run_manifest(
        run_id,
        results_dir=results_dir,
    )
    run_result = persistence.load_run_results(
        run_id,
        results_dir=results_dir,
    )

    plan = _build_pending_run_plan(
        manifest,
        run_result,
    )

    run = manifest["run"]

    total_trials = (
        len(run["systems"])
        * len(run["trial_configs"])
        * len(run["scenarios"])
        * run["trials_per_case"]
    )

    completed_trials = sum(
        len(result["trials"])
        for result in run_result["results"]
    )

    for case in plan["cases"]:
        case_identity = {
            "agent_config": case["agent_config"],
            "llm_config": case["llm_config"],
            "trial_config": case["trial_config"],
            "scenario": case["scenario"],
        }

        def on_trial_complete(
            trial: dict[str, Any],
        ) -> None:
            nonlocal completed_trials

            _add_trial_result(
                run_result,
                case_identity,
                trial,
            )

            persistence.write_run_results(
                run_id,
                run_result,
                results_dir=results_dir,
            )

            completed_trials += 1

            if progress_callback is not None:
                progress_callback(
                    completed_trials,
                    total_trials,
                    dict(case_identity),
                    trial,
                )

        run_case(
            scenario_spec=case["scenario"],
            agent_config_name=case["agent_config"],
            llm_config_name=case["llm_config"],
            agent_config=plan["agent_configs"][
                case["agent_config"]
            ],
            llm_config=plan["llm_configs"][
                case["llm_config"]
            ],
            trial_config=plan["trial_configs"][
                case["trial_config"]
            ],
            trial_indices=list(case["trial_indices"]),
            trial_callback=on_trial_complete,
        )

    return deepcopy(run_result)


def start_run(
    run_id: str,
    run_config: dict[str, Any],
    *,
    results_dir: Path = persistence.RUNS_DIR,
    progress_callback: Callable[
        [int, int, dict[str, str], dict[str, Any]],
        None,
    ] | None = None,
) -> dict[str, Any]:
    """Crea y ejecuta una nueva corrida."""

    persistence.initialize_run(
        run_id=run_id,
        run_config=run_config,
        results_dir=results_dir,
    )
    return _execute_pending_trials(
        run_id,
        results_dir=results_dir,
        progress_callback=progress_callback,
    )


def resume_run(
    run_id: str,
    *,
    results_dir: Path = persistence.RUNS_DIR,
    progress_callback: Callable[
        [int, int, dict[str, str], dict[str, Any]],
        None,
    ] | None = None,
) -> dict[str, Any]:
    """Reanuda y ejecuta una corrida existente."""

    persistence.require_existing_run(
        run_id,
        results_dir=results_dir,
    )

    return _execute_pending_trials(
        run_id,
        results_dir=results_dir,
        progress_callback=progress_callback,
    )