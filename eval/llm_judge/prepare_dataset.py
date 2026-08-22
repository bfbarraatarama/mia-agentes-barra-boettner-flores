"""Preparación reproducible de datasets para evaluación cualitativa."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Permite ejecutar exactamente:
#     python eval/llm_judge/prepare_dataset.py
REPO_ROOT = Path(__file__).resolve().parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from eval.llm_judge.configs.dataset_configs import DATASET_CONFIG
from eval.llm_judge.persistence import (
    RESULTS_DIR,
    create_qualitative_dataset,
)
from eval.llm_judge.sampling import (
    RANDOM_STRATIFIED_BY_SCENARIO_METHOD,
    collect_trial_candidates,
    sample_trials_by_scenario,
)
from eval.persistence import load_run_results


def _optional_set(
    values: list[str] | None,
) -> set[str] | None:
    """Convierte un filtro configurado en conjunto sin alterar None."""

    if values is None:
        return None

    return set(values)


def prepare_qualitative_dataset(
    dataset_config: dict[str, Any],
    *,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    """Prepara y persiste un dataset cualitativo configurado."""

    run_ids = dataset_config["run_ids"]

    if not run_ids:
        raise ValueError(
            "run_ids debe contener al menos un run_id."
        )

    if len(run_ids) != len(set(run_ids)):
        raise ValueError(
            "run_ids no puede contener duplicados."
        )

    sampling = dataset_config["sampling"]

    if (
        sampling["method"]
        != RANDOM_STRATIFIED_BY_SCENARIO_METHOD
    ):
        raise ValueError(
            "Método de sampling no soportado: "
            f"{sampling['method']!r}."
        )

    run_results = {
        run_id: load_run_results(run_id)
        for run_id in run_ids
    }

    population = dataset_config["population"]

    candidates = collect_trial_candidates(
        run_results,
        agent_configs=_optional_set(
            population["agent_configs"]
        ),
        llm_configs=_optional_set(
            population["llm_configs"]
        ),
        trial_configs=_optional_set(
            population["trial_configs"]
        ),
        scenarios=_optional_set(
            population["scenarios"]
        ),
    )


    sampled_trials = sample_trials_by_scenario(
        candidates,
        seed=sampling["seed"],
        cases_per_scenario=sampling[
            "cases_per_scenario"
        ],
        dev_per_scenario=sampling[
            "dev_per_scenario"
        ],
    )

    manifest = create_qualitative_dataset(
        dataset_config,
        sampled_trials,
        results_dir=results_dir,
    )

    return {
        "manifest": manifest,
        "eligible_trials": len(candidates),
        "sampled_trials": sampled_trials,
    }


def main() -> int:
    result = prepare_qualitative_dataset(
        DATASET_CONFIG,
    )

    manifest = result["manifest"]
    dataset_id = manifest["dataset_id"]
    output_dir = RESULTS_DIR / dataset_id

    print(
        f"Dataset cualitativo preparado: {dataset_id}"
    )
    print(
        f"Trials elegibles: {result['eligible_trials']}"
    )
    print(
        "Casos seleccionados: "
        f"{manifest['counts']['total']} "
        f"({manifest['counts']['dev']} dev, "
        f"{manifest['counts']['holdout']} holdout)"
    )
    print()
    print(
        f"Manifest: {output_dir / 'manifest.json'}"
    )
    print(
        f"Casos ciegos: {output_dir / 'cases.jsonl'}"
    )
    print(
        "Procedencia de los casos: "
        f"{output_dir / 'case_sources.jsonl'}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())