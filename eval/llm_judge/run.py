"""Ejecución reproducible de una evaluación mediante LLM-as-judge."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Permite ejecutar exactamente:
#     python eval/llm_judge/run.py
REPO_ROOT = Path(__file__).resolve().parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from eval.llm_judge.configs.judge_configs import JUDGE_CONFIG
from eval.llm_judge.persistence import (
    RESULTS_DIR,
    load_judge_evaluation_manifest,
)
from eval.llm_judge.runner import (
    resume_judge_evaluation,
    start_judge_evaluation,
)


def execute_judge_config(
    judge_config: dict[str, Any],
    *,
    results_dir: Path = RESULTS_DIR,
) -> dict[str, Any]:
    """Inicia o reanuda la evaluación declarada por una configuración."""

    dataset_id = judge_config[
        "dataset_id"
    ]
    judge_eval_id = judge_config[
        "judge_eval_id"
    ]

    try:
        load_judge_evaluation_manifest(
            dataset_id,
            judge_eval_id,
            results_dir=results_dir,
        )
    except FileNotFoundError:
        predictions = start_judge_evaluation(
            dataset_id,
            judge_eval_id,
            split=judge_config["split"],
            judge_llm_config=judge_config[
                "judge_llm_config"
            ],
            max_repair_attempts=judge_config[
                "max_repair_attempts"
            ],
            results_dir=results_dir,
        )
        mode = "start"
    else:
        predictions = resume_judge_evaluation(
            dataset_id,
            judge_eval_id,
            results_dir=results_dir,
        )
        mode = "resume"

    return {
        "mode": mode,
        "predictions": predictions,
    }


def main() -> int:
    if JUDGE_CONFIG is None:
        print(
            "No hay una JUDGE_CONFIG activa. "
            "Definí explícitamente la configuración del judge "
            "en eval/llm_judge/configs/judge_configs.py.",
            file=sys.stderr,
        )
        return 1

    result = execute_judge_config(
        JUDGE_CONFIG
    )

    dataset_id = JUDGE_CONFIG[
        "dataset_id"
    ]
    judge_eval_id = JUDGE_CONFIG[
        "judge_eval_id"
    ]
    output_dir = (
        RESULTS_DIR
        / dataset_id
        / "judge_evaluations"
        / judge_eval_id
    )

    action = (
        "iniciada"
        if result["mode"] == "start"
        else "reanudada"
    )

    print(
        f"Evaluación del judge {action}: {judge_eval_id}"
    )
    print(
        f"Dataset: {dataset_id}"
    )
    print(
        f"Casos completos: {len(result['predictions'])}"
    )
    print()
    print(
        f"Manifest: {output_dir / 'manifest.json'}"
    )
    print(
        f"Predicciones: {output_dir / 'predictions.jsonl'}"
    )
    print(
        f"Progreso: {output_dir / 'progress.json'}"
    )
    print(
        f"Traza: {output_dir / 'trace.jsonl'}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())