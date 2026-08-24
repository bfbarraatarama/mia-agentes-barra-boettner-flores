"""Muestreo reproducible de trials para evaluación cualitativa."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import random
from typing import Any

from eval.llm_judge.cases import build_qualitative_case
from eval.llm_judge.models import CaseSource, CaseSplit
from eval.llm_judge.presentation import build_case_presentation


RANDOM_STRATIFIED_BY_SCENARIO_METHOD = (
    "random_stratified_by_scenario_without_replacement"
)

BALANCED_HOLDOUT_THEN_DIAGNOSTIC_DEV_METHOD = (
    "balanced_holdout_then_diagnostic_dev"
)


@dataclass(frozen=True)
class TrialCandidate:
    """Trial elegible junto con su procedencia experimental."""

    run_id: str
    agent_config: str
    llm_config: str
    trial_config: str
    scenario: str
    trial_index: int
    trial: dict[str, Any]

    @property
    def identity(
        self,
    ) -> tuple[str, str, str, str, str, int]:
        """Identidad estable del trial dentro de la evidencia primaria."""

        return (
            self.run_id,
            self.agent_config,
            self.llm_config,
            self.trial_config,
            self.scenario,
            self.trial_index,
        )


@dataclass(frozen=True)
class SampledTrial:
    """Trial seleccionado y asignado a un split cualitativo."""

    case_id: str
    split: CaseSplit
    candidate: TrialCandidate

    def case_source(self) -> CaseSource:
        """Construye la procedencia persistible del caso ciego."""

        candidate = self.candidate

        return CaseSource(
            case_id=self.case_id,
            run_id=candidate.run_id,
            agent_config=candidate.agent_config,
            llm_config=candidate.llm_config,
            trial_config=candidate.trial_config,
            scenario=candidate.scenario,
            trial_index=candidate.trial_index,
            split=self.split,
        )


def _is_selected(
    value: str,
    allowed: set[str] | None,
) -> bool:
    """Indica si un valor pertenece al filtro opcional."""

    return allowed is None or value in allowed


def collect_trial_candidates(
    run_results: dict[str, dict[str, Any]],
    *,
    agent_configs: set[str] | None = None,
    llm_configs: set[str] | None = None,
    trial_configs: set[str] | None = None,
    scenarios: set[str] | None = None,
) -> list[TrialCandidate]:
    """Recolecta trials elegibles desde uno o más runs."""

    candidates = []

    for run_id, run_result in run_results.items():
        for result in run_result["results"]:
            if not _is_selected(
                result["agent_config"],
                agent_configs,
            ):
                continue

            if not _is_selected(
                result["llm_config"],
                llm_configs,
            ):
                continue

            if not _is_selected(
                result["trial_config"],
                trial_configs,
            ):
                continue

            if not _is_selected(
                result["scenario"],
                scenarios,
            ):
                continue

            for trial in result["trials"]:
                candidates.append(TrialCandidate(
                    run_id=run_id,
                    agent_config=result["agent_config"],
                    llm_config=result["llm_config"],
                    trial_config=result["trial_config"],
                    scenario=result["scenario"],
                    trial_index=trial["trial_index"],
                    trial=trial,
                ))

    return sorted(
        candidates,
        key=lambda candidate: candidate.identity,
    )


def _candidate_system(
    candidate: TrialCandidate,
) -> tuple[str, str, str]:
    """Identifica la condición de sistema de un candidato."""

    return (
        candidate.agent_config,
        candidate.llm_config,
        candidate.trial_config,
    )


def _presentation_word_count(
    candidate: TrialCandidate,
) -> int:
    """Mide la longitud de la presentación canónica del trial."""

    case = build_qualitative_case(
        candidate.trial,
        case_id="sampling-length",
    )
    presentation = build_case_presentation(case)

    return len(presentation.text.split())


@dataclass(frozen=True)
class DiagnosticCandidate:
    """Features observables utilizadas para seleccionar casos de dev."""

    candidate: TrialCandidate
    words: int
    success: bool
    has_plan: bool
    has_summary: bool
    multi_attempt: bool
    q1_4_trigger_kinds: frozenset[str]


def _diagnostic_candidate(
    candidate: TrialCandidate,
) -> DiagnosticCandidate:
    """Construye features diagnósticas desde la vista cualitativa canónica."""

    case = build_qualitative_case(
        candidate.trial,
        case_id="sampling-diagnostics",
    )
    presentation = build_case_presentation(case)

    contexts = [
        context
        for attempt in case.attempts
        for iteration in attempt.iterations
        for context in (
            iteration.context_before_decision
            + iteration.context_after_decision
        )
    ]

    q1_4 = case.criteria_applicability["Q1.4"]
    trigger_kinds = frozenset(
        component.kind
        for trigger in q1_4.triggers
        for component in trigger.components
    )

    return DiagnosticCandidate(
        candidate=candidate,
        words=len(presentation.text.split()),
        success=bool(candidate.trial["goal_achieved"]),
        has_plan=any(
            context.kind == "plan"
            for context in contexts
        ),
        has_summary=any(
            context.kind == "summary"
            for context in contexts
        ),
        multi_attempt=len(case.attempts) > 1,
        q1_4_trigger_kinds=trigger_kinds,
    )


def _reduce_diagnostic_pool(
    candidates: list[DiagnosticCandidate],
) -> list[DiagnosticCandidate]:
    """Conserva el caso más corto por combinación diagnóstica equivalente."""

    best_by_signature: dict[
        tuple[bool, bool, frozenset[str]],
        DiagnosticCandidate,
    ] = {}

    for candidate in candidates:
        signature = (
            candidate.success,
            candidate.multi_attempt,
            candidate.q1_4_trigger_kinds,
        )
        current = best_by_signature.get(signature)

        if current is None or (
            candidate.words,
            candidate.candidate.identity,
        ) < (
            current.words,
            current.candidate.identity,
        ):
            best_by_signature[signature] = candidate

    return sorted(
        best_by_signature.values(),
        key=lambda candidate: (
            candidate.words,
            candidate.candidate.identity,
        ),
    )


def select_diagnostic_dev_candidates(
    candidates: list[TrialCandidate],
    *,
    excluded_identities: set[
        tuple[str, str, str, str, str, int]
    ],
    successes: int,
    require_plan_for_agent_configs: set[str],
    require_summary_for_agent_configs: set[str],
    require_multi_attempt: bool,
) -> list[TrialCandidate]:
    """Selecciona un dev dirigido luego de excluir el holdout."""

    remaining = [
        candidate
        for candidate in candidates
        if candidate.identity not in excluded_identities
    ]

    if not remaining:
        raise ValueError(
            "No quedan trials disponibles para seleccionar dev."
        )

    diagnostic = [
        _diagnostic_candidate(candidate)
        for candidate in remaining
    ]

    systems = sorted({
        _candidate_system(candidate.candidate)
        for candidate in diagnostic
    })

    if not 0 <= successes <= len(systems):
        raise ValueError(
            "successes debe estar entre 0 y la cantidad de sistemas."
        )

    candidates_by_system: dict[
        tuple[str, str, str],
        list[DiagnosticCandidate],
    ] = {}

    for candidate in diagnostic:
        system = _candidate_system(candidate.candidate)
        agent_config = candidate.candidate.agent_config

        if (
            agent_config in require_plan_for_agent_configs
            and not candidate.has_plan
        ):
            continue

        if (
            agent_config in require_summary_for_agent_configs
            and not candidate.has_summary
        ):
            continue

        candidates_by_system.setdefault(
            system,
            [],
        ).append(candidate)

    reduced_by_system = {}

    for system in systems:
        system_candidates = candidates_by_system.get(
            system,
            [],
        )

        if not system_candidates:
            raise ValueError(
                "No hay candidatos de dev que satisfagan los requisitos "
                f"para el sistema {system!r}."
            )

        reduced_by_system[system] = _reduce_diagnostic_pool(
            system_candidates
        )

    valid_selections = []

    for selection in product(
        *[
            reduced_by_system[system]
            for system in systems
        ]
    ):
        if sum(
            candidate.success
            for candidate in selection
        ) != successes:
            continue

        if (
            require_multi_attempt
            and not any(
                candidate.multi_attempt
                for candidate in selection
            )
        ):
            continue

        trigger_kinds = frozenset().union(
            *[
                candidate.q1_4_trigger_kinds
                for candidate in selection
            ]
        )
        total_words = sum(
            candidate.words
            for candidate in selection
        )

        valid_selections.append((
            -len(trigger_kinds),
            total_words,
            tuple(
                candidate.candidate.identity
                for candidate in selection
            ),
            selection,
        ))

    if not valid_selections:
        raise ValueError(
            "No existe una selección de dev que satisfaga "
            "las restricciones configuradas."
        )

    _, _, _, selected = min(valid_selections)

    return [
        candidate.candidate
        for candidate in selected
    ]


def select_balanced_holdout_candidates(
    candidates: list[TrialCandidate],
    *,
    seed: int,
    shortest_per_cell: int,
    cases_per_system: int,
    successes: int,
) -> list[TrialCandidate]:
    """Selecciona holdout balanceado desde candidatos cortos por celda."""

    if not candidates:
        raise ValueError(
            "No hay trials elegibles para seleccionar el holdout."
        )

    if shortest_per_cell < 1:
        raise ValueError(
            "shortest_per_cell debe ser al menos 1."
        )

    if cases_per_system < 1:
        raise ValueError(
            "cases_per_system debe ser al menos 1."
        )

    systems = sorted({
        _candidate_system(candidate)
        for candidate in candidates
    })
    scenarios = sorted({
        candidate.scenario
        for candidate in candidates
    })
    holdout_size = len(scenarios)

    if len(systems) * cases_per_system != holdout_size:
        raise ValueError(
            "La cantidad de escenarios debe coincidir con "
            "systems × cases_per_system."
        )

    if not 0 <= successes <= holdout_size:
        raise ValueError(
            "successes debe estar entre 0 y la cantidad de escenarios."
        )

    word_counts = {
        candidate.identity: _presentation_word_count(candidate)
        for candidate in candidates
    }

    candidates_by_cell: dict[
        tuple[tuple[str, str, str], str],
        list[TrialCandidate],
    ] = {}

    for candidate in candidates:
        key = (
            _candidate_system(candidate),
            candidate.scenario,
        )
        candidates_by_cell.setdefault(key, []).append(candidate)

    eligible_by_stratum: dict[
        tuple[tuple[str, str, str], str, bool],
        list[TrialCandidate],
    ] = {}

    for system in systems:
        for scenario in scenarios:
            cell_candidates = candidates_by_cell.get(
                (system, scenario),
                [],
            )

            if len(cell_candidates) < shortest_per_cell:
                raise ValueError(
                    f"La celda {system!r} / {scenario!r} tiene "
                    f"{len(cell_candidates)} trials, pero se requieren "
                    f"{shortest_per_cell} para el corte por longitud."
                )

            shortest = sorted(
                cell_candidates,
                key=lambda candidate: (
                    word_counts[candidate.identity],
                    candidate.identity,
                ),
            )[:shortest_per_cell]

            for candidate in shortest:
                stratum = (
                    system,
                    scenario,
                    bool(candidate.trial["goal_achieved"]),
                )
                eligible_by_stratum.setdefault(
                    stratum,
                    [],
                ).append(candidate)

    valid_assignments = []
    system_counts = {
        system: 0
        for system in systems
    }
    assignment: list[
        tuple[str, tuple[str, str, str], bool]
    ] = []

    def search(
        scenario_index: int,
        success_count: int,
    ) -> None:
        remaining = len(scenarios) - scenario_index

        if success_count > successes:
            return

        if success_count + remaining < successes:
            return

        if scenario_index == len(scenarios):
            if (
                success_count == successes
                and all(
                    count == cases_per_system
                    for count in system_counts.values()
                )
            ):
                valid_assignments.append(tuple(assignment))

            return

        scenario = scenarios[scenario_index]

        for system in systems:
            if system_counts[system] >= cases_per_system:
                continue

            for success in (False, True):
                stratum = (
                    system,
                    scenario,
                    success,
                )

                if stratum not in eligible_by_stratum:
                    continue

                system_counts[system] += 1
                assignment.append(
                    (scenario, system, success)
                )

                search(
                    scenario_index + 1,
                    success_count + int(success),
                )

                assignment.pop()
                system_counts[system] -= 1

    search(0, 0)

    if not valid_assignments:
        raise ValueError(
            "No existe una asignación de holdout que satisfaga "
            "las restricciones configuradas."
        )

    rng = random.Random(seed)
    selected_assignment = rng.choice(valid_assignments)
    selected_candidates = []

    for scenario, system, success in selected_assignment:
        stratum_candidates = sorted(
            eligible_by_stratum[
                (system, scenario, success)
            ],
            key=lambda candidate: candidate.identity,
        )

        selected_candidates.append(
            rng.choice(stratum_candidates)
        )

    return selected_candidates


def sample_holdout_then_dev(
    candidates: list[TrialCandidate],
    *,
    seed: int,
    holdout_shortest_per_cell: int,
    holdout_cases_per_system: int,
    holdout_successes: int,
    dev_successes: int,
    dev_require_plan_for_agent_configs: set[str],
    dev_require_summary_for_agent_configs: set[str],
    dev_require_multi_attempt: bool,
) -> list[SampledTrial]:
    """Selecciona primero holdout y luego dev sobre la población restante."""

    holdout = select_balanced_holdout_candidates(
        candidates,
        seed=seed,
        shortest_per_cell=holdout_shortest_per_cell,
        cases_per_system=holdout_cases_per_system,
        successes=holdout_successes,
    )

    holdout_identities = {
        candidate.identity
        for candidate in holdout
    }

    dev = select_diagnostic_dev_candidates(
        candidates,
        excluded_identities=holdout_identities,
        successes=dev_successes,
        require_plan_for_agent_configs=(
            dev_require_plan_for_agent_configs
        ),
        require_summary_for_agent_configs=(
            dev_require_summary_for_agent_configs
        ),
        require_multi_attempt=dev_require_multi_attempt,
    )

    selected = [
        (candidate, "holdout")
        for candidate in holdout
    ] + [
        (candidate, "dev")
        for candidate in dev
    ]

    return [
        SampledTrial(
            case_id=f"qc-{case_index:03d}",
            split=split,
            candidate=candidate,
        )
        for case_index, (candidate, split) in enumerate(
            selected,
            start=1,
        )
    ]


def sample_trials_by_scenario(
    candidates: list[TrialCandidate],
    *,
    seed: int,
    cases_per_scenario: int,
    dev_per_scenario: int,
) -> list[SampledTrial]:
    """Muestrea y asigna trials a dev/holdout por escenario."""

    if cases_per_scenario < 2:
        raise ValueError(
            "cases_per_scenario debe ser al menos 2."
        )

    if not 1 <= dev_per_scenario < cases_per_scenario:
        raise ValueError(
            "dev_per_scenario debe ser al menos 1 y menor que "
            "cases_per_scenario."
        )

    if not candidates:
        raise ValueError(
            "No hay trials elegibles para muestrear."
        )

    candidates_by_scenario: dict[str, list[TrialCandidate]] = {}

    for candidate in candidates:
        candidates_by_scenario.setdefault(
            candidate.scenario,
            [],
        ).append(candidate)

    rng = random.Random(seed)
    selected: list[tuple[TrialCandidate, CaseSplit]] = []

    for scenario in sorted(candidates_by_scenario):
        scenario_candidates = sorted(
            candidates_by_scenario[scenario],
            key=lambda candidate: candidate.identity,
        )

        if len(scenario_candidates) < cases_per_scenario:
            raise ValueError(
                f"El escenario {scenario!r} tiene "
                f"{len(scenario_candidates)} trials elegibles, pero se "
                f"requieren {cases_per_scenario}."
            )

        scenario_sample = rng.sample(
            scenario_candidates,
            k=cases_per_scenario,
        )

        for index, candidate in enumerate(scenario_sample):
            split: CaseSplit = (
                "dev"
                if index < dev_per_scenario
                else "holdout"
            )

            selected.append(
                (candidate, split)
            )

    rng.shuffle(selected)

    return [
        SampledTrial(
            case_id=f"qc-{case_index:03d}",
            split=split,
            candidate=candidate,
        )
        for case_index, (candidate, split) in enumerate(
            selected,
            start=1,
        )
    ]