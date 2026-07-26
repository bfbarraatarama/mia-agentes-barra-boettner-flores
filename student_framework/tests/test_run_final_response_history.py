import json

from mia_agents.testing import MockLLMClient, make_recording_tool
from mia_agents.types import LLMResponse, ToolCall
from student_framework import build_agent


def test_run_preserves_final_response_in_history_across_runs() -> None:
    """El segundo turno recibe la respuesta final del asistente del primero."""

    mock = MockLLMClient(
        [
            LLMResponse(content="respuesta arbitraria del primer turno"),
            LLMResponse(content="respuesta final del segundo turno"),
        ]
    )

    agent = build_agent({"llm_client": mock})

    agent.run("mensaje del primer turno")
    agent.run("mensaje del segundo turno")

    assert mock.calls[1]["messages"] == [
        {
            "role": "user",
            "content": "mensaje del primer turno",
        },
        {
            "role": "assistant",
            "content": "respuesta arbitraria del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
    ]

def test_run_preserves_final_response_after_tool_call_across_runs() -> None:
    """El segundo turno recibe la respuesta final posterior a una tool call."""

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
            LLMResponse(content="respuesta final del primer turno"),
            LLMResponse(content="respuesta final del segundo turno"),
        ]
    )

    agent = build_agent({"llm_client": mock})
    agent.register_tool(tool, schema)

    agent.run("mensaje del primer turno")
    agent.run("mensaje del segundo turno")

    assert tool.calls == [{"text": "hola"}]

    assert mock.calls[2]["messages"] == [
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
                        "name": schema.name,
                        "arguments": arguments,
                    },
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call-1",
            "name": schema.name,
            "content": "recorded:hola",
        },
        {
            "role": "assistant",
            "content": "respuesta final del primer turno",
        },
        {
            "role": "user",
            "content": "mensaje del segundo turno",
        },
    ]