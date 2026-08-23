import json

import pytest

from mia_agents.testing import MockLLMClient
from mia_agents.tool_schema import FINAL_RESULT_TOOL_NAME
from mia_agents.types import LLMResponse, ToolCall
from student_framework import build_agent


def test_planner_run_counts_planning_repair_and_agent_tokens() -> None:
    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="plan-invalid",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({"steps": []}),
                )
            ],
            input_tokens=10,
            output_tokens=2,
        ),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="plan-valid",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "steps": [
                            {"description": "Examinar la puerta"},
                        ],
                    }),
                )
            ],
            input_tokens=20,
            output_tokens=3,
        ),
        LLMResponse(
            content="hecho",
            input_tokens=30,
            output_tokens=4,
        ),
    ])
    trace_events: list[dict[str, object]] = []

    agent = build_agent({
        "llm_client": mock,
        "register_default_tools": False,
        "use_planner": True,
        "planning_prompt": "Planificá cuidadosamente esta tarea.",
        "plan_guidance": "Usá el plan como orientación flexible.",
        "trace_callback": trace_events.append,
    })

    result = agent.run("Abrí la puerta.")

    assert mock.calls[0]["messages"] == [
        {
            "role": "user",
            "content": (
                "Planificá cuidadosamente esta tarea.\n\n"
                "Abrí la puerta."
            ),
        },
    ]

    assert mock.calls[2]["messages"] == [
        {
            "role": "user",
            "content": (
                "Abrí la puerta.\n\n"
                "Plan de acción:\n"
                "1. Examinar la puerta\n\n"
                "Usá el plan como orientación flexible."
            ),
        },
    ]

    assert result.answer == "hecho"
    assert result.input_tokens == 60
    assert result.output_tokens == 9
    assert mock.call_count == 3

    llm_events = [
        event
        for event in trace_events
        if event["type"] == "llm_call"
    ]

    assert [event["purpose"] for event in llm_events] == [
        "planning",
        "planning",
        "agent",
    ]

    planning_events = [
        event
        for event in trace_events
        if event["type"] == "planning"
    ]

    assert planning_events == [
        {
            "type": "planning",
            "plan": {
                "steps": [
                    {"description": "Examinar la puerta"},
                ],
            },
        },
    ]


def test_planner_respects_planning_repair_limit() -> None:
    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="plan-invalid",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({"steps": []}),
                )
            ],
        ),
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="plan-valid",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "steps": [
                            {"description": "Examinar la puerta"},
                        ],
                    }),
                )
            ],
        ),
        LLMResponse(content="hecho"),
    ])

    agent = build_agent({
        "llm_client": mock,
        "register_default_tools": False,
        "use_planner": True,
        "planning_repair_max_attempts": 0,
    })

    with pytest.raises(ValueError):
        agent.run("Abrí la puerta.")

    assert mock.call_count == 1


def test_planner_generates_plan_only_for_initial_turn() -> None:
    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="plan",
                    name=FINAL_RESULT_TOOL_NAME,
                    arguments=json.dumps({
                        "steps": [
                            {"description": "Examinar la puerta"},
                        ],
                    }),
                )
            ],
        ),
        LLMResponse(content="Todavía no terminé."),
        LLMResponse(content="Continúo con la tarea."),
    ])
    trace_events: list[dict[str, object]] = []

    agent = build_agent({
        "llm_client": mock,
        "register_default_tools": False,
        "use_planner": True,
        "trace_callback": trace_events.append,
    })

    first_result = agent.run("Abrí la puerta.")
    second_result = agent.run("El desafío todavía no está completado. Continuá.")

    assert first_result.answer == "Todavía no terminé."
    assert second_result.answer == "Continúo con la tarea."
    assert mock.call_count == 3

    llm_events = [
        event
        for event in trace_events
        if event["type"] == "llm_call"
    ]

    assert [event["purpose"] for event in llm_events] == [
        "planning",
        "agent",
        "agent",
    ]

    second_run_messages = mock.calls[2]["messages"]

    assert "Plan de acción:" in second_run_messages[0]["content"]
    assert second_run_messages[-1] == {
        "role": "user",
        "content": "El desafío todavía no está completado. Continuá.",
    }
