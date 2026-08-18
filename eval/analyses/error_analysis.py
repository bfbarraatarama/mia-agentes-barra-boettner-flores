"""Análisis de errores sobre evidencia persistida de M3.

Lee los artefactos de un run persistido y clasifica cada trial fallido.
Genera un .md con el 100% de los trials fallidos.

Cada trial se clasifica usando su último attempt.

Taxonomía de modos de fallo:
    context_overflow   — se quedó sin ventana de historial (max_history_messages)
    max_iterations     — agotó el presupuesto de pasos
    hallucination      — narra acciones como texto en vez de llamar herramientas
    wrong_tool_use     — llamó una herramienta con args inválidos o inexistentes
    gave_up_early      — terminó voluntariamente sin alcanzar el objetivo
    planning_order     — rompió el orden de un goal sequence
    navigation_error   — se perdió en escenarios multi-sala sin usar go
    planning_failure   — exploró correctamente pero no llegó al objetivo

Uso:
    python eval/error_analysis.py --run-id <run_id>
    python eval/error_analysis.py \
        --run-id <run_id> \
        --output <ruta.md>
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = REPO_ROOT / "eval" / "results" / "runs"

MULTI_ROOM_SCENARIOS = {
    "apartment-keys",
    "office-sequence",
    "vault-combination",
    "backtracking-vault",
}

SEQUENCE_GOAL_SCENARIOS = {"office-sequence"}

# Frases que indican que el modelo narró una tool call en texto en vez de llamarla
_HALLUCINATION_MARKERS = [
    '"name":',
    '"parameters":',
    '{"name"',
]

# Frases que indican que el modelo creyó haber ganado cuando no
_FALSE_SUCCESS_MARKERS = [
    "abrí la puerta",
    "abri la puerta",
    "puerta abierta",
    "salí del",
    "sali del",
    "objetivo cumplido",
    "tarea completada",
    "logré salir",
    "logre salir",
]


def classify_trial(trial: dict, scenario: str) -> tuple[str, str]:
    """Clasifica un trial fallido. Devuelve (modo, razón breve)."""

    answer = trial["agent_result"].get("answer") or ""
    answer_lower = answer.lower()
    agent_error = trial["agent_result"].get("error") or ""
    steps = trial["agent_result"].get("steps") or []
    goal_reason = trial.get("goal_reason", "")

    # 1. context_overflow
    if "max_history_messages" in agent_error or "max_history_messages" in answer:
        return "context_overflow", "ventana de historial agotada"

    # 2. max_iterations
    if "límite de" in answer and "iteraciones" in answer:
        return "max_iterations", "presupuesto de pasos agotado"

    # 3. planning_order — solo en escenarios con goal sequence
    if scenario in SEQUENCE_GOAL_SCENARIOS and "orden" in goal_reason.lower():
        return "planning_order", "condiciones cumplidas en orden incorrecto"

    # 4. hallucination — el modelo escribe JSON de tool call en texto libre
    if any(marker in answer for marker in _HALLUCINATION_MARKERS):
        return "hallucination", "narró tool calls como texto en vez de ejecutarlas"

    # 5. false success — el modelo creyó ganar pero no ganó
    if any(marker in answer_lower for marker in _FALSE_SUCCESS_MARKERS):
        return "hallucination", "declaró éxito cuando el objetivo no estaba cumplido"

    # 6. wrong_tool_use — algún step devolvió error de herramienta
    has_tool_error = any(s.get("error") for s in steps)
    if has_tool_error:
        first_error = next(s["error"] for s in steps if s.get("error"))
        return "wrong_tool_use", first_error[:120]

    n_steps = len(steps)

    # 7. gave_up_early — muy pocos pasos sin error
    if n_steps <= 4:
        return "gave_up_early", f"terminó voluntariamente en {n_steps} pasos"

    # 8. navigation_error — multi-sala sin usar go
    if scenario in MULTI_ROOM_SCENARIOS:
        used_go = any(s.get("tool_name") == "go" for s in steps)
        if not used_go:
            return "navigation_error", "no usó go en escenario multi-sala"

    # 9. planning_failure — catch-all
    return "planning_failure", f"exploró {n_steps} pasos sin alcanzar el objetivo"


def analyze_errors(
    run_manifest: dict,
    run_result: dict,
) -> dict:
    """Analiza todos los trials fallidos de un run."""

    run_id = run_manifest["run_id"]

    total = 0
    successes = 0
    classified_failures: list[dict] = []

    failures_by_mode: dict[str, int] = defaultdict(int)
    failures_by_model: dict[str, dict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    failures_by_system: dict[
        str,
        dict[str, dict[str, int]],
    ] = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(int)
        )
    )
    failures_by_scenario: dict[str, dict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    examples_by_mode: dict[str, list[dict]] = defaultdict(list)

    scenario_metadata = run_manifest["scenario_metadata"]

    for result in run_result["results"]:
        agent_config = result["agent_config"]
        model = result["llm_config"]
        scenario = result["scenario"]
        difficulty = scenario_metadata[scenario]["difficulty"]

        for trial in result["trials"]:
            total += 1

            if trial["goal_achieved"]:
                successes += 1
                continue

            final_attempt = trial["attempts"][-1]

            trial_for_classify = {
                "agent_result": final_attempt["agent_result"],
                "goal_reason": (
                    final_attempt.get("goal_reason", "")
                    or trial.get("goal_reason", "")
                ),
            }

            mode, reason = classify_trial(
                trial_for_classify,
                scenario,
            )

            steps = final_attempt["agent_result"].get("steps") or []

            failures_by_mode[mode] += 1
            failures_by_model[model][mode] += 1
            failures_by_system[agent_config][model][mode] += 1
            failures_by_scenario[scenario][mode] += 1

            failure_record = {
                "agent_config": agent_config,
                "model": model,
                "scenario": scenario,
                "difficulty": difficulty,
                "trial_index": trial["trial_index"],
                "n_attempts": len(trial["attempts"]),
                "mode": mode,
                "reason": reason,
                "goal_reason": trial_for_classify["goal_reason"],
                "n_steps": len(steps),
                "answer_preview": (
                    final_attempt["agent_result"].get("answer") or ""
                )[:200].strip(),
                "agent_error": final_attempt["agent_result"].get("error"),
            }

            classified_failures.append(failure_record)

            if len(examples_by_mode[mode]) < 2:
                examples_by_mode[mode].append(failure_record)

    failures = total - successes

    return {
        "run_id": run_id,
        "total_trials": total,
        "successes": successes,
        "failures": failures,
        "success_rate": round(successes / total, 3) if total else 0,
        "coverage": (
            f"{len(classified_failures)}/{failures} "
            "trials fallidos clasificados"
        ),
        "failures_by_mode": dict(
            sorted(
                failures_by_mode.items(),
                key=lambda item: -item[1],
            )
        ),
        "failures_by_model": {
            model: dict(
                sorted(
                    modes.items(),
                    key=lambda item: -item[1],
                )
            )
            for model, modes in failures_by_model.items()
        },
        "failures_by_system": {
            agent_config: {
                model: dict(
                    sorted(
                        modes.items(),
                        key=lambda item: -item[1],
                    )
                )
                for model, modes in models.items()
            }
            for agent_config, models in failures_by_system.items()
        },
        "failures_by_scenario": {
            scenario: dict(
                sorted(
                    modes.items(),
                    key=lambda item: -item[1],
                )
            )
            for scenario, modes in failures_by_scenario.items()
        },
        "examples_by_mode": dict(examples_by_mode),
        "all_failures": classified_failures,
    }


def print_report(analysis: dict) -> None:
    total = analysis["total_trials"]
    failures = analysis["failures"]
    successes = analysis["successes"]

    print("=" * 62)
    print("ANÁLISIS DE ERRORES — M3")
    print("=" * 62)
    print(f"\nRun: {analysis['run_id']}")
    print(f"\nTotal trials: {total}")
    print(f"Exitosos:     {successes}  ({100 * successes // total}%)")
    print(f"Fallidos:     {failures}  ({100 * failures // total}%)")
    print(f"Cobertura:    {analysis['coverage']}")

    print("\n── MODOS DE FALLO ──────────────────────────────────────")
    for mode, count in analysis["failures_by_mode"].items():
        pct = round(100 * count / failures)
        bar = "█" * count
        print(f"  {mode:<20} {count:>3}  ({pct:>2}%)  {bar}")

    print("\n── POR SISTEMA ─────────────────────────────────────────")
    for agent_config, models in analysis["failures_by_system"].items():
        for model, modes in models.items():
            total_system = sum(modes.values())
            print(
                f"\n  {agent_config} / {model}  "
                f"({total_system} fallos)"
            )
            for mode, count in modes.items():
                print(f"    {mode:<20} {count}")

    print("\n── POR MODELO ──────────────────────────────────────────")
    for model, modes in analysis["failures_by_model"].items():
        total_model = sum(modes.values())
        print(f"\n  {model}  ({total_model} fallos)")
        for mode, count in modes.items():
            print(f"    {mode:<20} {count}")

    print("\n── POR ESCENARIO ───────────────────────────────────────")
    for scenario, modes in analysis["failures_by_scenario"].items():
        total_sc = sum(modes.values())
        modes_str = ", ".join(
            f"{m}:{c}" for m, c in modes.items()
        )
        print(f"  {scenario:<32} {total_sc} fallos  [{modes_str}]")

    print("\n── EJEMPLOS POR MODO ───────────────────────────────────")
    for mode, examples in analysis["examples_by_mode"].items():
        print(f"\n  [{mode}]")
        for ex in examples:
            print(
                f"    {ex['agent_config']} / {ex['model']} / "
                f"{ex['scenario']} / trial {ex['trial_index']}  "
                f"({ex['n_steps']} pasos)"
            )
            print(f"    razón: {ex['reason']}")
            if ex["answer_preview"]:
                print(f"    answer: {ex['answer_preview'][:130]}")


def render_markdown(analysis: dict) -> str:
    lines = []
    total = analysis["total_trials"]
    failures = analysis["failures"]
    successes = analysis["successes"]

    lines.append("# Análisis de errores — M3\n")
    lines.append(f"**Run:** `{analysis['run_id']}`\n")
    lines.append(f"| | |")
    lines.append(f"|---|---|")
    lines.append(f"| Total trials | {total} |")
    lines.append(f"| Exitosos | {successes} ({100 * successes // total}%) |")
    lines.append(f"| Fallidos | {failures} ({100 * failures // total}%) |")
    lines.append(f"| Cobertura | {analysis['coverage']} |")
    lines.append("")

    lines.append("## Modos de fallo\n")
    lines.append("| Modo | Runs | % |")
    lines.append("|---|---:|---:|")
    for mode, count in analysis["failures_by_mode"].items():
        pct = round(100 * count / failures)
        lines.append(f"| `{mode}` | {count} | {pct}% |")
    lines.append("")

    lines.append("## Por sistema\n")
    for agent_config, models in analysis["failures_by_system"].items():
        for model, modes in models.items():
            total_system = sum(modes.values())
            lines.append(
                f"### {agent_config} / {model} "
                f"({total_system} fallos)\n"
            )
            lines.append("| Modo | Runs |")
            lines.append("|---|---:|")
            for mode, count in modes.items():
                lines.append(f"| `{mode}` | {count} |")
            lines.append("")

    lines.append("## Por modelo\n")
    for model, modes in analysis["failures_by_model"].items():
        total_model = sum(modes.values())
        lines.append(f"### {model} ({total_model} fallos)\n")
        lines.append("| Modo | Runs |")
        lines.append("|---|---:|")
        for mode, count in modes.items():
            lines.append(f"| `{mode}` | {count} |")
        lines.append("")

    lines.append("## Por escenario\n")
    lines.append("| Escenario | Dificultad | Fallos | Distribución |")
    lines.append("|---|---|---:|---|")
    difficulties = {
        r["scenario"]: r["difficulty"]
        for r in analysis["all_failures"]
    }
    for scenario, modes in analysis["failures_by_scenario"].items():
        total_sc = sum(modes.values())
        dist = ", ".join(f"`{m}`: {c}" for m, c in modes.items())
        diff = difficulties.get(scenario, "")
        lines.append(f"| {scenario} | {diff} | {total_sc} | {dist} |")
    lines.append("")

    lines.append("## Ejemplos por modo\n")
    for mode, examples in analysis["examples_by_mode"].items():
        lines.append(f"### `{mode}`\n")
        for ex in examples:
            lines.append(
                f"**{ex['agent_config']} / {ex['model']} / "
                f"{ex['scenario']} / trial {ex['trial_index']}** "
                f"({ex['n_steps']} pasos)"
            )
            lines.append(f"- Razón: {ex['reason']}")
            if ex["answer_preview"]:
                preview = ex["answer_preview"][:200].replace("\n", " ")
                lines.append(f"- Respuesta: *{preview}*")
            lines.append("")

    lines.append("## Todos los fallos clasificados\n")
    lines.append(
        "| Trial | Configuración de agente | Modelo | "
        "Escenario | Pasos | Modo | Razón |"
    )
    lines.append("|---|---|---|---|---:|---|---|")
    for f in analysis["all_failures"]:
        reason = f["reason"][:60].replace("|", "\\|")
        lines.append(
            f"| {f['trial_index']} | {f['agent_config']} | "
            f"{f['model']} | {f['scenario']} | {f['n_steps']} | "
            f"`{f['mode']}` | {reason} |"
        )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Análisis de errores de un run M3."
    )
    parser.add_argument(
        "--run-id",
        required=True,
        help="run_id cuya evidencia se analizará.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Ruta opcional donde guardar el Markdown. "
            "Si se omite, solo se imprime el análisis."
        ),
    )
    args = parser.parse_args()

    manifest_path = RUNS_DIR / f"{args.run_id}.manifest.json"
    results_path = RUNS_DIR / f"{args.run_id}.json"

    if not manifest_path.exists():
        raise SystemExit(
            f"No se encontró el manifest del run: {manifest_path}"
        )

    if not results_path.exists():
        raise SystemExit(
            f"No se encontraron los resultados del run: {results_path}"
        )

    with open(manifest_path, encoding="utf-8") as f:
        run_manifest = json.load(f)

    with open(results_path, encoding="utf-8") as f:
        run_result = json.load(f)

    analysis = analyze_errors(
        run_manifest,
        run_result,
    )
    print_report(analysis)

    if args.output is not None:
        args.output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(render_markdown(analysis))

        print(
            f"\nArtefacto guardado en: {args.output}"
        )


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    main()