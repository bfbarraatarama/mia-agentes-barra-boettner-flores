import json

from pydantic import BaseModel

from mia_agents.testing import MockLLMClient
from mia_agents.tool_schema import FINAL_RESULT_TOOL_NAME
from mia_agents.types import LLMResponse, ToolCall
from student_framework import build_agent


class Answer(BaseModel):
    result: int


def test_structured_call_preserves_failed_tool_call_in_history() -> None:
    """El segundo intento debe recibir la tool call fallida en formato function."""

    invalid_arguments = json.dumps({"result": "no-es-un-entero"})

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="fr-invalid",
                        name=FINAL_RESULT_TOOL_NAME,
                        arguments=invalid_arguments,
                    )
                ],
            ),
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="fr-valid",
                        name=FINAL_RESULT_TOOL_NAME,
                        arguments=json.dumps({"result": 42}),
                    )
                ],
            ),
        ]
    )

    agent = build_agent({"llm_client": mock})

    agent.structured_call(
        prompt="Devuelve un resultado entero",
        schema=Answer,
    )

    second_attempt_messages = mock.calls[1]["messages"]

    failed_assistant_message = next(
        message
        for message in second_attempt_messages
        if message.get("role") == "assistant"
        and message.get("tool_calls")
    )

    failed_tool_call = failed_assistant_message["tool_calls"][0]

    assert "function" in failed_tool_call
    assert failed_tool_call["function"]["name"] == FINAL_RESULT_TOOL_NAME
    assert failed_tool_call["function"]["arguments"] == invalid_arguments