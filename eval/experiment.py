"""Runner mínimo de evaluación para M3."""

from __future__ import annotations
from collections.abc import Callable

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

# Permite ejecutar exactamente:
#     python eval/experiment.py
REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from mia_world import (
    Scenario,
    check_goal,
    list_scenarios,
    load_scenario,
    make_world_tools,
)
from student_framework import build_agent
from eval.agent_configs import AGENT_CONFIGS
from eval.llm_configs import LLM_CONFIGS, build_llm_client


SCENARIOS_DIR = REPO_ROOT / "scenarios"


def _resolve_scenario(spec: str) -> Scenario:
    """Resuelve un escenario por path, id o dificultad."""

    path = Path(spec)

    if path.is_file():
        return load_scenario(path)

    available = list_scenarios(SCENARIOS_DIR)

    by_id = {
        scenario.id: scenario
        for scenario in available
    }

    if spec in by_id:
        return by_id[spec]

    by_difficulty = [
        scenario
        for scenario in available
        if scenario.difficulty == spec
    ]

    if by_difficulty:
        return by_difficulty[0]

    options = ", ".join(
        sorted(scenario.id for scenario in available)
    ) or "(ninguno)"

    raise SystemExit(
        f"No se encontró el escenario {spec!r}. "
        f"Disponibles: {options}."
    )


def run_experiment(
    scenario_spec: str,
    agent_config_name: str,
    llm_config_name: str,
    runs_count: int,
    progress_callback: Callable[[int, int, bool], None] | None = None,
):
    
    runs = []
    scenario_metadata = _resolve_scenario(scenario_spec)

    for run_index in range(1, runs_count + 1):
        scenario = _resolve_scenario(scenario_spec)
        world = scenario.initial_world

        llm_client = build_llm_client(llm_config_name)

        agent_config = dict(AGENT_CONFIGS[agent_config_name])
        agent_config["llm_client"] = llm_client

        agent = build_agent(agent_config)

        for tool, schema in make_world_tools(world):
            agent.register_tool(tool, schema)

        result = agent.run(scenario.user_message)
        achieved, reason = check_goal(world, scenario.goal)

        runs.append({
            "run_index": run_index,
            "goal_achieved": achieved,
            "goal_reason": reason,
            "agent_result": asdict(result),
        })

        if progress_callback is not None:
            progress_callback(run_index, runs_count, achieved)

    output = {
        "agent_config": agent_config_name,
        "llm_config": llm_config_name,
        "scenario": scenario_metadata.id,
        "difficulty": scenario_metadata.difficulty,
        "goal": scenario_metadata.goal,
        "requested_runs": runs_count,
        "runs": runs,
    }

    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Ejecuta una evaluación individual de M3."
    )
    parser.add_argument(
        "--scenario",
        default="easy",
        help="Escenario a ejecutar: path, id o dificultad.",
    )
    parser.add_argument(
        "--agent-config",
        choices=sorted(AGENT_CONFIGS),
        default="minimal",
        help="Configuración del agente a evaluar.",
    )
    parser.add_argument(
        "--llm-config",
        choices=sorted(LLM_CONFIGS),
        default="llama3.1",
        help="Configuración del LLM a utilizar.",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Número de repeticiones independientes del experimento.",
    )

    args = parser.parse_args(argv)

    if args.runs < 1:
        parser.error("--runs debe ser al menos 1.")

    output = run_experiment(
        scenario_spec=args.scenario,
        agent_config_name=args.agent_config,
        llm_config_name=args.llm_config,
        runs_count=args.runs,
    )

    print(json.dumps(output, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())