"""Evaluación reproducible de M3."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Permite ejecutar exactamente:
#     python eval/run.py
REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from eval.evaluation import start_evaluation
from eval.persistence import RUNS_DIR, evaluation_dir
from eval.configs.evaluation_configs import M3_EVALUATION_CONFIG
from eval.configs.run_configs import (
    M3_FINAL_SELECTION_RUN_CONFIG,
)
from eval.run_execution import resume_run, start_run
from eval.report import (
    plot_success_rate,
    print_success_rate_summary,
    write_error_analysis_report,
)
from eval.analyses.tool_call_repair_analysis import (
    render_markdown as render_tool_call_repair_markdown,
)
from eval.analyses.attempt_recovery_analysis import (
    render_markdown as render_attempt_recovery_markdown,
)
from eval.analyses.efficiency_analysis import (
    render_markdown as render_efficiency_markdown,
)
from eval.analyses.context_analysis import (
    render_markdown as render_context_markdown,
)
from eval.llm_judge.configs.dataset_configs import (
    M3_FINAL_SELECTION_QUALITATIVE_DATASET_CONFIG,
)
from eval.llm_judge.configs.judge_configs import (
    M3_FINAL_SELECTION_JUDGE_CONFIG,
)
from eval.llm_judge.persistence import (
    RESULTS_DIR as LLM_JUDGE_RESULTS_DIR,
)
from eval.llm_judge.prepare_dataset import (
    execute_dataset_config,
)
from eval.llm_judge.report import (
    build_judge_system_summary,
    render_judge_system_summary,
)
from eval.llm_judge.run import (
    execute_judge_config,
)

RUNS = [
    (
        "m3-final-run-008",
        M3_FINAL_SELECTION_RUN_CONFIG,
    ),
]

EVALUATIONS = [
    (
        "m3-final-eval-008",
        [
            "m3-final-run-008",
        ],
    ),
]

QUALITATIVE_DATASET_CONFIG = (
    M3_FINAL_SELECTION_QUALITATIVE_DATASET_CONFIG
)
QUALITATIVE_JUDGE_CONFIG = (
    M3_FINAL_SELECTION_JUDGE_CONFIG
)

EVALUATION_CONFIG = M3_EVALUATION_CONFIG


def print_progress(
    completed_trials: int,
    total_trials: int,
    case: dict[str, str],
    trial: dict[str, Any],
) -> None:
    """Muestra el progreso de la corrida."""

    percentage = 100 * completed_trials / total_trials
    status = "SUCCESS" if trial["goal_achieved"] else "FAIL"

    print(
        f"[{completed_trials}/{total_trials} | {percentage:5.1f}%] "
        f"[{status}] "
        f"{case['agent_config']} / {case['llm_config']} / "
        f"{case['trial_config']} / {case['scenario']} "
        f"(trial {trial['trial_index']})",
        flush=True,
    )


def _run_evaluation(
    eval_id: str,
    run_ids: list[str],
) -> None:
    evaluation_result = start_evaluation(
        eval_id=eval_id,
        run_ids=run_ids,
        evaluation_config=EVALUATION_CONFIG,
    )

    evaluation_output_dir = evaluation_dir(eval_id)

    success_rate_plot_path = (
        evaluation_output_dir / "success_rate.png"
    )

    error_analysis_path = (
        evaluation_output_dir / "error_analysis.md"
    )

    attempt_recovery_analysis_path = (
        evaluation_output_dir
        / "attempt_recovery_analysis.md"
    )

    tool_call_repair_analysis_path = (
        evaluation_output_dir
        / "tool_call_repair_analysis.md"
    )

    efficiency_analysis_path = (
        evaluation_output_dir
        / "efficiency_analysis.md"
    )

    context_analysis_path = (
        evaluation_output_dir / "context_analysis.md"
    )

    print_success_rate_summary(
        evaluation_result
    )
    plot_success_rate(
        evaluation_result,
        success_rate_plot_path,
    )

    write_error_analysis_report(
        evaluation_result,
        error_analysis_path,
    )

    attempt_recovery_analysis = (
        evaluation_result["analyses"][
            "attempt_recovery_analysis"
        ]
    )

    attempt_recovery_analysis_path.write_text(
        render_attempt_recovery_markdown(
            attempt_recovery_analysis
        ),
        encoding="utf-8",
    )

    tool_call_repair_analysis = (
        evaluation_result["analyses"][
            "tool_call_repair_analysis"
        ]
    )

    tool_call_repair_analysis_path.write_text(
        render_tool_call_repair_markdown(
            tool_call_repair_analysis
        ),
        encoding="utf-8",
    )

    efficiency_analysis_path.write_text(
        render_efficiency_markdown(
            evaluation_result["analyses"]["efficiency_analysis"]
        ),
        encoding="utf-8",
    )

    context_analysis = (
        evaluation_result["analyses"]["context_analysis"]
    )

    context_analysis_path.write_text(
        render_context_markdown(context_analysis),
        encoding="utf-8",
    )

    print()

    for run_id in run_ids:
        print(
            "Manifest del run: "
            f"{RUNS_DIR / f'{run_id}.manifest.json'}"
        )
        print(
            "Resultados del run: "
            f"{RUNS_DIR / f'{run_id}.json'}"
        )
    print(
        "Manifest de la evaluación: "
        f"{evaluation_output_dir / 'manifest.json'}"
    )
    print(
        "Resultados de la evaluación: "
        f"{evaluation_output_dir / 'results.json'}"
    )
    print(
        f"Gráfico de success rate: {success_rate_plot_path}"
    )
    print(
        f"Análisis de errores: {error_analysis_path}"
    )
    print(
        "Análisis de recuperación entre attempts: "
        f"{attempt_recovery_analysis_path}"
    )
    print(
        "Análisis de reparación de tool calls: "
        f"{tool_call_repair_analysis_path}"
    )
    print(
        f"Análisis de eficiencia: {efficiency_analysis_path}"
    )
    print(
        "Análisis de presión de contexto: "
        f"{context_analysis_path}"
    )


def _run_qualitative_evaluation() -> None:
    dataset_result = execute_dataset_config(
        QUALITATIVE_DATASET_CONFIG
    )
    judge_result = execute_judge_config(
        QUALITATIVE_JUDGE_CONFIG
    )

    dataset_id = QUALITATIVE_DATASET_CONFIG[
        "dataset_id"
    ]
    judge_eval_id = QUALITATIVE_JUDGE_CONFIG[
        "judge_eval_id"
    ]
    judge_output_dir = (
        LLM_JUDGE_RESULTS_DIR
        / dataset_id
        / "judge_evaluations"
        / judge_eval_id
    )

    system_summary = build_judge_system_summary(
        dataset_id,
        judge_eval_id,
    )

    system_summary_json_path = (
        judge_output_dir
        / "system_summary.json"
    )
    system_summary_markdown_path = (
        judge_output_dir
        / "system_summary.md"
    )

    system_summary_json_path.write_text(
        json.dumps(
            system_summary,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    system_summary_markdown_path.write_text(
        render_judge_system_summary(
            system_summary
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(
        "Dataset cualitativo: "
        f"{dataset_id} ({dataset_result['mode']})"
    )
    print(
        "Evaluación LLM-as-judge: "
        f"{judge_eval_id} ({judge_result['mode']})"
    )
    print(
        "Resumen cualitativo estructurado: "
        f"{system_summary_json_path}"
    )
    print(
        "Resumen cualitativo Markdown: "
        f"{system_summary_markdown_path}"
    )


def main() -> int:
    for run_id, run_config in RUNS:
        run_manifest_path = (
            RUNS_DIR / f"{run_id}.manifest.json"
        )
        run_results_path = (
            RUNS_DIR / f"{run_id}.json"
        )

        if (
            not run_manifest_path.exists()
            and not run_results_path.exists()
        ):
            start_run(
                run_id=run_id,
                run_config=run_config,
                progress_callback=print_progress,
            )
        else:
            resume_run(
                run_id=run_id,
                progress_callback=print_progress,
            )

    for eval_id, run_ids in EVALUATIONS:
        _run_evaluation(
            eval_id,
            run_ids,
        )

    _run_qualitative_evaluation()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())