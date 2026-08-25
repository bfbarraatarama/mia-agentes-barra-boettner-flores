import json

import pytest

from mia_agents.testing import MockLLMClient, make_recording_tool
from mia_agents.types import LLMResponse, ToolCall
from mia_world import Item, Room, Scenario, World

from eval import experiment, persistence
from eval.analyses.attempt_recovery_analysis import (
    analyze_attempt_recovery,
    render_markdown,
)
from eval.configs.run_configs import (
    M3_FINAL_RECOVERY_RUN_CONFIG,
)
from eval.configs.trial_configs import (
    CONTEXT_OVERFLOW_RECOVERY_MESSAGE,
    CONTINUATION_MESSAGE,
    MAX_ITERATIONS_RECOVERY_MESSAGE,
    TRIAL_CONFIGS,
)
from student_framework.agent import MyAgent


def test_run_traces_max_iterations_termination() -> None:
    """max_iterations expone una causa de terminación estructurada."""

    events = []
    tool, schema = make_recording_tool()

    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name=schema.name,
                    arguments=json.dumps({"text": "uno"}),
                ),
            ],
        ),
    ])

    agent = MyAgent(
        llm_client=mock,
        max_iterations=1,
        max_history_messages=10,
        trace_callback=events.append,
    )
    agent.register_tool(tool, schema)

    result = agent.run("ejecutá una herramienta")

    assert result.error is not None
    assert events[-1] == {
        "type": "run_termination",
        "reason": "max_iterations",
        "max_iterations": 1,
    }


def test_run_traces_context_overflow_without_executing_round() -> None:
    """context_overflow registra la ronda rechazada sin ejecutarla."""

    events = []
    tool, schema = make_recording_tool()

    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name=schema.name,
                    arguments=json.dumps({"text": "uno"}),
                ),
            ],
        ),
    ])

    agent = MyAgent(
        llm_client=mock,
        max_iterations=2,
        max_history_messages=2,
        trace_callback=events.append,
    )
    agent.register_tool(tool, schema)

    result = agent.run("ejecutá una herramienta")

    assert result.error is not None
    assert tool.calls == []
    assert events[-1] == {
        "type": "run_termination",
        "reason": "context_overflow",
        "requested_tool_calls": 1,
        "round_messages_to_add": 2,
        "max_history_messages": 2,
    }




def test_recovery_feedback_configuration_semantics() -> None:
    """La política distingue fatal, default, override y sin feedback."""

    assert experiment._resolve_recovery_user_message(
        termination_reason="max_iterations",
        trial_config={
            "max_attempts": 2,
            "continuation_message": CONTINUATION_MESSAGE,
        },
    ) is None

    assert experiment._resolve_recovery_user_message(
        termination_reason="max_iterations",
        trial_config={
            "max_attempts": 2,
            "continuation_message": CONTINUATION_MESSAGE,
            "recoverable_attempt_terminations": {
                "max_iterations": None,
            },
        },
    ) == (
        f"{MAX_ITERATIONS_RECOVERY_MESSAGE}\n\n"
        f"{CONTINUATION_MESSAGE}"
    )

    assert experiment._resolve_recovery_user_message(
        termination_reason="max_iterations",
        trial_config={
            "max_attempts": 2,
            "continuation_message": CONTINUATION_MESSAGE,
            "recoverable_attempt_terminations": {
                "max_iterations": "Feedback controlado.",
            },
        },
    ) == (
        "Feedback controlado.\n\n"
        f"{CONTINUATION_MESSAGE}"
    )

    assert experiment._resolve_recovery_user_message(
        termination_reason="max_iterations",
        trial_config={
            "max_attempts": 2,
            "continuation_message": CONTINUATION_MESSAGE,
            "recoverable_attempt_terminations": {
                "max_iterations": "",
            },
        },
    ) == CONTINUATION_MESSAGE


def test_run_trial_recovers_from_max_iterations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """max_iterations recuperable abre otro attempt."""

    scenario = Scenario(
        id="test-max-iterations-recovery",
        description="Escenario controlado para probar recuperación.",
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
    ])

    agent_config = dict(experiment.AGENT_CONFIGS["minimal"])
    agent_config["max_iterations"] = 1

    monkeypatch.setattr(
        experiment,
        "_resolve_scenario",
        lambda spec: scenario,
    )
    monkeypatch.setattr(
        experiment,
        "build_llm_client",
        lambda config: mock,
    )

    trial = experiment.run_trial(
        scenario_spec="test-max-iterations-recovery",
        agent_config=agent_config,
        llm_config=experiment.LLM_CONFIGS["llama3.1"],
        trial_config={
            "max_attempts": 3,
            "continuation_message": CONTINUATION_MESSAGE,
            "recoverable_attempt_terminations": {
                "max_iterations": "Feedback de recuperación.",
            },
        },
        trial_index=1,
    )

    assert trial["goal_achieved"] is True
    assert len(trial["attempts"]) == 2
    assert mock.call_count == 2

    assert trial["attempts"][0]["goal_achieved"] is False
    assert trial["attempts"][1]["goal_achieved"] is True
    assert trial["attempts"][1]["user_message"] == (
        "Feedback de recuperación.\n\n"
        f"{CONTINUATION_MESSAGE}"
    )

    assert trial["attempts"][0]["trace"][-1]["reason"] == (
        "max_iterations"
    )


def test_run_trial_recovers_from_context_overflow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Un nuevo attempt puede continuar tras cerrar el historial desbordado."""

    scenario = Scenario(
        id="test-context-overflow-recovery",
        description="Escenario controlado para probar recuperación.",
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
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-2",
                    name="look",
                    arguments=json.dumps({}),
                ),
            ],
        ),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-3",
                    name="take",
                    arguments=json.dumps({"item": "llave"}),
                ),
            ],
        ),
        LLMResponse(content="Listo."),
    ])

    agent_config = dict(experiment.AGENT_CONFIGS["minimal"])
    agent_config["max_iterations"] = 3
    agent_config["max_history_messages"] = 3

    monkeypatch.setattr(
        experiment,
        "_resolve_scenario",
        lambda spec: scenario,
    )
    monkeypatch.setattr(
        experiment,
        "build_llm_client",
        lambda config: mock,
    )

    trial = experiment.run_trial(
        scenario_spec="test-context-overflow-recovery",
        agent_config=agent_config,
        llm_config=experiment.LLM_CONFIGS["llama3.1"],
        trial_config={
            "max_attempts": 2,
            "continuation_message": CONTINUATION_MESSAGE,
            "recoverable_attempt_terminations": {
                "context_overflow": "Feedback de contexto.",
            },
        },
        trial_index=1,
    )

    assert trial["goal_achieved"] is True
    assert len(trial["attempts"]) == 2
    assert mock.call_count == 4

    assert trial["attempts"][0]["trace"][-1]["reason"] == (
        "context_overflow"
    )
    assert trial["attempts"][1]["user_message"] == (
        "Feedback de contexto.\n\n"
        f"{CONTINUATION_MESSAGE}"
    )

    assert len(mock.calls[2]["messages"]) <= 3
    assert mock.calls[2]["messages"][-1] == {
        "role": "user",
        "content": (
            "Feedback de contexto.\n\n"
            f"{CONTINUATION_MESSAGE}"
        ),
    }


def test_recovery_run_manifest_materializes_effective_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """El manifest conserva literalmente la política de recuperación."""

    monkeypatch.setattr(
        persistence,
        "_created_at",
        lambda: "2026-08-25T00:00:00+00:00",
    )
    monkeypatch.setattr(
        persistence,
        "_git_metadata",
        lambda: {
            "commit": "abc123",
            "branch": "m3/final-experimental-improvements",
            "dirty": False,
        },
    )

    manifest = persistence.build_run_manifest(
        run_id="m3-final-run-002",
        run_config=M3_FINAL_RECOVERY_RUN_CONFIG,
    )

    assert manifest["run"]["trial_configs"] == [
        "multi_attempt_recovery",
    ]
    assert manifest["trial_configs"] == {
        "multi_attempt_recovery": (
            TRIAL_CONFIGS["multi_attempt_recovery"]
        ),
    }
    assert manifest["trial_configs"][
        "multi_attempt_recovery"
    ]["recoverable_attempt_terminations"] == {
        "max_iterations": MAX_ITERATIONS_RECOVERY_MESSAGE,
        "context_overflow": CONTEXT_OVERFLOW_RECOVERY_MESSAGE,
    }

    json.dumps(
        manifest,
        ensure_ascii=False,
    )


def test_attempt_recovery_analysis_tracks_outcomes_and_legacy_runs() -> None:
    """El análisis distingue terminación, recovery y resultado final."""

    recovery_policy = {
        "max_iterations": "Feedback de iteraciones.",
        "context_overflow": "Feedback de contexto.",
    }

    def termination_attempt(
        attempt_index: int,
        reason: str,
        *,
        goal_achieved: bool = False,
    ) -> dict:
        return {
            "attempt_index": attempt_index,
            "goal_achieved": goal_achieved,
            "trace": [
                {
                    "type": "run_termination",
                    "reason": reason,
                },
            ],
        }

    recovery_trials = [
        {
            "trial_index": 1,
            "goal_achieved": True,
            "attempts": [
                termination_attempt(
                    1,
                    "max_iterations",
                ),
                termination_attempt(
                    2,
                    "max_iterations",
                ),
                {
                    "attempt_index": 3,
                    "goal_achieved": True,
                    "trace": [],
                },
            ],
        },
        {
            "trial_index": 2,
            "goal_achieved": False,
            "attempts": [
                termination_attempt(
                    1,
                    "context_overflow",
                ),
                {
                    "attempt_index": 2,
                    "goal_achieved": False,
                    "trace": [],
                },
            ],
        },
        {
            "trial_index": 3,
            "goal_achieved": True,
            "attempts": [
                termination_attempt(
                    1,
                    "context_overflow",
                    goal_achieved=True,
                ),
            ],
        },
        {
            "trial_index": 4,
            "goal_achieved": False,
            "attempts": [
                termination_attempt(
                    1,
                    "context_overflow",
                ),
            ],
        },
    ]

    run_source = {
        "run_id": "m3-final-run-test",
        "manifest": {
            "trial_configs": {
                "multi_attempt_recovery": {
                    "max_attempts": 10,
                    "continuation_message": CONTINUATION_MESSAGE,
                    "recoverable_attempt_terminations": (
                        recovery_policy
                    ),
                },
                "multi_attempt": {
                    "max_attempts": 10,
                    "continuation_message": CONTINUATION_MESSAGE,
                },
            },
        },
        "result": {
            "results": [
                {
                    "agent_config": "baseline",
                    "llm_config": "nova-lite",
                    "trial_config": "multi_attempt_recovery",
                    "scenario": "study-with-key",
                    "trials": recovery_trials,
                },
                {
                    "agent_config": "baseline",
                    "llm_config": "nova-lite",
                    "trial_config": "multi_attempt",
                    "scenario": "study-with-key",
                    "trials": [
                        {
                            "trial_index": 1,
                            "goal_achieved": False,
                            "attempts": [
                                {
                                    "attempt_index": 1,
                                    "goal_achieved": False,
                                    "trace": [],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    }

    analysis = analyze_attempt_recovery([run_source])

    assert analysis[
        "ignored_trials_without_recovery_policy"
    ] == 1

    totals = analysis["totals"]

    assert totals["trials"] == 4
    assert totals["trials_with_termination"] == 4
    assert totals["termination_events"] == 5
    assert totals["configured_termination_events"] == 5

    assert totals["goal_already_achieved_events"] == 1

    assert totals["recovery_events"] == 3
    assert totals["trials_with_recovery"] == 2
    assert totals["recovered_trials_succeeded"] == 1
    assert totals["recovered_trials_failed"] == 1
    assert totals["recovered_trial_success_rate"] == 0.5

    assert totals["configured_events_without_recovery"] == 1
    assert totals["fatal_events"] == 0
    assert totals["unexpected_recovery_events"] == 0
    assert totals[
        "trials_with_multiple_termination_events"
    ] == 1

    max_iterations = totals["reasons"]["max_iterations"]

    assert max_iterations["termination_events"] == 2
    assert max_iterations["recovery_events"] == 2
    assert max_iterations["recovered_trials"] == 1
    assert max_iterations["recovered_trials_succeeded"] == 1
    assert max_iterations["recovered_trials_failed"] == 0
    assert max_iterations["recovered_trial_success_rate"] == 1.0
    assert max_iterations["trials_with_repeated_reason"] == 1
    assert max_iterations["events_by_attempt_index"] == {
        1: 1,
        2: 1,
    }

    context_overflow = totals["reasons"]["context_overflow"]

    assert context_overflow["termination_events"] == 3
    assert context_overflow["recovery_events"] == 1
    assert context_overflow["recovered_trials"] == 1
    assert context_overflow["recovered_trials_succeeded"] == 0
    assert context_overflow["recovered_trials_failed"] == 1
    assert context_overflow[
        "goal_already_achieved_events"
    ] == 1
    assert context_overflow[
        "configured_events_without_recovery"
    ] == 1

    assert len(analysis["conditions"]) == 1
    assert len(analysis["cases"]) == 1

    markdown = render_markdown(analysis)

    assert (
        "# Análisis de recuperación entre attempts — M3"
        in markdown
    )
    assert "| `max_iterations` | 2 |" in markdown
    assert "| `context_overflow` | 3 |" in markdown
    assert (
        "**Trials ignorados sin política de recovery:** 1"
        in markdown
    )