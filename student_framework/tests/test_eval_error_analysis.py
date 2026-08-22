from eval.analyses.error_analysis import analyze_errors, render_markdown


def _failed_trial(
    trial_index: int,
    *,
    steps: list[dict],
    answer: str = "No se alcanzó el objetivo.",
) -> dict:
    return {
        "trial_index": trial_index,
        "goal_achieved": False,
        "goal_reason": "puerta principal está cerrada",
        "attempts": [
            {
                "goal_reason": "puerta principal está cerrada",
                "agent_result": {
                    "answer": answer,
                    "steps": steps,
                    "error": None,
                },
            },
        ],
    }


def test_error_analysis_preserves_agent_config_and_separates_systems() -> None:
    run_manifest = {
        "run_id": "test-run",
        "scenario_metadata": {
            "study-with-key": {
                "difficulty": "easy",
            },
        },
    }

    run_result = {
        "results": [
            {
                "agent_config": "minimal",
                "llm_config": "llama3.1",
                "scenario": "study-with-key",
                "trials": [
                    _failed_trial(
                        1,
                        steps=[
                            {
                                "tool_name": "examine",
                                "error": "argumento inválido",
                            },
                        ],
                    ),
                ],
            },
            {
                "agent_config": "minimal_tool_repair",
                "llm_config": "llama3.1",
                "scenario": "study-with-key",
                "trials": [
                    _failed_trial(
                        1,
                        steps=[
                            {"tool_name": "look", "error": None},
                            {"tool_name": "look", "error": None},
                            {"tool_name": "look", "error": None},
                            {"tool_name": "look", "error": None},
                            {"tool_name": "look", "error": None},
                        ],
                    ),
                ],
            },
        ],
    }

    analysis = analyze_errors([
        {
            "run_id": run_manifest["run_id"],
            "manifest": run_manifest,
            "result": run_result,
        },
    ])

    assert analysis["failures_by_model"] == {
        "llama3.1": {
            "wrong_tool_use": 1,
            "planning_failure": 1,
        },
    }

    assert analysis["failures_by_system"] == {
        "minimal": {
            "llama3.1": {
                "wrong_tool_use": 1,
            },
        },
        "minimal_tool_repair": {
            "llama3.1": {
                "planning_failure": 1,
            },
        },
    }

    assert [
        failure["agent_config"]
        for failure in analysis["all_failures"]
    ] == [
        "minimal",
        "minimal_tool_repair",
    ]


def test_error_analysis_markdown_identifies_each_system() -> None:
    analysis = {
        "run_id": "test-run",
        "total_trials": 2,
        "successes": 0,
        "failures": 2,
        "coverage": "2/2 trials fallidos clasificados",
        "failures_by_mode": {
            "wrong_tool_use": 1,
            "planning_failure": 1,
        },
        "failures_by_model": {
            "llama3.1": {
                "wrong_tool_use": 1,
                "planning_failure": 1,
            },
        },
        "failures_by_system": {
            "minimal": {
                "llama3.1": {
                    "wrong_tool_use": 1,
                },
            },
            "minimal_tool_repair": {
                "llama3.1": {
                    "planning_failure": 1,
                },
            },
        },
        "failures_by_scenario": {
            "study-with-key": {
                "wrong_tool_use": 1,
                "planning_failure": 1,
            },
        },
        "examples_by_mode": {},
        "all_failures": [
            {
                "agent_config": "minimal",
                "model": "llama3.1",
                "scenario": "study-with-key",
                "difficulty": "easy",
                "trial_index": 1,
                "n_steps": 1,
                "mode": "wrong_tool_use",
                "reason": "argumento inválido",
            },
            {
                "agent_config": "minimal_tool_repair",
                "model": "llama3.1",
                "scenario": "study-with-key",
                "difficulty": "easy",
                "trial_index": 1,
                "n_steps": 5,
                "mode": "planning_failure",
                "reason": "no alcanzó el objetivo",
            },
        ],
    }

    markdown = render_markdown(analysis)

    assert "## Por sistema" in markdown
    assert "### minimal / llama3.1 (1 fallos)" in markdown
    assert "### minimal_tool_repair / llama3.1 (1 fallos)" in markdown
    assert "| 1 | minimal | llama3.1 | study-with-key |" in markdown
    assert (
        "| 1 | minimal_tool_repair | llama3.1 | study-with-key |"
        in markdown
    )


def test_error_analysis_markdown_uses_trial_counts_and_precise_percentages() -> None:
    analysis = {
        "run_id": "test-run",
        "total_trials": 320,
        "successes": 51,
        "failures": 269,
        "coverage": "269/269 trials fallidos clasificados",
        "failures_by_mode": {
            "planning_failure": 130,
        },
        "failures_by_model": {},
        "failures_by_system": {},
        "failures_by_scenario": {},
        "examples_by_mode": {},
        "all_failures": [],
    }

    markdown = render_markdown(analysis)

    assert "| Exitosos | 51 (15.9%) |" in markdown
    assert "| Fallidos | 269 (84.1%) |" in markdown
    assert "| Modo | Trials | % |" in markdown
    assert "| Modo | Runs |" not in markdown


def test_error_analysis_aggregates_trials_from_multiple_runs() -> None:
    run_sources = [
        {
            "run_id": "run-a",
            "manifest": {
                "run_id": "run-a",
                "scenario_metadata": {
                    "study-with-key": {
                        "difficulty": "easy",
                    },
                },
            },
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "llama3.1",
                        "scenario": "study-with-key",
                        "trials": [
                            _failed_trial(
                                1,
                                steps=[
                                    {
                                        "tool_name": "examine",
                                        "error": "argumento inválido",
                                    },
                                ],
                            ),
                        ],
                    },
                ],
            },
        },
        {
            "run_id": "run-b",
            "manifest": {
                "run_id": "run-b",
                "scenario_metadata": {
                    "study-with-key": {
                        "difficulty": "easy",
                    },
                },
            },
            "result": {
                "results": [
                    {
                        "agent_config": "minimal",
                        "llm_config": "llama3.1",
                        "scenario": "study-with-key",
                        "trials": [
                            _failed_trial(
                                1,
                                steps=[
                                    {
                                        "tool_name": "look",
                                        "error": None,
                                    },
                                    {
                                        "tool_name": "look",
                                        "error": None,
                                    },
                                    {
                                        "tool_name": "look",
                                        "error": None,
                                    },
                                    {
                                        "tool_name": "look",
                                        "error": None,
                                    },
                                    {
                                        "tool_name": "look",
                                        "error": None,
                                    },
                                ],
                            ),
                        ],
                    },
                ],
            },
        },
    ]

    analysis = analyze_errors(run_sources)

    assert analysis["run_ids"] == [
        "run-a",
        "run-b",
    ]
    assert analysis["total_trials"] == 2
    assert analysis["failures"] == 2
    assert analysis["failures_by_mode"] == {
        "wrong_tool_use": 1,
        "planning_failure": 1,
    }

    assert [
        failure["source_run_id"]
        for failure in analysis["all_failures"]
    ] == [
        "run-a",
        "run-b",
    ]

    assert [
        failure["trial_index"]
        for failure in analysis["all_failures"]
    ] == [
        1,
        1,
    ]

    markdown = render_markdown(analysis)

    assert "**Runs:** `run-a`, `run-b`" in markdown

    assert "| run-a | 1 |" in markdown
    assert "| run-b | 1 |" in markdown