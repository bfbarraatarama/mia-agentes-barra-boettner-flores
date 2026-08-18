from mia_agents.testing import MockLLMClient
from mia_agents.types import LLMResponse
from student_framework import build_agent


def test_run_trace_records_successful_llm_call() -> None:
    """La traza conserva la llamada efectiva y la respuesta del LLM."""

    events = []
    response = LLMResponse(
        content="respuesta final",
        input_tokens=11,
        output_tokens=4,
        raw_response={"done_reason": "stop"},
    )
    mock = MockLLMClient([response])

    agent = build_agent({
        "llm_client": mock,
        "trace_callback": events.append,
    })

    result = agent.run("mensaje inicial")

    assert result.answer == "respuesta final"
    assert len(events) == 1

    event = events[0]

    assert event["type"] == "llm_call"
    assert event["retry_index"] == 0
    assert event["messages"] == [
        {
            "role": "user",
            "content": "mensaje inicial",
        },
    ]
    assert event["response"] is response

    mock.calls[0]["messages"].append({
        "role": "user",
        "content": "mutación posterior",
    })

    assert event["messages"] == [
        {
            "role": "user",
            "content": "mensaje inicial",
        },
    ]


def test_run_trace_records_transient_llm_retry() -> None:
    """La traza distingue el fallo transitorio de la llamada reintentada."""

    events = []
    transient_error = TimeoutError("timeout controlado")
    response = LLMResponse(content="respuesta recuperada")

    mock = MockLLMClient([
        transient_error,
        response,
    ])

    agent = build_agent({
        "llm_client": mock,
        "trace_callback": events.append,
    })

    result = agent.run("mensaje inicial")

    assert result.answer == "respuesta recuperada"
    assert mock.call_count == 2
    assert len(events) == 2

    first_event = events[0]

    assert first_event["type"] == "llm_call"
    assert first_event["retry_index"] == 0
    assert first_event["messages"] == [
        {
            "role": "user",
            "content": "mensaje inicial",
        },
    ]
    assert first_event["error"] is transient_error

    second_event = events[1]

    assert second_event["type"] == "llm_call"
    assert second_event["retry_index"] == 1
    assert second_event["messages"] == [
        {
            "role": "user",
            "content": "mensaje inicial",
        },
    ]
    assert second_event["response"] is response


import json

from mia_agents.testing import MockLLMClient, make_recording_tool
from mia_agents.types import LLMResponse, ToolCall
from student_framework import build_agent


def test_run_trace_records_successful_tool_execution() -> None:
    """La traza conserva la ejecución efectiva de una tool."""

    events = []
    tool, schema = make_recording_tool(
        return_value="recorded:hola",
    )
    arguments = json.dumps({"text": "hola"})

    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name=schema.name,
                    arguments=arguments,
                ),
            ],
        ),
        LLMResponse(content="respuesta final"),
    ])

    agent = build_agent({
        "llm_client": mock,
        "trace_callback": events.append,
    })
    agent.register_tool(tool, schema)

    result = agent.run("usá la herramienta")

    assert result.answer == "respuesta final"
    assert [
        event["type"]
        for event in events
    ] == [
        "llm_call",
        "tool_execution",
        "llm_call",
    ]

    tool_event = events[1]

    assert tool_event["retry_index"] == 0
    assert tool_event["tool_name"] == schema.name
    assert tool_event["arguments"] == {"text": "hola"}
    assert tool_event["output"] == "recorded:hola"


def test_run_trace_records_transient_tool_retry() -> None:
    """La traza distingue cada ejecución física durante un retry."""

    events = []
    calls = []

    _, schema = make_recording_tool()
    arguments = json.dumps({"text": "hola"})

    def flaky_tool(**kwargs):
        calls.append(kwargs)

        if len(calls) == 1:
            raise ConnectionError("fallo transitorio controlado")

        return "recorded:hola"

    mock = MockLLMClient([
        LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name=schema.name,
                    arguments=arguments,
                ),
            ],
        ),
        LLMResponse(content="respuesta recuperada"),
    ])

    agent = build_agent({
        "llm_client": mock,
        "trace_callback": events.append,
    })
    agent.register_tool(flaky_tool, schema)

    result = agent.run("usá la herramienta")

    assert result.answer == "respuesta recuperada"
    assert calls == [
        {"text": "hola"},
        {"text": "hola"},
    ]

    tool_events = [
        event
        for event in events
        if event["type"] == "tool_execution"
    ]

    assert len(tool_events) == 2

    first_event = tool_events[0]

    assert first_event["retry_index"] == 0
    assert first_event["tool_name"] == schema.name
    assert first_event["arguments"] == {"text": "hola"}
    assert isinstance(first_event["error"], ConnectionError)
    assert str(first_event["error"]) == "fallo transitorio controlado"

    second_event = tool_events[1]

    assert second_event["retry_index"] == 1
    assert second_event["tool_name"] == schema.name
    assert second_event["arguments"] == {"text": "hola"}
    assert second_event["output"] == "recorded:hola"