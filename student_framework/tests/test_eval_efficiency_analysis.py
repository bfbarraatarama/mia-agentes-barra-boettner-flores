from eval.analyses.efficiency_analysis import (
    analyze_efficiency,
    render_markdown,
)

def _trial(
    trial_index: int,
    *,
    goal_achieved: bool,
    attempts: int,
) -> dict:
    return {
        "trial_index": trial_index,
        "goal_achieved": goal_achieved,
        "attempts": [
            {
                "agent_result": {
                    "steps": [],
                },
                "trace": [],
            }
            for _ in range(attempts)
        ],
    }


def test_efficiency_keeps_trial_configs_as_separate_conditions() -> None:
    run_sources = [
        {
            "run_id": "run-001",
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "single_attempt",
                        "scenario": "color-locks",
                        "trials": [
                            _trial(
                                1,
                                goal_achieved=False,
                                attempts=1,
                            ),
                        ],
                    },
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "multi_attempt",
                        "scenario": "color-locks",
                        "trials": [
                            _trial(
                                1,
                                goal_achieved=True,
                                attempts=3,
                            ),
                        ],
                    },
                ],
            },
        },
    ]

    analysis = analyze_efficiency(run_sources)

    assert set(analysis["systems"]) == {
        "minimal / nova-lite / single_attempt",
        "minimal / nova-lite / multi_attempt",
    }

    single_attempt = analysis["systems"][
        "minimal / nova-lite / single_attempt"
    ]
    multi_attempt = analysis["systems"][
        "minimal / nova-lite / multi_attempt"
    ]

    assert single_attempt["trial_config"] == "single_attempt"
    assert multi_attempt["trial_config"] == "multi_attempt"

    assert single_attempt["global"]["trials"] == 1
    assert single_attempt["global"]["success_rate"] == 0.0
    assert single_attempt["global"]["attempts_per_trial"] == 1.0

    assert multi_attempt["global"]["trials"] == 1
    assert multi_attempt["global"]["success_rate"] == 1.0
    assert multi_attempt["global"]["attempts_per_trial"] == 3.0


def test_efficiency_counts_only_llm_retries() -> None:
    run_sources = [
        {
            "run_id": "run-001",
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "single_attempt",
                        "scenario": "color-locks",
                        "trials": [
                            {
                                "trial_index": 1,
                                "goal_achieved": True,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [],
                                        },
                                        "trace": [
                                            {
                                                "type": "llm_call",
                                                "purpose": "agent",
                                                "retry_index": 0,
                                                "error": {
                                                    "type": "TimeoutError",
                                                    "message": "timeout",
                                                },
                                            },
                                            {
                                                "type": "llm_call",
                                                "purpose": "agent",
                                                "retry_index": 1,
                                                "response": {
                                                    "input_tokens": 10,
                                                    "output_tokens": 2,
                                                },
                                            },
                                            {
                                                "type": "tool_execution",
                                                "retry_index": 0,
                                                "tool_name": "look",
                                                "error": {
                                                    "type": "ConnectionError",
                                                    "message": "fallo transitorio",
                                                },
                                            },
                                            {
                                                "type": "tool_execution",
                                                "retry_index": 1,
                                                "tool_name": "look",
                                                "output": "ok",
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        },
    ]

    analysis = analyze_efficiency(run_sources)

    metrics = analysis["systems"][
        "minimal / nova-lite / single_attempt"
    ]["global"]

    assert metrics["retries_per_trial"] == 1.0
    assert metrics["llm_calls_per_trial"] == 2.0
    assert metrics["tool_executions_per_trial"] == 2.0


def test_efficiency_per_success_includes_cost_of_failed_trials() -> None:
    run_sources = [
        {
            "run_id": "run-001",
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "single_attempt",
                        "scenario": "color-locks",
                        "trials": [
                            {
                                "trial_index": 1,
                                "goal_achieved": True,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [{}],
                                        },
                                        "trace": [
                                            {
                                                "type": "llm_call",
                                                "purpose": "agent",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 100,
                                                    "output_tokens": 20,
                                                },
                                            },
                                            {
                                                "type": "tool_execution",
                                                "retry_index": 0,
                                                "tool_name": "look",
                                            },
                                        ],
                                    },
                                ],
                            },
                            {
                                "trial_index": 2,
                                "goal_achieved": False,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [{}, {}],
                                        },
                                        "trace": [
                                            {
                                                "type": "llm_call",
                                                "purpose": "agent",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 50,
                                                    "output_tokens": 10,
                                                },
                                            },
                                            {
                                                "type": "tool_execution",
                                                "retry_index": 0,
                                                "tool_name": "examine",
                                            },
                                            {
                                                "type": "tool_execution",
                                                "retry_index": 0,
                                                "tool_name": "take",
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        },
    ]

    analysis = analyze_efficiency(run_sources)

    metrics = analysis["systems"][
        "minimal / nova-lite / single_attempt"
    ]["global"]

    assert metrics["trials"] == 2
    assert metrics["successful_trials"] == 1
    assert metrics["success_rate"] == 0.5

    assert metrics["attempts_per_success"] == 2.0
    assert metrics["total_tokens_per_success"] == 180.0
    assert metrics["llm_calls_per_success"] == 2.0
    assert metrics["tool_executions_per_success"] == 3.0
    assert metrics["steps_per_success"] == 3.0


def test_efficiency_distinguishes_steps_from_physical_tool_executions() -> None:
    run_sources = [
        {
            "run_id": "run-001",
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "multi_attempt",
                        "scenario": "color-locks",
                        "trials": [
                            {
                                "trial_index": 1,
                                "goal_achieved": True,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [
                                                {
                                                    "tool_name": "look",
                                                },
                                            ],
                                        },
                                        "trace": [
                                            {
                                                "type": "tool_execution",
                                                "tool_name": "look",
                                                "retry_index": 0,
                                                "error": {
                                                    "type": "TimeoutError",
                                                    "message": "timeout",
                                                },
                                            },
                                            {
                                                "type": "tool_execution",
                                                "tool_name": "look",
                                                "retry_index": 1,
                                                "output": "ok",
                                            },
                                        ],
                                    },
                                    {
                                        "agent_result": {
                                            "steps": [
                                                {
                                                    "tool_name": "examine",
                                                },
                                                {
                                                    "tool_name": "take",
                                                },
                                            ],
                                        },
                                        "trace": [
                                            {
                                                "type": "tool_execution",
                                                "tool_name": "examine",
                                                "retry_index": 0,
                                                "output": "ok",
                                            },
                                            {
                                                "type": "tool_execution",
                                                "tool_name": "take",
                                                "retry_index": 0,
                                                "output": "ok",
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        },
    ]

    analysis = analyze_efficiency(run_sources)

    metrics = analysis["systems"][
        "minimal / nova-lite / multi_attempt"
    ]["global"]

    assert metrics["attempts_per_trial"] == 2.0
    assert metrics["steps_per_trial"] == 3.0
    assert metrics["tool_executions_per_trial"] == 4.0


def test_efficiency_groups_llm_consumption_dynamically_by_purpose() -> None:
    run_sources = [
        {
            "run_id": "run-001",
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "single_attempt",
                        "scenario": "color-locks",
                        "trials": [
                            {
                                "trial_index": 1,
                                "goal_achieved": True,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [],
                                        },
                                        "trace": [
                                            {
                                                "type": "llm_call",
                                                "purpose": "agent",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 10,
                                                    "output_tokens": 2,
                                                },
                                            },
                                            {
                                                "type": "llm_call",
                                                "purpose": "structured_call",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 20,
                                                    "output_tokens": 3,
                                                },
                                            },
                                            {
                                                "type": "llm_call",
                                                "purpose": "tool_call_repair",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 30,
                                                    "output_tokens": 4,
                                                },
                                            },
                                            {
                                                "type": "llm_call",
                                                "purpose": "planning",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 40,
                                                    "output_tokens": 5,
                                                },
                                            },
                                            {
                                                "type": "llm_call",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 5,
                                                    "output_tokens": 1,
                                                },
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        },
    ]

    analysis = analyze_efficiency(run_sources)

    metrics = analysis["systems"][
        "minimal / nova-lite / single_attempt"
    ]["global"]

    assert metrics["llm_calls_per_trial"] == 5.0
    assert metrics["total_tokens_per_trial"] == 120.0

    assert metrics["by_purpose"] == {
        "agent": {
            "llm_calls_per_trial": 1.0,
            "input_tokens_per_trial": 10.0,
            "output_tokens_per_trial": 2.0,
            "total_tokens_per_trial": 12.0,
        },
        "planning": {
            "llm_calls_per_trial": 1.0,
            "input_tokens_per_trial": 40.0,
            "output_tokens_per_trial": 5.0,
            "total_tokens_per_trial": 45.0,
        },
        "structured_call": {
            "llm_calls_per_trial": 1.0,
            "input_tokens_per_trial": 20.0,
            "output_tokens_per_trial": 3.0,
            "total_tokens_per_trial": 23.0,
        },
        "tool_call_repair": {
            "llm_calls_per_trial": 1.0,
            "input_tokens_per_trial": 30.0,
            "output_tokens_per_trial": 4.0,
            "total_tokens_per_trial": 34.0,
        },
        "unknown": {
            "llm_calls_per_trial": 1.0,
            "input_tokens_per_trial": 5.0,
            "output_tokens_per_trial": 1.0,
            "total_tokens_per_trial": 6.0,
        },
    }


def test_efficiency_tool_usage_averages_over_all_trials() -> None:
    run_sources = [
        {
            "run_id": "run-001",
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "single_attempt",
                        "scenario": "color-locks",
                        "trials": [
                            {
                                "trial_index": 1,
                                "goal_achieved": True,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [],
                                        },
                                        "trace": [
                                            {
                                                "type": "tool_execution",
                                                "tool_name": "look",
                                                "retry_index": 0,
                                            },
                                            {
                                                "type": "tool_execution",
                                                "tool_name": "take",
                                                "retry_index": 0,
                                            },
                                            {
                                                "type": "tool_execution",
                                                "tool_name": "take",
                                                "retry_index": 0,
                                            },
                                        ],
                                    },
                                ],
                            },
                            {
                                "trial_index": 2,
                                "goal_achieved": False,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [],
                                        },
                                        "trace": [],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        },
    ]

    analysis = analyze_efficiency(run_sources)

    metrics = analysis["systems"][
        "minimal / nova-lite / single_attempt"
    ]["by_scenario"]["color-locks"]

    assert metrics["by_tool"] == {
        "take": 1.0,
        "look": 0.5,
    }
    assert metrics["tool_executions_per_trial"] == 1.5


def test_efficiency_global_metrics_are_weighted_by_trials() -> None:
    run_sources = [
        {
            "run_id": "run-001",
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "single_attempt",
                        "scenario": "scenario-a",
                        "trials": [
                            {
                                "trial_index": 1,
                                "goal_achieved": True,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [],
                                        },
                                        "trace": [
                                            {
                                                "type": "llm_call",
                                                "purpose": "agent",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 80,
                                                    "output_tokens": 20,
                                                },
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "single_attempt",
                        "scenario": "scenario-b",
                        "trials": [
                            {
                                "trial_index": trial_index,
                                "goal_achieved": False,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [],
                                        },
                                        "trace": [
                                            {
                                                "type": "llm_call",
                                                "purpose": "agent",
                                                "retry_index": 0,
                                                "response": {
                                                    "input_tokens": 8,
                                                    "output_tokens": 2,
                                                },
                                            },
                                        ],
                                    },
                                ],
                            }
                            for trial_index in range(1, 4)
                        ],
                    },
                ],
            },
        },
    ]

    analysis = analyze_efficiency(run_sources)

    system = analysis["systems"][
        "minimal / nova-lite / single_attempt"
    ]

    assert system["by_scenario"]["scenario-a"]["total_tokens_per_trial"] == 100.0
    assert system["by_scenario"]["scenario-b"]["total_tokens_per_trial"] == 10.0

    global_metrics = system["global"]

    assert global_metrics["trials"] == 4
    assert global_metrics["successful_trials"] == 1
    assert global_metrics["success_rate"] == 0.25
    assert global_metrics["total_tokens_per_trial"] == 32.5
    assert global_metrics["llm_calls_per_trial"] == 1.0


def test_efficiency_markdown_rounds_token_averages_instead_of_truncating() -> None:
    analysis = {
        "run_ids": ["run-001"],
        "systems": {
            "minimal / nova-lite / single_attempt": {
                "agent_config": "minimal",
                "llm_config": "nova-lite",
                "trial_config": "single_attempt",
                "by_scenario": {
                    "color-locks": {
                        "trials": 2,
                        "successful_trials": 1,
                        "success_rate": 0.5,
                        "attempts_per_trial": 1.0,
                        "attempts_per_success": 2.0,
                        "retries_per_trial": 0.0,
                        "llm_calls_per_trial": 1.0,
                        "tool_executions_per_trial": 0.0,
                        "steps_per_trial": 0.0,
                        "input_tokens_per_trial": 20.6,
                        "output_tokens_per_trial": 12.3,
                        "total_tokens_per_trial": 32.9,
                        "llm_calls_per_success": 2.0,
                        "tool_executions_per_success": 0.0,
                        "steps_per_success": 0.0,
                        "total_tokens_per_success": 65.8,
                        "by_purpose": {
                            "agent": {
                                "llm_calls_per_trial": 1.0,
                                "input_tokens_per_trial": 20.6,
                                "output_tokens_per_trial": 12.3,
                                "total_tokens_per_trial": 32.9,
                            },
                        },
                        "by_tool": {},
                    },
                },
                "global": {
                    "trials": 2,
                    "successful_trials": 1,
                    "success_rate": 0.5,
                    "attempts_per_trial": 1.0,
                    "attempts_per_success": 2.0,
                    "retries_per_trial": 0.0,
                    "llm_calls_per_trial": 1.0,
                    "tool_executions_per_trial": 0.0,
                    "steps_per_trial": 0.0,
                    "input_tokens_per_trial": 20.6,
                    "output_tokens_per_trial": 12.3,
                    "total_tokens_per_trial": 32.9,
                    "llm_calls_per_success": 2.0,
                    "tool_executions_per_success": 0.0,
                    "steps_per_success": 0.0,
                    "total_tokens_per_success": 65.8,
                    "by_purpose": {
                        "agent": {
                            "llm_calls_per_trial": 1.0,
                            "input_tokens_per_trial": 20.6,
                            "output_tokens_per_trial": 12.3,
                            "total_tokens_per_trial": 32.9,
                        },
                    },
                    "by_tool": {},
                },
            },
        },
    }

    markdown = render_markdown(analysis)

    assert "| color-locks | 2 | 1.0 | 0.0 | 1.0 | 0.0 | 0.0 | 21 | 12 | 33 |" in markdown
    assert "| color-locks | 2 | 1 | 50% | 2.0 | 66 |" in markdown


def test_efficiency_markdown_describes_only_transient_llm_retries() -> None:
    run_sources = [
        {
            "run_id": "run-001",
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "nova-lite",
                        "trial_config": "single_attempt",
                        "scenario": "color-locks",
                        "trials": [
                            {
                                "trial_index": 1,
                                "goal_achieved": True,
                                "attempts": [
                                    {
                                        "agent_result": {
                                            "steps": [],
                                        },
                                        "trace": [],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        },
    ]

    markdown = render_markdown(analyze_efficiency(run_sources))

    assert "respuesta malformada" not in markdown
    assert (
        "**Retries**: número de intentos adicionales de llamadas al LLM "
        "debidos a errores transitorios"
        in markdown
    )


def test_efficiency_analysis_is_registered_in_m3_evaluation() -> None:
    from eval.analyses import ANALYSES
    from eval.configs.evaluation_configs import M3_EVALUATION_CONFIG

    assert ANALYSES["efficiency_analysis"] is analyze_efficiency
    assert "efficiency_analysis" in M3_EVALUATION_CONFIG["analyses"]
