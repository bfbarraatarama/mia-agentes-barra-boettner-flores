"""Evaluación reproducible de M3."""

from __future__ import annotations

import sys
from pathlib import Path

# Permite ejecutar exactamente:
#     python eval/run.py
REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from eval.evaluation import run_evaluation
from eval.evaluation_configs import M3_EVALUATION
from eval.report import (
    plot_success_rate,
    print_success_rate_summary,
    save_evaluation_result,
)


RESULTS_DIR = REPO_ROOT / "eval" / "results"
RESULTS_PATH = RESULTS_DIR / "evaluation.json"
SUCCESS_RATE_PLOT_PATH = RESULTS_DIR / "success_rate.png"


def print_progress(
    completed_runs: int,
    total_runs: int,
    agent_config: str,
    llm_config: str,
    scenario: str,
    run_index: int,
    runs_count: int,
    achieved: bool,
) -> None:
    """Muestra el progreso de la evaluación."""

    percentage = 100 * completed_runs / total_runs
    status = "SUCCESS" if achieved else "FAIL"

    print(
        f"[{completed_runs}/{total_runs} | {percentage:5.1f}%] "
        f"[{status}] "
        f"{agent_config} / {llm_config} / {scenario} "
        f"(run {run_index}/{runs_count})",
        flush=True,
    )

def main() -> int:
    result = run_evaluation(
        M3_EVALUATION,
        progress_callback=print_progress,
    )

    save_evaluation_result(
        result,
        RESULTS_PATH,
    )

    print_success_rate_summary(result)

    plot_success_rate(
        result,
        SUCCESS_RATE_PLOT_PATH,
    )

    print()
    print(f"Resultados completos: {RESULTS_PATH}")
    print(f"Gráfico de success rate: {SUCCESS_RATE_PLOT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())