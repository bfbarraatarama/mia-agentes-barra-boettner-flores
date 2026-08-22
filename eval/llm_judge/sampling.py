"""Muestreo reproducible de trials para evaluación cualitativa."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from eval.llm_judge.models import CaseSource, CaseSplit


RANDOM_STRATIFIED_BY_SCENARIO_METHOD = (
    "random_stratified_by_scenario_without_replacement"
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