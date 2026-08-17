"""Análisis de errores sobre resultados de evaluación M3.

Lee un archivo evaluation.json (o cualquier archivo del mismo formato) y
clasifica cada corrida fallida. Genera un .md con el 100% de los runs fallidos.

Compatible con ambas estructuras de resultados:
  - Estructura antigua: result["runs"]   (un agente por run)
  - Estructura nueva:   result["trials"] (un trial con varios attempts)
    En este caso se clasifica usando el último attempt de cada trial.

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
    python eval/error_analysis.py
    python eval/error_analysis.py --results eval/results/evaluation.json
    python eval/error_analysis.py --no-save   (solo imprime, no guarda .md)
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = REPO_ROOT / "eval" / "results" / "evaluation.json"
DEFAULT_OUTPUT = REPO_ROOT / "eval" / "results" / "error_analysis.md"

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


def classify_run(run: dict, scenario: str) -> tuple[str, str]:
    """Clasifica un run fallido. Devuelve (modo, razón breve)."""

    answer = run["agent_result"].get("answer") or ""
    answer_lower = answer.lower()
    agent_error = run["agent_result"].get("error") or ""
    steps = run["agent_result"].get("steps") or []
    goal_reason = run.get("goal_reason", "")

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


def analyze(results_path: Path) -> dict:
    with open(results_path, encoding="utf-8") as f:
        data = json.load(f)

    total = 0
    successes = 0
    classified_failures: list[dict] = []

    failures_by_mode: dict[str, int] = defaultdict(int)
    failures_by_model: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    failures_by_scenario: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    examples_by_mode: dict[str, list[dict]] = defaultdict(list)

    for result in data["results"]:
        model = result["llm_config"]
        scenario = result["scenario"]
        difficulty = result["difficulty"]

        # Soporta estructura antigua (runs) y nueva (trials/attempts)
        if "runs" in result:
            items = [
                {
                    "index": r["run_index"],
                    "goal_achieved": r["goal_achieved"],
                    "agent_result": r["agent_result"],
                    "goal_reason": r.get("goal_reason", ""),
                    "n_attempts": 1,
                }
                for r in result["runs"]
            ]
        else:
            items = [
                {
                    "index": t["trial_index"],
                    "goal_achieved": t["goal_achieved"],
                    "agent_result": t["attempts"][-1]["agent_result"],
                    "goal_reason": t["attempts"][-1].get("goal_reason", "") or t.get("goal_reason", ""),
                    "n_attempts": len(t["attempts"]),
                }
                for t in result["trials"]
            ]

        for item in items:
            total += 1
            if item["goal_achieved"]:
                successes += 1
                continue

            run_for_classify = {
                "agent_result": item["agent_result"],
                "goal_reason": item["goal_reason"],
            }
            mode, reason = classify_run(run_for_classify, scenario)
            steps = item["agent_result"].get("steps") or []

            failures_by_mode[mode] += 1
            failures_by_model[model][mode] += 1
            failures_by_scenario[scenario][mode] += 1

            failure_record = {
                "model": model,
                "scenario": scenario,
                "difficulty": difficulty,
                "run_index": item["index"],
                "n_attempts": item["n_attempts"],
                "mode": mode,
                "reason": reason,
                "goal_reason": item["goal_reason"],
                "n_steps": len(steps),
                "answer_preview": (item["agent_result"].get("answer") or "")[:200].strip(),
                "agent_error": item["agent_result"].get("error"),
            }
            classified_failures.append(failure_record)

            if len(examples_by_mode[mode]) < 2:
                examples_by_mode[mode].append(failure_record)

    failures = total - successes

    return {
        "baseline": str(results_path),
        "total_runs": total,
        "successes": successes,
        "failures": failures,
        "success_rate": round(successes / total, 3) if total else 0,
        "coverage": f"{len(classified_failures)}/{failures} runs fallidos clasificados",
        "failures_by_mode": dict(
            sorted(failures_by_mode.items(), key=lambda x: -x[1])
        ),
        "failures_by_model": {
            m: dict(sorted(v.items(), key=lambda x: -x[1]))
            for m, v in failures_by_model.items()
        },
        "failures_by_scenario": {
            s: dict(sorted(v.items(), key=lambda x: -x[1]))
            for s, v in failures_by_scenario.items()
        },
        "examples_by_mode": dict(examples_by_mode),
        "all_failures": classified_failures,
    }


def print_report(analysis: dict) -> None:
    total = analysis["total_runs"]
    failures = analysis["failures"]
    successes = analysis["successes"]

    print("=" * 62)
    print("ANÁLISIS DE ERRORES — BASELINE M3")
    print("=" * 62)
    print(f"\nTotal runs:   {total}")
    print(f"Exitosos:     {successes}  ({100 * successes // total}%)")
    print(f"Fallidos:     {failures}  ({100 * failures // total}%)")
    print(f"Cobertura:    {analysis['coverage']}")

    print("\n── MODOS DE FALLO ──────────────────────────────────────")
    for mode, count in analysis["failures_by_mode"].items():
        pct = round(100 * count / failures)
        bar = "█" * count
        print(f"  {mode:<20} {count:>3}  ({pct:>2}%)  {bar}")

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
            print(f"    {ex['model']} / {ex['scenario']} / run {ex['run_index']}  ({ex['n_steps']} pasos)")
            print(f"    razón: {ex['reason']}")
            if ex["answer_preview"]:
                print(f"    answer: {ex['answer_preview'][:130]}")


def render_markdown(analysis: dict) -> str:
    lines = []
    total = analysis["total_runs"]
    failures = analysis["failures"]
    successes = analysis["successes"]

    lines.append("# Análisis de errores — Baseline M3\n")
    lines.append(f"**Fuente:** `{analysis['baseline']}`\n")
    lines.append(f"| | |")
    lines.append(f"|---|---|")
    lines.append(f"| Total runs | {total} |")
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
            lines.append(f"**{ex['model']} / {ex['scenario']} / run {ex['run_index']}** ({ex['n_steps']} pasos)")
            lines.append(f"- Razón: {ex['reason']}")
            if ex["answer_preview"]:
                preview = ex["answer_preview"][:200].replace("\n", " ")
                lines.append(f"- Respuesta: *{preview}*")
            lines.append("")

    lines.append("## Todos los fallos clasificados\n")
    lines.append("| Run | Modelo | Escenario | Pasos | Modo | Razón |")
    lines.append("|---|---|---|---:|---|---|")
    for f in analysis["all_failures"]:
        reason = f["reason"][:60].replace("|", "\\|")
        lines.append(
            f"| {f['run_index']} | {f['model']} | {f['scenario']} "
            f"| {f['n_steps']} | `{f['mode']}` | {reason} |"
        )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Análisis de errores del baseline M3.")
    parser.add_argument(
        "--results",
        type=Path,
        default=DEFAULT_RESULTS,
        help="Ruta al evaluation.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Ruta de salida del .md de análisis",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Solo imprime en consola, no guarda el .md",
    )
    args = parser.parse_args()

    if not args.results.exists():
        raise SystemExit(f"No se encontró el archivo: {args.results}")

    analysis = analyze(args.results)
    print_report(analysis)

    if not args.no_save:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(render_markdown(analysis))
        print(f"\nArtefacto guardado en: {args.output}")


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
