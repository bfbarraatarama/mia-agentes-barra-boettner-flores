import json

import pytest

from mia_agents.testing import MockLLMClient, make_recording_tool
from mia_agents.types import LLMResponse, ToolCall
from student_framework import build_agent


def _two_completed_tool_turns() -> list[dict[str, object]]:
    """Construye dos turnos cerrados con una tool call cada uno."""

    return [
        {
            "role": "user",
            "content": "mensaje del primer turno",
        },
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call-1",
                    "type": "function",
                    "function": {
                        "name": "record",
                        "arguments": '{"text": "uno"}',
                    },
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call-1",
            "name": "record",
            "content": "recorded:uno",
        },
        {
            "role": "assistant",
            "content": "respuesta del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call-2",
                    "type": "function",
                    "function": {
                        "name": "record",
                        "arguments": '{"text": "dos"}',
                    },
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call-2",
            "name": "record",
            "content": "recorded:dos",
        },
        {
            "role": "assistant",
            "content": "respuesta del segundo turno",
        },
    ]


@pytest.mark.parametrize(
    ("max_history_messages", "expected_history"),
    [
        (
            1,
            [],
        ),
        (
            2,
            [
                {
                    "role": "assistant",
                    "content": "respuesta del primer turno",
                },
            ],
        ),
        (
            3,
            [
                {
                    "role": "user",
                    "content": "mensaje del primer turno",
                },
                {
                    "role": "assistant",
                    "content": "respuesta del primer turno",
                },
            ],
        ),
        (
            4,
            [
                {
                    "role": "user",
                    "content": "mensaje del primer turno",
                },
                {
                    "role": "assistant",
                    "content": "respuesta del primer turno",
                },
            ],
        ),
    ],
)
def test_run_reserves_space_for_next_user_after_final_response(
    max_history_messages: int,
    expected_history: list[dict[str, str]],
) -> None:
    """Al cerrar un turno se reserva espacio para el próximo usuario."""

    mock = MockLLMClient(
        [
            LLMResponse(content="respuesta del primer turno"),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": max_history_messages,
    })

    agent.run("mensaje del primer turno")

    assert agent._history == expected_history


def test_run_removes_oldest_user_before_oldest_final_response() -> None:
    """Ante exceso conversacional, elimina primero el user más antiguo."""

    mock = MockLLMClient(
        [
            LLMResponse(content="respuesta del primer turno"),
            LLMResponse(content="respuesta del segundo turno"),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 4,
    })

    agent.run("mensaje del primer turno")
    agent.run("mensaje del segundo turno")

    assert agent._history == [
        {
            "role": "assistant",
            "content": "respuesta del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del segundo turno",
        },
    ]

    assert all(
        len(call["messages"]) <= 4
        for call in mock.calls
    )


def test_run_discards_oldest_complete_tool_trace_before_user_messages() -> None:
    """La traza más antigua se elimina antes que los mensajes conversacionales."""

    tool, schema = make_recording_tool(return_value="recorded:hola")
    arguments = json.dumps({"text": "hola"})

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name=schema.name,
                        arguments=arguments,
                    )
                ],
            ),
            LLMResponse(content="respuesta del primer turno"),
            LLMResponse(content="respuesta del segundo turno"),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 5,
    })
    agent.register_tool(tool, schema)

    agent.run("mensaje del primer turno")
    agent.run("mensaje del segundo turno")

    assert tool.calls == [{"text": "hola"}]

    assert agent._history == [
        {
            "role": "user",
            "content": "mensaje del primer turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del segundo turno",
        },
    ]


def test_run_discards_all_results_from_same_tool_call_response_together() -> None:
    """Una respuesta con varias tool calls se elimina junto con sus resultados."""

    tool, schema = make_recording_tool(return_value="recorded")
    first_arguments = json.dumps({"text": "uno"})
    second_arguments = json.dumps({"text": "dos"})

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name=schema.name,
                        arguments=first_arguments,
                    ),
                    ToolCall(
                        id="call-2",
                        name=schema.name,
                        arguments=second_arguments,
                    ),
                ],
            ),
            LLMResponse(content="respuesta final"),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 4,
    })
    agent.register_tool(tool, schema)

    agent.run("mensaje de usuario")

    assert tool.calls == [
        {"text": "uno"},
        {"text": "dos"},
    ]

    assert agent._history == [
        {
            "role": "user",
            "content": "mensaje de usuario",
        },
        {
            "role": "assistant",
            "content": "respuesta final",
        },
    ]


def test_run_discards_all_tool_rounds_from_same_turn_together() -> None:
    """Todas las rondas intermedias del turno se eliminan como una unidad."""

    tool, schema = make_recording_tool(return_value="recorded")
    first_arguments = json.dumps({"text": "primera"})
    second_arguments = json.dumps({"text": "segunda"})

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name=schema.name,
                        arguments=first_arguments,
                    )
                ],
            ),
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-2",
                        name=schema.name,
                        arguments=second_arguments,
                    )
                ],
            ),
            LLMResponse(content="respuesta final"),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 5,
    })
    agent.register_tool(tool, schema)

    agent.run("mensaje de usuario")

    assert tool.calls == [
        {"text": "primera"},
        {"text": "segunda"},
    ]

    assert agent._history == [
        {
            "role": "user",
            "content": "mensaje de usuario",
        },
        {
            "role": "assistant",
            "content": "respuesta final",
        },
    ]


def test_run_discards_oldest_final_response_after_oldest_user() -> None:
    """Tras el user más antiguo se elimina la respuesta final más antigua."""

    mock = MockLLMClient(
        [
            LLMResponse(content="respuesta del primer turno"),
            LLMResponse(content="respuesta del segundo turno"),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 2,
    })

    agent.run("mensaje del primer turno")
    agent.run("mensaje del segundo turno")

    assert agent._history == [
        {
            "role": "assistant",
            "content": "respuesta del segundo turno",
        },
    ]


def test_run_stops_before_tool_execution_when_active_turn_does_not_fit() -> None:
    """No se ejecuta una herramienta si su contexto mínimo no entra."""

    tool, schema = make_recording_tool(return_value="recorded:hola")
    arguments = json.dumps({"text": "hola"})

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name=schema.name,
                        arguments=arguments,
                    )
                ],
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 2,
    })
    agent.register_tool(tool, schema)

    result = agent.run("mensaje de usuario")

    assert mock.call_count == 1
    assert tool.calls == []
    assert result.steps == []

    assert result.answer
    assert result.error == result.answer
    assert "herramienta" in result.answer.lower()
    assert "max_history_messages" in result.answer

    assert agent._history == [
        {
            "role": "assistant",
            "content": result.answer,
        },
    ]


def test_trim_run_history_removes_needed_traces_before_conversation() -> None:
    """Mientras haya exceso, se eliminan trazas antes que user o assistant."""

    agent = build_agent({
        "llm_client": MockLLMClient([]),
    })
    agent._history = _two_completed_tool_turns()

    reached_target = agent._trim_run_history(
        target_length=4,
    )

    assert reached_target is True

    assert agent._history == [
        {
            "role": "user",
            "content": "mensaje del primer turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del segundo turno",
        },
    ]


def test_trim_run_history_alternates_oldest_user_and_final_response() -> None:
    """Sin trazas, alterna user y respuesta final desde los más antiguos."""

    agent = build_agent({
        "llm_client": MockLLMClient([]),
    })
    agent._history = [
        {
            "role": "user",
            "content": "mensaje del primer turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del segundo turno",
        },
    ]

    reached_target = agent._trim_run_history(
        target_length=2,
    )

    assert reached_target is True

    assert agent._history == [
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del segundo turno",
        },
    ]


def test_run_removes_historical_trace_before_next_tool_round() -> None:
    """La siguiente llamada no recibe una traza histórica fragmentada."""

    tool, schema = make_recording_tool(return_value="recorded")
    previous_arguments = json.dumps({"text": "anterior"})
    current_arguments = json.dumps({"text": "actual"})

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-previous",
                        name=schema.name,
                        arguments=previous_arguments,
                    )
                ],
            ),
            LLMResponse(content="respuesta del primer turno"),
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-current",
                        name=schema.name,
                        arguments=current_arguments,
                    )
                ],
            ),
            LLMResponse(content="respuesta del segundo turno"),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 5,
    })
    agent.register_tool(tool, schema)

    agent.run("mensaje del primer turno")
    result = agent.run("mensaje del segundo turno")

    assert result.answer == "respuesta del segundo turno"

    assert tool.calls == [
        {"text": "anterior"},
        {"text": "actual"},
    ]

    assert mock.call_count == 4

    tool_followup_messages = mock.calls[3]["messages"]

    assert tool_followup_messages == [
        {
            "role": "user",
            "content": "mensaje del primer turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call-current",
                    "type": "function",
                    "function": {
                        "name": schema.name,
                        "arguments": current_arguments,
                    },
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call-current",
            "name": schema.name,
            "content": "recorded",
        },
    ]

    assert agent._history == [
        {
            "role": "user",
            "content": "mensaje del primer turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": "respuesta del segundo turno",
        },
    ]


def test_run_stops_before_multiple_tools_when_active_turn_does_not_fit() -> None:
    """Dos tool calls requieren dos resultados además del mensaje assistant."""

    tool, schema = make_recording_tool(return_value="recorded")
    first_arguments = json.dumps({"text": "uno"})
    second_arguments = json.dumps({"text": "dos"})

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-1",
                        name=schema.name,
                        arguments=first_arguments,
                    ),
                    ToolCall(
                        id="call-2",
                        name=schema.name,
                        arguments=second_arguments,
                    ),
                ],
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 3,
    })
    agent.register_tool(tool, schema)

    result = agent.run("mensaje de usuario")

    assert mock.call_count == 1
    assert tool.calls == []
    assert result.steps == []

    assert result.answer
    assert result.error == result.answer
    assert "herramienta" in result.answer.lower()
    assert "max_history_messages" in result.answer

    assert agent._history == [
        {
            "role": "user",
            "content": "mensaje de usuario",
        },
        {
            "role": "assistant",
            "content": result.answer,
        },
    ]


def test_run_keeps_active_turn_protected_after_historical_trimming() -> None:
    """El comienzo protegido se ajusta tras eliminar mensajes históricos."""

    tool, schema = make_recording_tool(return_value="recorded")

    previous_arguments = json.dumps({"text": "anterior"})
    first_current_arguments = json.dumps({"text": "actual-1"})
    second_current_arguments = json.dumps({"text": "actual-2"})
    third_current_arguments = json.dumps({"text": "actual-3"})

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-previous",
                        name=schema.name,
                        arguments=previous_arguments,
                    )
                ],
            ),
            LLMResponse(content="respuesta del primer turno"),
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-current-1",
                        name=schema.name,
                        arguments=first_current_arguments,
                    )
                ],
            ),
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-current-2",
                        name=schema.name,
                        arguments=second_current_arguments,
                    )
                ],
            ),
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="call-current-3",
                        name=schema.name,
                        arguments=third_current_arguments,
                    )
                ],
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 5,
    })
    agent.register_tool(tool, schema)

    agent.run("mensaje del primer turno")
    result = agent.run("mensaje del segundo turno")

    assert mock.call_count == 5

    assert all(
        len(call["messages"]) <= 5
        for call in mock.calls
    )

    assert tool.calls == [
        {"text": "anterior"},
        {"text": "actual-1"},
        {"text": "actual-2"},
    ]

    assert len(result.steps) == 2
    assert result.answer
    assert result.error == result.answer

    assert agent._history == [
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
        {
            "role": "assistant",
            "content": result.answer,
        },
    ]


@pytest.mark.parametrize(
    "max_history_messages",
    [
        0,
        -1,
    ],
)
def test_run_rejects_history_limits_below_one(
    max_history_messages: int,
) -> None:
    """run rechaza un límite que no permite enviar el user actual."""

    mock = MockLLMClient([])

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": max_history_messages,
    })

    with pytest.raises(
        ValueError,
        match="max_history_messages",
    ):
        agent.run("mensaje de usuario")

    assert mock.call_count == 0
    assert agent._history == []
    