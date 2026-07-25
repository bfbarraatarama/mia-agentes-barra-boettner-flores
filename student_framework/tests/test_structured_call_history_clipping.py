import json

import pytest
from pydantic import BaseModel

from mia_agents.testing import MockLLMClient
from mia_agents.tool_schema import FINAL_RESULT_TOOL_NAME
from mia_agents.types import LLMResponse, ToolCall
from student_framework import build_agent


class Answer(BaseModel):
    result: int


def _final_result_response(
    arguments: dict[str, object],
    *,
    call_id: str,
) -> LLMResponse:
    return LLMResponse(
        content=None,
        tool_calls=[
            ToolCall(
                id=call_id,
                name=FINAL_RESULT_TOOL_NAME,
                arguments=json.dumps(arguments),
            )
        ],
    )


@pytest.mark.parametrize(
    "max_history_messages",
    [
        0,
        -1,
    ],
)
def test_structured_call_rejects_history_limits_below_one(
    max_history_messages: int,
) -> None:
    """No se llama al LLM si ni siquiera puede enviarse el prompt."""

    mock = MockLLMClient([])

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": max_history_messages,
    })

    with pytest.raises(
        ValueError,
        match="max_history_messages",
    ):
        agent.structured_call(
            prompt="dame un resultado",
            schema=Answer,
        )

    assert mock.call_count == 0


def test_structured_call_uses_self_contained_repair_with_limit_one() -> None:
    """Con límite uno, el user de reparación contiene todo el contexto."""

    prompt = "Calcula el resultado solicitado."

    mock = MockLLMClient(
        [
            LLMResponse(content="respuesta en texto libre"),
            _final_result_response(
                {"result": 42},
                call_id="fr-2",
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 1,
    })

    parsed = agent.structured_call(
        prompt=prompt,
        schema=Answer,
    )

    assert parsed.result == 42
    assert mock.call_count == 2

    first_messages = mock.calls[0]["messages"]
    repair_messages = mock.calls[1]["messages"]

    assert first_messages == [
        {
            "role": "user",
            "content": prompt,
        },
    ]

    assert len(repair_messages) == 1
    assert repair_messages[0]["role"] == "user"
    assert prompt in repair_messages[0]["content"]
    assert "final_result" in repair_messages[0]["content"]

    assert all(
        len(call["messages"]) <= 1
        for call in mock.calls
    )


def test_structured_call_preserves_initial_and_repair_users_with_limit_two() -> None:
    """Con límite dos, se aplica la representación compacta elegida."""

    prompt = "Devuelve un resultado entero."

    mock = MockLLMClient(
        [
            _final_result_response(
                {"result": "no es un entero"},
                call_id="fr-1",
            ),
            _final_result_response(
                {"result": 42},
                call_id="fr-2",
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 2,
    })

    parsed = agent.structured_call(
        prompt=prompt,
        schema=Answer,
    )

    assert parsed.result == 42
    assert mock.call_count == 2

    repair_messages = mock.calls[1]["messages"]

    assert repair_messages[0] == {
        "role": "user",
        "content": prompt,
    }

    assert repair_messages[1]["role"] == "user"
    assert prompt in repair_messages[1]["content"]
    assert "result" in repair_messages[1]["content"]

    assert all(
        len(call["messages"]) <= 2
        for call in mock.calls
    )


def test_structured_call_keeps_complete_latest_tool_block_with_limit_three() -> None:
    """Con límite tres, se conserva completo el último bloque inválido."""

    prompt = "Devuelve un resultado entero."

    invalid_arguments = json.dumps({
        "result": "no es un entero",
    })

    mock = MockLLMClient(
        [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id="fr-1",
                        name=FINAL_RESULT_TOOL_NAME,
                        arguments=invalid_arguments,
                    )
                ],
            ),
            _final_result_response(
                {"result": 42},
                call_id="fr-2",
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 3,
    })

    parsed = agent.structured_call(
        prompt=prompt,
        schema=Answer,
    )

    assert parsed.result == 42
    assert mock.call_count == 2

    repair_messages = mock.calls[1]["messages"]

    assert [message["role"] for message in repair_messages] == [
        "assistant",
        "tool",
        "user",
    ]

    assert repair_messages[0]["tool_calls"] == [
        {
            "id": "fr-1",
            "type": "function",
            "function": {
                "name": FINAL_RESULT_TOOL_NAME,
                "arguments": invalid_arguments,
            },
        }
    ]

    assert repair_messages[1]["tool_call_id"] == "fr-1"
    assert repair_messages[1]["name"] == FINAL_RESULT_TOOL_NAME

    assert prompt in repair_messages[2]["content"]
    assert "result" in repair_messages[2]["content"]

    assert all(
        len(call["messages"]) <= 3
        for call in mock.calls
    )


def test_structured_call_discards_older_repair_blocks_that_do_not_fit() -> None:
    """Descarta bloques anteriores cuando no entran completos."""

    prompt = "Devuelve un resultado entero."

    mock = MockLLMClient(
        [
            _final_result_response(
                {"result": "primer error"},
                call_id="fr-1",
            ),
            _final_result_response(
                {"result": "segundo error"},
                call_id="fr-2",
            ),
            _final_result_response(
                {"result": 42},
                call_id="fr-3",
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 4,
    })

    parsed = agent.structured_call(
        prompt=prompt,
        schema=Answer,
        max_repair_attempts=2,
    )

    assert parsed.result == 42
    assert mock.call_count == 3

    latest_repair_messages = mock.calls[2]["messages"]

    assert [message["role"] for message in latest_repair_messages] == [
        "user",
        "assistant",
        "tool",
        "user",
    ]

    assert latest_repair_messages[0] == {
        "role": "user",
        "content": prompt,
    }

    assert (
        latest_repair_messages[1]["tool_calls"][0]["id"]
        == "fr-2"
    )
    assert latest_repair_messages[2]["tool_call_id"] == "fr-2"

    assert prompt in latest_repair_messages[3]["content"]
    assert "fr-1" not in json.dumps(latest_repair_messages)

    assert all(
        len(call["messages"]) <= 4
        for call in mock.calls
    )


def test_structured_call_keeps_older_complete_blocks_when_they_fit() -> None:
    """Conserva reparaciones anteriores completas si hay espacio."""

    prompt = "Devuelve un resultado entero."

    mock = MockLLMClient(
        [
            _final_result_response(
                {"result": "primer error"},
                call_id="fr-1",
            ),
            _final_result_response(
                {"result": "segundo error"},
                call_id="fr-2",
            ),
            _final_result_response(
                {"result": 42},
                call_id="fr-3",
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 7,
    })

    parsed = agent.structured_call(
        prompt=prompt,
        schema=Answer,
        max_repair_attempts=2,
    )

    assert parsed.result == 42

    latest_messages = mock.calls[2]["messages"]

    assert [message["role"] for message in latest_messages] == [
        "user",
        "assistant",
        "tool",
        "user",
        "assistant",
        "tool",
        "user",
    ]

    assert (
        latest_messages[1]["tool_calls"][0]["id"]
        == "fr-1"
    )
    assert latest_messages[2]["tool_call_id"] == "fr-1"

    assert (
        latest_messages[4]["tool_calls"][0]["id"]
        == "fr-2"
    )
    assert latest_messages[5]["tool_call_id"] == "fr-2"

    assert all(
        len(call["messages"]) <= 7
        for call in mock.calls
    )


def test_structured_call_does_not_skip_recent_block_for_older_smaller_block(
) -> None:
    """No rescata un bloque antiguo si uno más reciente no entra."""

    prompt = "Devuelve un resultado entero."

    mock = MockLLMClient(
        [
            LLMResponse(content="respuesta libre antigua"),
            _final_result_response(
                {"result": "segundo error"},
                call_id="fr-2",
            ),
            _final_result_response(
                {"result": "tercer error"},
                call_id="fr-3",
            ),
            _final_result_response(
                {"result": 42},
                call_id="fr-4",
            ),
        ]
    )

    agent = build_agent({
        "llm_client": mock,
        "max_history_messages": 6,
    })

    parsed = agent.structured_call(
        prompt=prompt,
        schema=Answer,
        max_repair_attempts=3,
    )

    assert parsed.result == 42
    assert mock.call_count == 4

    latest_messages = mock.calls[3]["messages"]

    assert [message["role"] for message in latest_messages] == [
        "user",
        "assistant",
        "tool",
        "user",
    ]

    assert latest_messages[0] == {
        "role": "user",
        "content": prompt,
    }

    assert (
        latest_messages[1]["tool_calls"][0]["id"]
        == "fr-3"
    )
    assert latest_messages[2]["tool_call_id"] == "fr-3"

    serialized_messages = json.dumps(latest_messages)

    assert "fr-2" not in serialized_messages
    assert "respuesta libre antigua" not in serialized_messages

    assert all(
        len(call["messages"]) <= 6
        for call in mock.calls
    )