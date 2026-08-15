import json

import pytest

from mia_agents.testing import MockLLMClient
from mia_agents.types import LLMResponse, ToolCall
from mia_world import Item, Room, Scenario, World

from eval import experiment
from eval.experiment_configs import CONTINUATION_MESSAGE


def test_run_trial_continues_after_incomplete_final_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Un trial continúa sobre el mismo agente cuando el goal sigue incompleto."""

    scenario = Scenario(
        id="test-trial-continuation",
        description="Escenario controlado para probar la continuación.",
        user_message="Tomá la llave.",
        initial_world=World(
            rooms={
                "sala": Room(
                    id="sala",
                    name="Sala",
                    description="Una sala con una llave.",
                    items=["llave"],
                ),
            },
            items={
                "llave": Item(
                    id="llave",
                    name="Llave",
                    description="Una llave.",
                    takeable=True,
                ),
            },
            current_room="sala",
        ),
        goal={
            "type": "item_in_inventory",
            "item": "llave",
        },
        difficulty="test",
    )

    mock = MockLLMClient([
        LLMResponse(content="Listo."),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name="take",
                    arguments=json.dumps({"item": "llave"}),
                ),
            ],
        ),
        LLMResponse(content="Ahora sí."),
    ])

    monkeypatch.setattr(
        experiment,
        "_resolve_scenario",
        lambda spec: scenario,
    )
    monkeypatch.setattr(
        experiment,
        "build_llm_client",
        lambda name: mock,
    )

    trial = experiment.run_trial(
        scenario_spec="test-trial-continuation",
        agent_config_name="minimal",
        llm_config_name="llama3.1",
        experiment_config={
            "max_attempts": 2,
            "continuation_message": CONTINUATION_MESSAGE,
        },
        trial_index=1,
    )

    assert trial["trial_index"] == 1
    assert trial["goal_achieved"] is True
    assert len(trial["attempts"]) == 2

    assert trial["attempts"][0]["user_message"] == "Tomá la llave."
    assert trial["attempts"][0]["goal_achieved"] is False

    assert trial["attempts"][1]["user_message"] == CONTINUATION_MESSAGE
    assert trial["attempts"][1]["goal_achieved"] is True

    assert mock.call_count == 3
    assert mock.calls[1]["messages"] == [
        {
            "role": "user",
            "content": "Tomá la llave.",
        },
        {
            "role": "assistant",
            "content": "Listo.",
        },
        {
            "role": "user",
            "content": CONTINUATION_MESSAGE,
        },
    ]


def test_run_trial_stops_when_max_attempts_is_reached(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Un trial no continúa cuando alcanza max_attempts."""

    scenario = Scenario(
        id="test-max-attempts",
        description="Escenario controlado para probar max_attempts.",
        user_message="Tomá la llave.",
        initial_world=World(
            rooms={
                "sala": Room(
                    id="sala",
                    name="Sala",
                    description="Una sala con una llave.",
                    items=["llave"],
                ),
            },
            items={
                "llave": Item(
                    id="llave",
                    name="Llave",
                    description="Una llave.",
                    takeable=True,
                ),
            },
            current_room="sala",
        ),
        goal={
            "type": "item_in_inventory",
            "item": "llave",
        },
        difficulty="test",
    )

    mock = MockLLMClient([
        LLMResponse(content="Listo."),
    ])

    monkeypatch.setattr(
        experiment,
        "_resolve_scenario",
        lambda spec: scenario,
    )
    monkeypatch.setattr(
        experiment,
        "build_llm_client",
        lambda name: mock,
    )

    trial = experiment.run_trial(
        scenario_spec="test-max-attempts",
        agent_config_name="minimal",
        llm_config_name="llama3.1",
        experiment_config={
            "max_attempts": 1,
            "continuation_message": CONTINUATION_MESSAGE,
        },
        trial_index=1,
    )

    assert trial["goal_achieved"] is False
    assert len(trial["attempts"]) == 1
    assert mock.call_count == 1

    assert trial["attempts"][0]["user_message"] == "Tomá la llave."
    assert trial["attempts"][0]["goal_achieved"] is False


def test_run_trial_stops_after_run_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Un trial no continúa cuando run termina con error."""

    scenario = Scenario(
        id="test-run-error",
        description="Escenario controlado para probar errores de run.",
        user_message="Tomá la llave.",
        initial_world=World(
            rooms={
                "sala": Room(
                    id="sala",
                    name="Sala",
                    description="Una sala con una llave.",
                    items=["llave"],
                ),
            },
            items={
                "llave": Item(
                    id="llave",
                    name="Llave",
                    description="Una llave.",
                    takeable=True,
                ),
            },
            current_room="sala",
        ),
        goal={
            "type": "item_in_inventory",
            "item": "llave",
        },
        difficulty="test",
    )

    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name="look",
                    arguments=json.dumps({}),
                ),
            ],
        ),
    ])

    agent_config = dict(experiment.AGENT_CONFIGS["minimal"])
    agent_config["max_iterations"] = 1

    monkeypatch.setitem(
        experiment.AGENT_CONFIGS,
        "minimal",
        agent_config,
    )
    monkeypatch.setattr(
        experiment,
        "_resolve_scenario",
        lambda spec: scenario,
    )
    monkeypatch.setattr(
        experiment,
        "build_llm_client",
        lambda name: mock,
    )

    trial = experiment.run_trial(
        scenario_spec="test-run-error",
        agent_config_name="minimal",
        llm_config_name="llama3.1",
        experiment_config={
            "max_attempts": 2,
            "continuation_message": CONTINUATION_MESSAGE,
        },
        trial_index=1,
    )

    assert trial["goal_achieved"] is False
    assert len(trial["attempts"]) == 1
    assert mock.call_count == 1

    assert trial["attempts"][0]["goal_achieved"] is False
    assert trial["attempts"][0]["agent_result"]["error"] is not None


def test_run_trial_succeeds_when_goal_is_reached_despite_run_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Un trial es exitoso si alcanza el goal aunque run termine con error."""

    scenario = Scenario(
        id="test-goal-before-run-error",
        description="Escenario controlado para probar goal y error.",
        user_message="Tomá la llave.",
        initial_world=World(
            rooms={
                "sala": Room(
                    id="sala",
                    name="Sala",
                    description="Una sala con una llave.",
                    items=["llave"],
                ),
            },
            items={
                "llave": Item(
                    id="llave",
                    name="Llave",
                    description="Una llave.",
                    takeable=True,
                ),
            },
            current_room="sala",
        ),
        goal={
            "type": "item_in_inventory",
            "item": "llave",
        },
        difficulty="test",
    )

    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name="take",
                    arguments=json.dumps({"item": "llave"}),
                ),
            ],
        ),
    ])

    agent_config = dict(experiment.AGENT_CONFIGS["minimal"])
    agent_config["max_iterations"] = 1

    monkeypatch.setitem(
        experiment.AGENT_CONFIGS,
        "minimal",
        agent_config,
    )
    monkeypatch.setattr(
        experiment,
        "_resolve_scenario",
        lambda spec: scenario,
    )
    monkeypatch.setattr(
        experiment,
        "build_llm_client",
        lambda name: mock,
    )

    trial = experiment.run_trial(
        scenario_spec="test-goal-before-run-error",
        agent_config_name="minimal",
        llm_config_name="llama3.1",
        experiment_config={
            "max_attempts": 2,
            "continuation_message": CONTINUATION_MESSAGE,
        },
        trial_index=1,
    )

    assert trial["goal_achieved"] is True
    assert len(trial["attempts"]) == 1
    assert mock.call_count == 1

    assert trial["attempts"][0]["goal_achieved"] is True
    assert trial["attempts"][0]["agent_result"]["error"] is not None


def test_run_experiment_uses_independent_trials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cada trial de un experimento usa un World y un agente independientes."""

    def make_scenario() -> Scenario:
        return Scenario(
            id="test-independent-trials",
            description="Escenario controlado para probar trials independientes.",
            user_message="Tomá la llave.",
            initial_world=World(
                rooms={
                    "sala": Room(
                        id="sala",
                        name="Sala",
                        description="Una sala con una llave.",
                        items=["llave"],
                    ),
                },
                items={
                    "llave": Item(
                        id="llave",
                        name="Llave",
                        description="Una llave.",
                        takeable=True,
                    ),
                },
                current_room="sala",
            ),
            goal={
                "type": "item_in_inventory",
                "item": "llave",
            },
            difficulty="test",
        )

    mocks = [
        MockLLMClient([
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name="take",
                        arguments=json.dumps({"item": "llave"}),
                    ),
                ],
            ),
            LLMResponse(content="Listo."),
        ]),
        MockLLMClient([
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-2",
                        name="take",
                        arguments=json.dumps({"item": "llave"}),
                    ),
                ],
            ),
            LLMResponse(content="Listo."),
        ]),
    ]
    mock_iterator = iter(mocks)

    worlds = []
    agents = []

    real_make_world_tools = experiment.make_world_tools
    real_build_agent = experiment.build_agent

    def recording_make_world_tools(world):
        worlds.append(world)
        return real_make_world_tools(world)

    def recording_build_agent(config):
        agent = real_build_agent(config)
        agents.append(agent)
        return agent

    monkeypatch.setattr(
        experiment,
        "_resolve_scenario",
        lambda spec: make_scenario(),
    )
    monkeypatch.setattr(
        experiment,
        "build_llm_client",
        lambda name: next(mock_iterator),
    )
    monkeypatch.setattr(
        experiment,
        "make_world_tools",
        recording_make_world_tools,
    )
    monkeypatch.setattr(
        experiment,
        "build_agent",
        recording_build_agent,
    )

    result = experiment.run_experiment(
        scenario_spec="test-independent-trials",
        agent_config_name="minimal",
        llm_config_name="llama3.1",
        experiment_config={
            "max_attempts": 1,
            "continuation_message": CONTINUATION_MESSAGE,
        },
        trials_count=2,
    )

    assert result["requested_trials"] == 2
    assert len(result["trials"]) == 2

    assert [trial["trial_index"] for trial in result["trials"]] == [1, 2]
    assert all(trial["goal_achieved"] for trial in result["trials"])

    assert len(worlds) == 2
    assert worlds[0] is not worlds[1]
    assert worlds[0].inventory == ["llave"]
    assert worlds[1].inventory == ["llave"]

    assert len(agents) == 2
    assert agents[0] is not agents[1]

    assert mocks[0].call_count == 2
    assert mocks[1].call_count == 2
    