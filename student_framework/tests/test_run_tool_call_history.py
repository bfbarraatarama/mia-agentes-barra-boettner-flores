import json
from typing import Any

from mia_agents.llm_client import OllamaProvider
from mia_agents.testing import MockLLMClient, make_recording_tool
from mia_agents.types import LLMResponse, ToolCall
from student_framework import build_agent


def _run_with_tool_call() -> tuple[list[dict[str, Any]], str]:
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
            LLMResponse(content="La herramienta se ejecutó."),
        ]
    )

    agent = build_agent({"llm_client": mock})
    agent.register_tool(tool, schema)
    agent.run("Invocá la herramienta con el texto hola.")

    return mock.calls[1]["messages"], arguments


def test_run_preserves_tool_call_in_history() -> None:
    """La segunda llamada conserva la tool call y su resultado asociado."""

    second_call_messages, arguments = _run_with_tool_call()

    assistant_message = next(
        message
        for message in second_call_messages
        if message.get("role") == "assistant"
        and message.get("tool_calls")
    )
    tool_call = assistant_message["tool_calls"][0]

    assert tool_call["id"] == "call-1"
    assert tool_call["type"] == "function"
    assert tool_call["function"]["name"] == "record"
    assert tool_call["function"]["arguments"] == arguments

    tool_message = next(
        message
        for message in second_call_messages
        if message.get("role") == "tool"
    )

    assert tool_message["tool_call_id"] == tool_call["id"]


def test_run_history_is_compatible_with_ollama_normalizer() -> None:
    """Ollama conserva el nombre y los argumentos generados por run()."""

    second_call_messages, arguments = _run_with_tool_call()

    normalized_messages = OllamaProvider._normalize_messages(
        second_call_messages,
        system=None,
    )
    assistant_message = next(
        message
        for message in normalized_messages
        if message.get("role") == "assistant"
        and message.get("tool_calls")
    )
    normalized_tool_call = assistant_message["tool_calls"][0]

    assert normalized_tool_call["function"]["name"] == "record"
    assert normalized_tool_call["function"]["arguments"] == json.loads(arguments)

