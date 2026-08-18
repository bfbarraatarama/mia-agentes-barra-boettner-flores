from eval.analyses.tool_call_repair_analysis import (
    analyze_tool_call_repair,
)


def _llm_event(
    purpose: str,
    *,
    input_tokens: int,
    output_tokens: int,
) -> dict:
    return {
        "type": "llm_call",
        "purpose": purpose,
        "retry_index": 0,
        "response": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        },
    }


def _failed_llm_event(
    purpose: str,
) -> dict:
    return {
        "type": "llm_call",
        "purpose": purpose,
        "retry_index": 1,
        "error": {
            "type": "TimeoutError",
            "message": "timeout",
        },
    }


def test_tool_call_repair_analysis_counts_activity_and_tokens_by_system() -> None:
    run_manifest = {
        "run_id": "test-run",
    }

    run_result = {
        "results": [
            {
                "agent_config": "minimal",
                "llm_config": "llama3.1",
                "trials": [
                    {
                        "attempts": [
                            {
                                "trace": [
                                    _llm_event(
                                        "agent",
                                        input_tokens=100,
                                        output_tokens=10,
                                    ),
                                ],
                            },
                        ],
                    },
                    {
                        "attempts": [
                            {
                                "trace": [
                                    _llm_event(
                                        "agent",
                                        input_tokens=100,
                                        output_tokens=10,
                                    ),
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "agent_config": "minimal_tool_repair",
                "llm_config": "llama3.1",
                "trials": [
                    {
                        "attempts": [
                            {
                                "trace": [
                                    _llm_event(
                                        "agent",
                                        input_tokens=100,
                                        output_tokens=10,
                                    ),
                                    _llm_event(
                                        "tool_call_repair",
                                        input_tokens=500,
                                        output_tokens=20,
                                    ),
                                    _llm_event(
                                        "tool_call_repair",
                                        input_tokens=510,
                                        output_tokens=21,
                                    ),
                                ],
                            },
                        ],
                    },
                    {
                        "attempts": [
                            {
                                "trace": [
                                    _llm_event(
                                        "agent",
                                        input_tokens=100,
                                        output_tokens=10,
                                    ),
                                    _failed_llm_event(
                                        "tool_call_repair",
                                    ),
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    }

    analysis = analyze_tool_call_repair(
        run_manifest,
        run_result,
    )

    assert analysis["run_id"] == "test-run"
    assert analysis["total_trials"] == 4
    assert analysis["trials_with_repair"] == 2
    assert analysis["repair_llm_calls"] == 3
    assert analysis["repair_llm_responses"] == 2
    assert analysis["repair_llm_errors"] == 1
    assert analysis["repair_llm_calls_with_token_usage"] == 2
    assert analysis["repair_llm_calls_without_token_usage"] == 1
    assert analysis["repair_input_tokens"] == 1010
    assert analysis["repair_output_tokens"] == 41
    assert analysis["token_usage_complete"] is False

    assert analysis["systems"] == {
        "minimal": {
            "llama3.1": {
                "trials": 2,
                "trials_with_repair": 0,
                "repair_llm_calls": 0,
                "repair_llm_responses": 0,
                "repair_llm_errors": 0,
                "repair_llm_calls_with_token_usage": 0,
                "repair_llm_calls_without_token_usage": 0,
                "repair_input_tokens": 0,
                "repair_output_tokens": 0,
                "token_usage_complete": True,
            },
        },
        "minimal_tool_repair": {
            "llama3.1": {
                "trials": 2,
                "trials_with_repair": 2,
                "repair_llm_calls": 3,
                "repair_llm_responses": 2,
                "repair_llm_errors": 1,
                "repair_llm_calls_with_token_usage": 2,
                "repair_llm_calls_without_token_usage": 1,
                "repair_input_tokens": 1010,
                "repair_output_tokens": 41,
                "token_usage_complete": False,
            },
        },
    }