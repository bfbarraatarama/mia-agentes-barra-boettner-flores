"""Runner mínimo de evaluación para M3."""

from __future__ import annotations
from collections.abc import Callable

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

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
from eval.configs.agent_configs import AGENT_CONFIGS
from eval.configs.trial_configs import TRIAL_CONFIGS
from eval.configs.llm_configs import LLM_CONFIGS, build_llm_client


SCENARIOS_DIR = REPO_ROOT / "scenarios"


def _serialize_trace_event(
    event: dict[str, Any],
) -> dict[str, Any]:
    """Convierte un evento de traza a estructuras serializables."""

    serialized = dict(event)

    response = serialized.get("response")
    if response is not None:
        serialized["response"] = asdict(response)

    error = serialized.get("error")
    if error is not None:
        serialized["error"] = {
            "type": type(error).__name__,
            "message": str(error),
        }

    return serialized


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

def run_trial(
    scenario_spec: str,
    agent_config: dict[str, Any],
    llm_config: dict[str, Any],
    trial_config: dict[str, Any],
    trial_index: int,
) -> dict[str, Any]:
    """Ejecuta un trial independiente sobre un escenario."""

    scenario = _resolve_scenario(scenario_spec)
    world = scenario.initial_world
    trace_events: list[dict[str, Any]] = []

    llm_client = build_llm_client(llm_config)

    agent_build_config = dict(agent_config)
    agent_build_config["llm_client"] = llm_client
    agent_build_config["trace_callback"] = lambda event: trace_events.append(
        _serialize_trace_event(event)
    )

    agent = build_agent(agent_build_config)

    for tool, schema in make_world_tools(world):
        agent.register_tool(tool, schema)

    attempts = []
    user_message = scenario.user_message

    for attempt_index in range(
        1,
        trial_config["max_attempts"] + 1,
    ):
        trace_start = len(trace_events)
        result = agent.run(user_message)
        trace = trace_events[trace_start:]

        achieved, reason = check_goal(world, scenario.goal)

        attempts.append({
            "attempt_index": attempt_index,
            "user_message": user_message,
            "goal_achieved": achieved,
            "goal_reason": reason,
            "agent_result": asdict(result),
            "trace": trace,
        })

        if achieved or result.error is not None:
            break

        user_message = trial_config["continuation_message"]

    final_attempt = attempts[-1]

    return {
        "trial_index": trial_index,
        "goal_achieved": final_attempt["goal_achieved"],
        "goal_reason": final_attempt["goal_reason"],
        "attempts": attempts,
    }


def run_case(
    scenario_spec: str,
    agent_config_name: str,
    llm_config_name: str,
    agent_config: dict[str, Any],
    llm_config: dict[str, Any],
    trial_config: dict[str, Any],
    trial_indices: list[int],
    trial_callback: Callable[[dict[str, Any]], None] | None = None,
):
    trials = []
    scenario_metadata = _resolve_scenario(scenario_spec)

    for trial_index in trial_indices:
        trial = run_trial(
            scenario_spec=scenario_spec,
            agent_config=agent_config,
            llm_config=llm_config,
            trial_config=trial_config,
            trial_index=trial_index,
        )

        trials.append(trial)

        if trial_callback is not None:
            trial_callback(trial)

    output = {
        "agent_config": agent_config_name,
        "llm_config": llm_config_name,
        "trial_config": dict(trial_config),
        "scenario": scenario_metadata.id,
        "difficulty": scenario_metadata.difficulty,
        "goal": scenario_metadata.goal,
        "requested_trial_indices": list(trial_indices),
        "trials": trials,
    }
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Ejecuta un caso individual de M3."
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
        "--trial-config",
        choices=sorted(TRIAL_CONFIGS),
        default="single_attempt",
        help="Configuración de trial a utilizar.",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=1,
        help="Número de trials independientes del caso.",
    )
    args = parser.parse_args(argv)

    if args.trials < 1:
        parser.error("--trials debe ser al menos 1.")

    output = run_case(
        scenario_spec=args.scenario,
        agent_config_name=args.agent_config,
        llm_config_name=args.llm_config,
        agent_config=AGENT_CONFIGS[args.agent_config],
        llm_config=LLM_CONFIGS[args.llm_config],
        trial_config=TRIAL_CONFIGS[args.trial_config],
        trial_indices=list(range(1, args.trials + 1)),
    )

    print(json.dumps(output, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())