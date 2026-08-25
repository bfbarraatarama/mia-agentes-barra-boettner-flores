"""Interfaz local para anotación humana de casos cualitativos."""

from __future__ import annotations

import html
import json
import re
import sys
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

# Permite ejecutar exactamente:
#     python eval/llm_judge/annotate.py
REPO_ROOT = Path(__file__).resolve().parents[2]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from eval.llm_judge.annotations import (
    HUMAN_ANNOTATION_SCHEMA_VERSION,
    create_annotator,
    delete_annotator,
    delete_human_annotation,
    list_annotators,
    save_human_annotation,
    update_human_annotation,
)
from eval.llm_judge.configs.dataset_configs import DATASET_CONFIG
from eval.llm_judge.models import (
    HumanAnnotation,
    HumanCriterionAnnotation,
)
from eval.llm_judge.persistence import RESULTS_DIR
from eval.llm_judge.reviewer import (
    ReviewCase,
    load_review_cases,
)
from eval.llm_judge.rubric import (
    BOUNDARY_RULES,
    CRITERIA_BY_ID,
    CRITERION_IDS,
    DIMENSION_DESCRIPTION,
    DIMENSION_ID,
    DIMENSION_NAME,
    MATERIALITY_RULE,
    RUBRIC_VERSION,
)


HOST = "127.0.0.1"
PORT = 8765


def _query_value(
    query: dict[str, list[str]],
    key: str,
    default: str,
) -> str:
    values = query.get(key)

    if not values:
        return default

    return values[0]


def _default_annotator_id(
    dataset_id: str,
) -> str:
    annotators = list_annotators(
        dataset_id,
        results_dir=RESULTS_DIR,
    )

    if annotators:
        return annotators[0]

    return ""


def _load_selected_cases(
    dataset_id: str,
    annotator_id: str,
    split: str,
    status: str = "all",
) -> list[ReviewCase]:
    selected_split = None if split == "all" else split

    review_cases = load_review_cases(
        dataset_id,
        annotator_id,
        split=selected_split,
        results_dir=RESULTS_DIR,
    )

    if status == "pending":
        return [
            review_case
            for review_case in review_cases
            if not review_case.completed
        ]

    if status in {
        "completed",
        "annotated",
    }:
        return [
            review_case
            for review_case in review_cases
            if review_case.completed
        ]
    return review_cases


def _selected_case(
    review_cases: list[ReviewCase],
    case_id: str | None,
) -> ReviewCase | None:
    if not review_cases:
        return None

    if case_id is None:
        return review_cases[0]

    for review_case in review_cases:
        if review_case.case_id == case_id:
            return review_case

    return review_cases[0]


def _annotation_from_form(
    review_case: ReviewCase,
    annotator_id: str,
    form: dict[str, list[str]],
) -> HumanAnnotation:
    criteria = {}

    for criterion_id in CRITERION_IDS:
        applicability = (
            review_case.case.criteria_applicability[
                criterion_id
            ]
        )

        if not applicability.applicable:
            continue

        verdict = _query_value(
            form,
            f"{criterion_id}.verdict",
            "",
        )
        reason = _query_value(
            form,
            f"{criterion_id}.reason",
            "",
        ).strip()
        evidence_refs = [
            value
            for value in form.get(
                f"{criterion_id}.evidence_refs",
                [],
            )
            if value
        ]

        started = bool(
            verdict
            or reason
            or evidence_refs
        )

        if not started:
            continue

        missing = []

        if verdict not in {
            "PASS",
            "FAIL",
        }:
            missing.append(
                "veredicto"
            )

        if not reason:
            missing.append(
                "justificación"
            )

        if not evidence_refs:
            missing.append(
                "evidencia"
            )

        if missing:
            raise ValueError(
                f"{criterion_id} está incompleto: "
                f"faltan {', '.join(missing)}."
            )

        criteria[criterion_id] = (
            HumanCriterionAnnotation(
                verdict=verdict,
                reason=reason,
                evidence_refs=evidence_refs,
            )
        )

    if not criteria:
        raise ValueError(
            "La anotación debe contener al menos "
            "un criterio completado."
        )

    return HumanAnnotation(
        schema_version=HUMAN_ANNOTATION_SCHEMA_VERSION,
        case_schema_version=review_case.case.schema_version,
        case_view_version=review_case.case.case_view_version,
        presentation_version=review_case.presentation.version,
        rubric_version=RUBRIC_VERSION,
        case_id=review_case.case_id,
        annotator_id=annotator_id,
        criteria=criteria,
    )


def _rubric_overview_html() -> str:
    """Renderiza las reglas comunes de la rúbrica canónica."""

    boundary_rules_html = "".join(
        f"<li>{html.escape(rule)}</li>"
        for rule in BOUNDARY_RULES
    )

    return f"""
    <details class="rubric-reference">
      <summary>
        {DIMENSION_ID} — {html.escape(DIMENSION_NAME)}
      </summary>

      <p>
        {html.escape(DIMENSION_DESCRIPTION)}
      </p>

      <p>
        <strong>Regla de materialidad:</strong>
        {html.escape(MATERIALITY_RULE)}
      </p>

      <p>
        <strong>Reglas de frontera:</strong>
      </p>

      <ul>
        {boundary_rules_html}
      </ul>
    </details>
    """


def _attempt_index_from_ref(
    evidence_ref: str,
) -> int:
    match = re.fullmatch(
        r"a(\d+)(?:\..+)?",
        evidence_ref,
    )

    if match is None:
        raise ValueError(
            f"Referencia de evidencia inválida: {evidence_ref!r}."
        )

    return int(match.group(1))


def _iteration_position_from_ref(
    evidence_ref: str,
) -> tuple[int, int]:
    match = re.fullmatch(
        r"a(\d+)\.i(\d+)(?:\..+)?",
        evidence_ref,
    )

    if match is None:
        raise ValueError(
            "El trigger de Q1.4 no referencia una iteración válida: "
            f"{evidence_ref!r}."
        )

    return (
        int(match.group(1)),
        int(match.group(2)),
    )


def _q1_4_trigger_ui_data(
    review_case: ReviewCase,
) -> list[dict[str, object]]:
    """Deriva una entrada humana por oportunidad de adaptación."""

    presentation = json.loads(
        review_case.presentation.text
    )
    q1_4 = presentation.get(
        "q1_4_applicability",
        {},
    )
    triggers = q1_4.get(
        "triggers",
        [],
    )
    multiple_attempts = (
        len(review_case.case.attempts) > 1
    )
    items = []

    for trigger_index, trigger in enumerate(
        triggers,
        start=1,
    ):
        trigger_id = f"D{trigger_index}"
        target_ref = str(
            trigger.get(
                "target_ref",
                "",
            )
        )
        components = trigger.get(
            "components",
            [],
        )

        if not target_ref or not components:
            raise ValueError(
                "Un trigger agrupado de Q1.4 debe contener "
                "target y componentes."
            )

        evidence_refs = []
        marker_refs = []
        has_continuation = False
        error_refs = []
        repetition_refs = []

        for component in components:
            kind = component.get(
                "kind"
            )
            component_refs = [
                str(evidence_ref)
                for evidence_ref in component.get(
                    "evidence_refs",
                    [],
                )
            ]

            if not component_refs:
                raise ValueError(
                    "Un componente de Q1.4 debe contener evidencia."
                )

            evidence_refs.extend(
                component_refs
            )

            if kind == "attempt_continuation":
                has_continuation = True

            elif kind == "error_before_later_decision":
                error_refs.extend(
                    component_refs
                )
                marker_refs.extend(
                    component_refs
                )

            elif kind == "consecutive_exact_repetition":
                if len(component_refs) < 2:
                    raise ValueError(
                        "Una repetición consecutiva de Q1.4 debe "
                        "contener al menos dos acciones."
                    )

                repetition_refs = component_refs
                marker_refs.extend(
                    component_refs
                )

            else:
                raise ValueError(
                    "Tipo de componente de Q1.4 desconocido: "
                    f"{kind!r}."
                )

        label_parts = []

        if has_continuation:
            label_parts.append(
                "Nuevo attempt"
            )

        if error_refs:
            label_parts.append(
                (
                    "1 error previo"
                    if len(error_refs) == 1
                    else f"{len(error_refs)} errores previos"
                )
            )

        if repetition_refs:
            if len(repetition_refs) == 2:
                label_parts.append(
                    "Repetición consecutiva"
                )
            else:
                label_parts.append(
                    "Repetición consecutiva · "
                    f"{len(repetition_refs)} ejecuciones iguales"
                )

        target_attempt = _attempt_index_from_ref(
            target_ref
        )
        target_iteration_match = re.fullmatch(
            r"a(\d+)\.i(\d+)",
            target_ref,
        )

        if target_iteration_match is not None:
            target_iteration = int(
                target_iteration_match.group(2)
            )

            if multiple_attempts:
                opportunity_location = (
                    f"Attempt {target_attempt} · "
                    f"iter. {target_iteration}"
                )
            else:
                opportunity_location = (
                    f"Iter. {target_iteration}"
                )
        else:
            opportunity_location = (
                f"Attempt {target_attempt}"
            )

        episode_location = None

        if repetition_refs:
            start_attempt, start_iteration = (
                _iteration_position_from_ref(
                    repetition_refs[0]
                )
            )
            end_attempt, end_iteration = (
                _iteration_position_from_ref(
                    repetition_refs[-1]
                )
            )

            if start_attempt == end_attempt:
                if multiple_attempts:
                    episode_location = (
                        f"Attempt {start_attempt} · "
                        f"iter. {start_iteration} → {end_iteration}"
                    )
                else:
                    episode_location = (
                        f"Iter. {start_iteration} → {end_iteration}"
                    )
            else:
                episode_location = (
                    f"Attempt {start_attempt} · iter. "
                    f"{start_iteration} → Attempt {end_attempt} · "
                    f"iter. {end_iteration}"
                )

            target = repetition_refs[1]

        else:
            target = (
                error_refs[0]
                if error_refs
                else f"attempt-{target_attempt}"
            )

        unique_evidence_refs = tuple(
            dict.fromkeys(
                evidence_refs
            )
        )
        unique_marker_refs = tuple(
            dict.fromkeys(
                marker_refs
            )
        )

        items.append({
            "id": trigger_id,
            "label": " · ".join(
                label_parts
            ),
            "location": opportunity_location,
            "episode_location": episode_location,
            "target": target,
            "evidence_refs": unique_evidence_refs,
            "marker_refs": unique_marker_refs,
            "marker_attempt": (
                target_attempt
                if has_continuation
                else None
            ),
        })

    return items


def _criterion_html(
    review_case: ReviewCase,
    criterion_id: str,
    *,
    active: bool,
) -> str:
    criterion = CRITERIA_BY_ID[criterion_id]
    applicability = (
        review_case.case.criteria_applicability[
            criterion_id
        ]
    )
    applicable = applicability.applicable
    classes = (
        "criterion-panel active"
        if active
        else "criterion-panel"
    )

    existing = None

    if review_case.annotation is not None:
        existing = review_case.annotation.criteria.get(
            criterion_id
        )

    verdict = (
        existing.verdict
        if existing
        else ""
    )
    reason = (
        existing.reason
        if existing
        else ""
    )

    guidance_html = ""

    if criterion.guidance:
        guidance_items = "".join(
            f"<li>{html.escape(item)}</li>"
            for item in criterion.guidance
        )
        guidance_html = f"""
        <div class="criterion-guidance">
          <strong>Aclaraciones:</strong>
          <ul>
            {guidance_items}
          </ul>
        </div>
        """

    applicability_html = ""

    if (
        criterion.applicability
        == "conditional"
    ):
        triggers_html = "".join(
            (
                "<li>"
                f"<strong>{html.escape(trigger)}</strong> "
                f"{html.escape(explanation)}"
                "</li>"
            )
            for trigger, explanation
            in criterion.applicability_triggers
        )
        notes_html = "".join(
            f"<li>{html.escape(note)}</li>"
            for note
            in criterion.applicability_notes
        )
        applicability_reason = (
            applicability.reason
            or ""
        )
        applicability_status = (
            "APLICA"
            if applicable
            else "N/A"
        )
        reason_html = (
            (
                " "
                + html.escape(
                    applicability_reason
                )
            )
            if applicability_reason
            else ""
        )

        applicability_html = f"""
        <details
          class="criterion-applicability"
        >
          <summary>
            Aplicabilidad de {criterion_id}
          </summary>

          <p>
            {html.escape(
                criterion.applicability_description
                or ""
            )}
          </p>

          <p>
            <strong>
              Estado en este caso:
              {applicability_status}
            </strong>
            {reason_html}
          </p>

          <p>
            <strong>Tipos de disparador:</strong>
          </p>

          <ul>
            {triggers_html}
          </ul>

          <p>
            <strong>Notas:</strong>
          </p>

          <ul>
            {notes_html}
          </ul>
        </details>
        """

    if applicable:
        annotation_html = f"""
        <div class="verdict">
          <label>
            <input
              type="radio"
              name="{criterion_id}.verdict"
              value="PASS"
              {" checked" if verdict == "PASS" else ""}
            >
            PASS
          </label>

          <label>
            <input
              type="radio"
              name="{criterion_id}.verdict"
              value="FAIL"
              {" checked" if verdict == "FAIL" else ""}
            >
            FAIL
          </label>
        </div>

        <label>
          Justificación
          <textarea
            name="{criterion_id}.reason"
          >{html.escape(reason)}</textarea>
        </label>

        <p class="evidence-hint">
          Seleccioná la evidencia directamente en el
          panel izquierdo.
        </p>
        """
    else:
        annotation_html = """
        <p class="criterion-na">
          Este criterio no se anota en este caso.
        </p>
        """

    return f"""
    <section
      class="{classes}"
      data-criterion="{criterion_id}"
      data-applicable="{"true" if applicable else "false"}"
    >
      <h3>
        {criterion_id} — {html.escape(criterion.name)}
      </h3>

      <p>
        {html.escape(criterion.question)}
      </p>

      <details>
        <summary>Definición PASS / FAIL</summary>
        <p>
          <strong>PASS:</strong>
          {html.escape(criterion.pass_description)}
        </p>
        <p>
          <strong>FAIL:</strong>
          {html.escape(criterion.fail_description)}
        </p>
      </details>

      {guidance_html}

      {applicability_html}

      {annotation_html}
    </section>
    """


def _q1_4_auxiliary_html(
    review_case: ReviewCase,
) -> str:
    """Renderiza la navegación auxiliar de disparadores de Q1.4."""

    applicability = (
        review_case.case.criteria_applicability[
            "Q1.4"
        ]
    )

    if not applicability.applicable:
        return ""

    trigger_items = _q1_4_trigger_ui_data(
        review_case
    )

    if not trigger_items:
        return ""

    trigger_rows = "".join(
        (
            '<button type="button" '
            'class="q14-trigger-link" '
            f'data-trigger-id="{item["id"]}" '
            f'data-trigger-target="{html.escape(str(item["target"]))}" '
            'data-trigger-refs="'
            + html.escape(
                json.dumps(
                    item["evidence_refs"],
                    ensure_ascii=False,
                ),
                quote=True,
            )
            + '">'
            "<strong>"
            f'Disparador {index} · {html.escape(str(item["label"]))}'
            "</strong>"
            '<span class="q14-trigger-location">'
            "<strong>Oportunidad de adaptación:</strong> "
            f'{html.escape(str(item["location"]))}'
            "</span>"
            + (
                (
                    '<span class="q14-trigger-location">'
                    "<strong>Episodio:</strong> "
                    f'{html.escape(str(item["episode_location"]))}'
                    "</span>"
                )
                if item["episode_location"] is not None
                else ""
            )
            + "</button>"
        )
        for index, item in enumerate(
            trigger_items,
            start=1,
        )
    )

    return f"""
    <section class="q14-auxiliary q14-detected-triggers">
      <p>
        <strong>
          Disparadores detectados ({len(trigger_items)})
        </strong>
      </p>

      <p class="q14-trigger-disclaimer">
        Estos disparadores determinan que Q1.4 debe evaluarse;
        no implican por sí mismos PASS ni FAIL.
      </p>

      <div class="q14-trigger-list">
        {trigger_rows}
      </div>
    </section>
    """


def _evidence_cards_html(
    review_case: ReviewCase,
) -> str:
    data = json.loads(
        review_case.presentation.text
    )
    iterations_by_ref = {
        str(iteration["ref"]): iteration
        for attempt in data.get("attempts", [])
        for iteration in attempt.get("iterations", [])
        if iteration.get("ref")
    }
    applicable = tuple(
        criterion_id
        for criterion_id in CRITERION_IDS
        if review_case.case.criteria_applicability[
            criterion_id
        ].applicable
    )
    selected = {
        criterion_id: set()
        for criterion_id in applicable
    }
    trigger_markers_by_ref: dict[str, list[str]] = {}
    attempt_trigger_markers: dict[int, list[str]] = {}

    for item in _q1_4_trigger_ui_data(review_case):
        trigger_id = str(item["id"])

        for evidence_ref in item["marker_refs"]:
            trigger_markers_by_ref.setdefault(
                str(evidence_ref),
                [],
            ).append(trigger_id)

        marker_attempt = item["marker_attempt"]

        if marker_attempt is not None:
            attempt_trigger_markers.setdefault(
                int(marker_attempt),
                [],
            ).append(trigger_id)

    if review_case.annotation is not None:
        for criterion_id, annotation in (
            review_case.annotation.criteria.items()
        ):
            selected[criterion_id] = set(
                annotation.evidence_refs
            )

    def inputs(
        evidence_ref: str,
    ) -> str:
        return "".join(
            (
                '<input '
                'class="evidence-checkbox" '
                'type="checkbox" '
                'hidden '
                'form="annotation-form" '
                f'name="{criterion_id}.evidence_refs" '
                f'value="{html.escape(evidence_ref)}" '
                f'data-criterion="{criterion_id}"'
                f'{" checked" if evidence_ref in selected[criterion_id] else ""}'
                ">"
            )
            for criterion_id in applicable
        )

    def trigger_markers(
        trigger_ids: list[str] | tuple[str, ...],
    ) -> str:
        return "".join(
            (
                '<span class="q14-trigger-marker" '
                f'data-trigger-id="{html.escape(trigger_id)}">'
                f"Q1.4 · {html.escape(trigger_id)}"
                "</span>"
            )
            for trigger_id in trigger_ids
        )

    def card(
        evidence_ref: str,
        card_type: str,
        label: str,
        title: str,
        body: str,
    ) -> str:
        return f"""
        <article
          class="evidence-card evidence-{card_type}"
          data-evidence-ref="{html.escape(evidence_ref)}"
          tabindex="0"
          role="button"
        >
          {inputs(evidence_ref)}

          <header class="evidence-card-header">
            <strong>
              {html.escape(title)}
            </strong>

            <span class="evidence-meta">
              {trigger_markers(
                  trigger_markers_by_ref.get(
                      evidence_ref,
                      [],
                  )
              )}
              <span class="evidence-ref">
                {html.escape(evidence_ref)}
              </span>
              <span class="evidence-kind">
                {label}
              </span>
              <span class="evidence-mark">
                ○
              </span>
            </span>
          </header>

          <div class="evidence-body">
            {body}
          </div>
        </article>
        """

    def tool_line(
        label: str,
        call: dict | None,
    ) -> str:
        if call is None:
            return (
                f"<div><strong>{label}:</strong> "
                "no disponible</div>"
            )

        arguments = json.dumps(
            call.get("arguments"),
            ensure_ascii=False,
            sort_keys=True,
        )
        raw = call.get("arguments_raw")
        raw_html = (
            '<div class="raw-arguments">'
            "raw: "
            f"<code>{html.escape(str(raw))}</code>"
            "</div>"
            if raw is not None
            else ""
        )

        return (
            f"<div><strong>{label}:</strong> "
            f"<code>{html.escape(str(call.get('tool', '')))}</code> "
            f"<code>{html.escape(arguments)}</code>"
            f"{raw_html}</div>"
        )

    def _action_body_html(
        action: dict,
    ) -> str:
        body = tool_line(
            "Propuesta",
            action.get("proposed_action"),
        )
        execution = action.get("execution")

        if execution is None:
            return (
                body
                + '<div class="muted">'
                "La acción no llegó a ejecutarse."
                "</div>"
            )

        if execution.get("differs_from_proposal"):
            body += (
                '<span class="repair-badge">'
                "MODIFICADA"
                "</span>"
            )

        body += tool_line(
            "Ejecución",
            execution.get("action"),
        )
        observation = (
            execution.get("observation")
            or {}
        )
        observation_class = (
            "observation observation-error"
            if observation.get("is_error")
            else "observation"
        )
        body += (
            f'<div class="{observation_class}">'
            "<strong>Observación:</strong> "
            '<span class="evidence-text">'
            + html.escape(str(
                observation.get("content", "")
            ))
            + "</span></div>"
        )

        if observation.get("error"):
            body += (
                '<div class="error-text">'
                + html.escape(str(
                    observation["error"]
                ))
                + "</div>"
            )

        return body

    def preserved_round_html(
        round_ref: str,
        position: int,
    ) -> str:
        iteration = iterations_by_ref.get(round_ref)

        if iteration is None:
            raise ValueError(
                "Un summary referencia una ronda preservada "
                f"inexistente: {round_ref!r}."
            )

        assistant_content = iteration.get(
            "assistant_content"
        )
        assistant_html = (
            '<div class="evidence-text">'
            + html.escape(str(assistant_content))
            + "</div>"
            if assistant_content is not None
            else (
                '<div class="muted">'
                "Sin contenido textual del assistant."
                "</div>"
            )
        )
        action_blocks = "".join(
            (
                '<div class="preserved-round-action">'
                f"<strong>Acción {action_index}</strong>"
                + _action_body_html(action)
                + "</div>"
            )
            for action_index, action in enumerate(
                iteration.get("actions", []),
                start=1,
            )
        )

        if not action_blocks:
            action_blocks = (
                '<div class="muted">'
                "Sin acciones en esta ronda."
                "</div>"
            )

        return f"""
        <section class="preserved-round">
          <header class="preserved-round-header">
            <strong>Ronda preservada {position}</strong>
            <span class="evidence-ref">
              {html.escape(round_ref)}
            </span>
          </header>

          <div class="preserved-round-assistant">
            <strong>Assistant</strong>
            {assistant_html}
          </div>

          {action_blocks}
        </section>
        """

    rules = "".join(
        f"<li>{html.escape(str(rule))}</li>"
        for rule in data.get(
            "evidence_rules",
            [],
        )
    )
    parts = [
        f"""
        <details class="evidence-rules">
          <summary>Reglas de evidencia</summary>
          <ul>{rules}</ul>
        </details>

        <section class="task-card">
          <span class="evidence-kind">
            TAREA
          </span>
          {html.escape(str(data.get("task", "")))}
        </section>
        """
    ]
    rendered_refs: list[str] = []

    def append_internal_context(
        context: dict,
        *,
        before_decision: bool,
    ) -> None:
        context_ref = str(
            context.get("ref", "")
        )
        kind = context.get("kind")
        content = context.get("content", "")

        if kind == "plan":
            label = "PLAN"
            title = "Plan previo del agente"
        else:
            label = "CONTEXTO REDUCIDO"
            title = (
                "Contexto reducido disponible antes de la decisión"
                if before_decision
                else (
                    "Contexto reducido disponible "
                    "para decisiones posteriores"
                )
            )

        rendered_refs.append(
            context_ref
        )
        if kind == "plan":
            body = (
                '<div class="internal-context-note">'
                "Estrategia previa del agente; "
                "no es una observación del mundo."
                "</div>"
                '<div class="evidence-text">'
                + html.escape(str(content))
                + "</div>"
            )
        else:
            preserved_refs = context.get(
                "preserved_raw_round_refs",
                [],
            )

            if not isinstance(preserved_refs, list):
                raise ValueError(
                    "Las rondas preservadas de un summary deben "
                    "estar representadas como una lista de refs."
                )

            preserved_html = "".join(
                preserved_round_html(
                    str(round_ref),
                    position,
                )
                for position, round_ref in enumerate(
                    preserved_refs,
                    start=1,
                )
            )

            if not preserved_html:
                preserved_html = (
                    '<div class="muted">'
                    "No quedaron rondas recientes preservadas en crudo."
                    "</div>"
                )

            body = (
                '<div class="internal-context-note">'
                "Contexto realmente disponible para decisiones posteriores: "
                "resumen sintetizado más las rondas recientes indicadas "
                "como preservadas en crudo. No es una observación del mundo."
                "</div>"
                '<div class="internal-context-section-title">'
                "Resumen sintetizado"
                "</div>"
                '<div class="evidence-text">'
                + html.escape(str(content))
                + "</div>"
                '<div class="internal-context-section-title">'
                "Rondas preservadas en crudo"
                "</div>"
                + preserved_html
            )

        parts.append(card(
            context_ref,
            "internal-context",
            label,
            title,
            body,
        ))

    for attempt in data.get(
        "attempts",
        [],
    ):
        attempt_index = attempt.get(
            "attempt_index"
        )
        parts.append(
            f'<h3 class="attempt-heading" id="attempt-{attempt_index}">'
            f"Attempt {attempt_index}"
            + trigger_markers(
                attempt_trigger_markers.get(
                    attempt_index,
                    [],
                )
            )
            + "</h3>"
        )

        user_message = (
            attempt.get("user_message")
            or {}
        )
        user_ref = (
            user_message.get("ref")
            or f"a{attempt_index}.user_message"
        )
        rendered_refs.append(
            user_ref
        )
        parts.append(card(
            user_ref,
            "user-message",
            "USER MESSAGE",
            f"Mensaje del attempt {attempt_index}",
            (
                '<div class="evidence-text">'
                + html.escape(str(
                    user_message.get(
                        "content",
                        "",
                    )
                ))
                + "</div>"
            ),
        ))

        for iteration_index, iteration in enumerate(
            attempt.get(
                "iterations",
                [],
            ),
            start=1,
        ):
            iteration_ref = (
                iteration.get("ref")
                or (
                    f"a{attempt_index}."
                    f"i{iteration_index}"
                )
            )

            for context in iteration.get(
                "context_before_decision",
                [],
            ):
                append_internal_context(
                    context,
                    before_decision=True,
                )

            rendered_refs.append(
                iteration_ref
            )

            content = iteration.get(
                "assistant_content"
            )
            iteration_body = (
                '<div class="evidence-text">'
                + html.escape(str(content))
                + "</div>"
                if content is not None
                else (
                    '<div class="muted">'
                    "Sin contenido textual."
                    "</div>"
                )
            )

            parts.append(card(
                iteration_ref,
                "iteration",
                "ITERACIÓN",
                f"Iteración {iteration_index}",
                iteration_body,
            ))

            for context in iteration.get(
                "context_after_decision",
                [],
            ):
                append_internal_context(
                    context,
                    before_decision=False,
                )

            for action_index, action in enumerate(
                iteration.get(
                    "actions",
                    [],
                ),
                start=1,
            ):
                action_ref = (
                    action.get("ref")
                    or (
                        f"a{attempt_index}."
                        f"i{iteration_index}."
                        f"action{action_index}"
                    )
                )
                rendered_refs.append(
                    action_ref
                )

                action_body = _action_body_html(
                    action
                )

                parts.append(card(
                    action_ref,
                    "action",
                    "ACCIÓN",
                    (
                        f"Acción {action_index} · "
                        f"iteración {iteration_index}"
                    ),
                    action_body,
                ))

        termination = (
            attempt.get("termination")
            or {}
        )
        termination_ref = (
            termination.get("ref")
            or (
                f"a{attempt_index}."
                "termination"
            )
        )
        rendered_refs.append(
            termination_ref
        )

        termination_body = ""

        if termination.get(
            "answer"
        ) is not None:
            termination_body += (
                "<div>"
                "<strong>Respuesta:</strong> "
                '<span class="evidence-text">'
                + html.escape(str(
                    termination[
                        "answer"
                    ]
                ))
                + "</span></div>"
            )

        if termination.get(
            "error"
        ) is not None:
            termination_body += (
                '<div class="error-text">'
                "<strong>Error:</strong> "
                + html.escape(str(
                    termination[
                        "error"
                    ]
                ))
                + "</div>"
            )

        parts.append(card(
            termination_ref,
            "termination",
            "TERMINACIÓN",
            f"Fin del attempt {attempt_index}",
            termination_body,
        ))

    if tuple(rendered_refs) != tuple(
        review_case.presentation.evidence_refs
    ):
        raise ValueError(
            "La vista no pudo conservar exactamente "
            "las referencias canónicas de evidencia."
        )

    return "".join(parts)


def _available_dataset_ids() -> list[str]:
    """Lista los datasets cualitativos materializados."""

    if not RESULTS_DIR.exists():
        return []

    return sorted(
        path.name
        for path in RESULTS_DIR.iterdir()
        if (
            path.is_dir()
            and (path / "manifest.json").is_file()
            and (path / "cases.jsonl").is_file()
            and (path / "case_sources.jsonl").is_file()
        )
    )


def _page_html(
    *,
    dataset_id: str,
    annotator_id: str,
    split: str,
    status: str,
    review_cases: list[ReviewCase],
    review_case: ReviewCase | None,
    message: str | None = None,
) -> str:
    dataset_options = "".join(
        (
            f'<option value="{html.escape(existing_dataset_id)}"'
            f'{" selected" if existing_dataset_id == dataset_id else ""}>'
            f'{html.escape(existing_dataset_id)}'
            "</option>"
        )
        for existing_dataset_id in _available_dataset_ids()
    )

    annotators = list_annotators(
        dataset_id,
        results_dir=RESULTS_DIR,
    )

    if annotators:
        annotator_options = "".join(
            (
                f'<option value="{html.escape(existing_annotator)}"'
                f'{" selected" if existing_annotator == annotator_id else ""}>'
                f'{html.escape(existing_annotator)}'
                "</option>"
            )
            for existing_annotator in annotators
        )
    else:
        annotator_options = (
            '<option value="">Sin anotadores registrados</option>'
        )
    case_list_html = "".join(
        (
            '<a class="case-item'
            f'{" selected" if review_case is not None and item.case_id == review_case.case_id else ""}'
            '" href="'
            + html.escape(
                "/?" + urlencode({
                    "dataset_id": dataset_id,
                    "annotator_id": annotator_id,
                    "split": split,
                    "status": status,
                    "case_id": item.case_id,
                })
            )
            + '">'
            + html.escape(item.case_id)
            + (
                " ✓"
                if item.completed
                else (
                    " ◐"
                    if item.in_progress
                    else " ○"
                )
            )
            + "</a>"
        )
        for item in review_cases
    )

    completed_count = sum(
        item.completed
        for item in review_cases
    )

    message_html = (
        f'<p class="message">{html.escape(message)}</p>'
        if message
        else ""
    )

    case_html = ""

    if review_case is not None:
        active_criterion_id = (
            CRITERION_IDS[0]
        )
        criterion_tabs_html = "".join(
            (
                '<button '
                'type="button" '
                'class="criterion-tab'
                f'{" active" if criterion_id == active_criterion_id else ""}'
                f'{" not-applicable" if not review_case.case.criteria_applicability[criterion_id].applicable else ""}'
                '" '
                f'data-criterion="{criterion_id}" '
                f'title="{html.escape(CRITERIA_BY_ID[criterion_id].name)}">'
                f"{criterion_id}"
                '<span class="criterion-tab-state">'
                + (
                    "N/A"
                    if not review_case.case.criteria_applicability[
                        criterion_id
                    ].applicable
                    else (
                        "✓"
                        if review_case.annotation
                        is not None
                        and criterion_id
                        in review_case.annotation.criteria
                        else ""
                    )
                )
                + "</span></button>"
            )
            for criterion_id in CRITERION_IDS
        )

        criteria_html = "".join(
            _criterion_html(
                review_case,
                criterion_id,
                active=(
                    criterion_id
                    == active_criterion_id
                ),
            )
            for criterion_id in CRITERION_IDS
        )
        q1_4_auxiliary_html = (
            _q1_4_auxiliary_html(
                review_case
            )
        )

        evidence_html = (
            _evidence_cards_html(
                review_case
            )
        )

        action = (
            "update"
            if review_case.annotated
            else "save"
        )
        button_text = (
            "Actualizar anotación"
            if review_case.annotated
            else "Guardar anotación"
        )

        delete_annotation_html = (
            """
            <button
              type="submit"
              formaction="/annotation/delete"
              formnovalidate
              onclick="return confirm('¿Eliminar la anotación de este caso?')"
            >
              Eliminar anotación
            </button>
            """
            if review_case.annotated
            else ""
        )

        case_html = f"""
        <div class="review-layout">
          <aside class="case-list">
            <h2>Casos</h2>
            {case_list_html}
          </aside>

          <div class="workspace">
            <section class="evidence">
              <div class="panel-heading">
                <h2>Evidencia del caso</h2>
                <span>
                  {html.escape(review_case.case_id)}
                </span>
              </div>

              {evidence_html}
            </section>

            <form
              method="post"
              action="/annotation"
              id="annotation-form"
            >
              <input
                type="hidden"
                name="dataset_id"
                value="{html.escape(dataset_id)}"
              >
              <input
                type="hidden"
                name="annotator_id"
                value="{html.escape(annotator_id)}"
              >
              <input
                type="hidden"
                name="split"
                value="{html.escape(split)}"
              >
              <input
                type="hidden"
                name="status"
                value="{html.escape(status)}"
              >
              <input
                type="hidden"
                name="case_id"
                value="{html.escape(review_case.case_id)}"
              >
              <input
                type="hidden"
                name="action"
                value="{action}"
              >

              <section class="rubric">
                <div class="rubric-heading">
                  <h2>Anotación</h2>

                  <div class="criterion-tabs">
                    {criterion_tabs_html}
                  </div>
                </div>

                {_rubric_overview_html()}

                {criteria_html}

                <div class="annotation-actions">
                  <button type="submit">
                    {button_text}
                  </button>

                  {delete_annotation_html}
                </div>

                {q1_4_auxiliary_html}
              </section>
            </form>
          </div>
        </div>
        """

    split_options = "".join(
        (
            f'<option value="{value}"'
            f'{" selected" if split == value else ""}>'
            f'{label}'
            "</option>"
        )
        for value, label in (
            ("all", "Todos"),
            ("dev", "Dev"),
            ("holdout", "Holdout"),
        )
    )

    status_options = "".join(
        (
            f'<option value="{value}"'
            f'{" selected" if status == value else ""}>'
            f'{label}'
            "</option>"
        )
        for value, label in (
            ("all", "Todos"),
            ("pending", "Pendientes"),
            ("completed", "Completados"),
        )
    )

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>LLM Judge — Anotación humana</title>
<style>
* {{
  box-sizing: border-box;
}}

body {{
  font-family: sans-serif;
  margin: 0;
  height: 100vh;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  overflow: hidden;
  background: #f5f5f5;
  color: #222;
}}

header {{
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid #ddd;
}}

header h1 {{
  margin-top: 0;
}}

.controls {{
  display: flex;
  gap: 1rem;
  align-items: end;
  flex-wrap: wrap;
}}

.controls label {{
  display: flex;
  flex-direction: column;
  gap: .25rem;
}}

.review-layout {{
  min-height: 0;
  display: grid;
  grid-template-columns: 180px minmax(0, 1fr);
  gap: 1rem;
  padding: 1rem;
}}

.case-list {{
  min-height: 0;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: .5rem;
  padding: .75rem;
  display: flex;
  flex-direction: column;
  gap: .25rem;
}}

.case-list h2 {{
  margin-top: 0;
}}

.case-item {{
  padding: .45rem .55rem;
  border-radius: .3rem;
  text-decoration: none;
  color: inherit;
}}

.case-item:hover {{
  background: #eee;
}}

.case-item.selected {{
  font-weight: bold;
  background: #ddd;
}}

.workspace {{
  min-width: 0;
  min-height: 0;
  display: grid;
  grid-template-columns:
    minmax(0, 1.25fr)
    minmax(390px, .75fr);
  gap: 1rem;
}}

#annotation-form {{
  min-height: 0;
}}

.evidence,
.rubric {{
  height: 100%;
  min-height: 0;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: .5rem;
  padding: 1rem;
}}

.panel-heading {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 1rem;
}}

.panel-heading h2 {{
  margin-top: 0;
}}

.panel-heading span {{
  color: #777;
  font-size: .8rem;
}}

.evidence-rules,
.rubric-reference,
.criterion-guidance,
.criterion-applicability {{
  margin-bottom: .75rem;
  padding: .6rem .75rem;
  border: 1px solid #ddd;
  border-radius: .4rem;
  background: #fafafa;
}}

.evidence-rules summary,
.rubric-reference summary,
.criterion-applicability summary {{
  cursor: pointer;
  font-weight: 600;
}}

.criterion-guidance {{
  margin-top: .75rem;
}}

.criterion-applicability {{
  margin-top: .75rem;
}}

.task-card,
.evidence-card {{
  position: relative;
  margin-bottom: .75rem;
  padding: .85rem;
  border: 1px solid #d8d8d8;
  border-left-width: 4px;
  border-radius: .5rem;
}}

.task-card {{
  padding-top: 2rem;
  background: #f5f3ff;
  border-left-color: #6f63a6;
  white-space: pre-wrap;
}}

.task-card > .evidence-kind {{
  position: absolute;
  top: .55rem;
  right: .65rem;
}}

.attempt-heading {{
  margin: 1.15rem 0 .5rem;
  font-size: .95rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: .5rem;
}}

.evidence-card {{
  transition: box-shadow .12s ease;
}}

.evidence-card.selectable {{
  cursor: pointer;
}}

.evidence-card.selectable:hover {{
  box-shadow:
    0 2px 8px rgba(0, 0, 0, .08);
}}

.evidence-card.selected-evidence {{
  box-shadow:
    0 0 0 2px #2d6a4f;
}}

.evidence-user-message {{
  background: #eef6ff;
  border-left-color: #4b86b4;
}}

.evidence-internal-context {{
  background: #f3f3f3;
  border-left-color: #777;
}}

.evidence-iteration {{
  background: #fff8e8;
  border-left-color: #c58a24;
}}

.evidence-action {{
  background: #eef9f0;
  border-left-color: #4f8b5b;
}}

.evidence-termination {{
  background: #f6f0fa;
  border-left-color: #8661a8;
}}

.evidence-card-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: .55rem;
  background: transparent;
  border: 0;
  padding: 0;
}}

.evidence-meta {{
  display: flex;
  gap: .4rem;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
}}

.evidence-ref {{
  font: .7rem monospace;
  color: #777;
}}

.evidence-kind {{
  font-size: .65rem;
  font-weight: 700;
  letter-spacing: .05em;
  color: #555;
}}

.evidence-mark {{
  width: 1.1rem;
  text-align: center;
  font-weight: 700;
}}

.selected-evidence .evidence-mark {{
  color: #2d6a4f;
}}

.q14-trigger-marker {{
  display: none;
  padding: .15rem .4rem;
  border: 1px solid #9b7b27;
  border-radius: .3rem;
  background: #fff4c7;
  color: #6d5418;
  font-size: .65rem;
  font-weight: 700;
  white-space: nowrap;
}}

.evidence.q14-active .q14-trigger-marker {{
  display: inline-flex;
}}

.q14-trigger-highlight {{
  box-shadow:
    0 0 0 3px #d3a82f
    !important;
}}

.attempt-heading.q14-trigger-highlight {{
  padding: .3rem .45rem;
  border-radius: .35rem;
  background: #fff4c7;
}}

.q14-auxiliary {{
  display: none;
}}

.rubric.q14-active .q14-auxiliary {{
  display: block;
}}

.q14-detected-triggers {{
  margin: 1.5rem 0 0;
  padding: .65rem .75rem;
  border: 1px solid #d8c780;
  border-radius: .4rem;
  background: #fffdf2;
}}

.q14-detected-triggers > p:first-child {{
  margin-top: 0;
}}

.q14-trigger-list {{
  display: grid;
  gap: .4rem;
}}

.q14-trigger-disclaimer {{
  color: #555;
  font-size: .85rem;
}}

.q14-trigger-link {{
  width: 100%;
  padding: .45rem .55rem;
  border: 1px solid #ccc;
  border-radius: .35rem;
  background: white;
  text-align: left;
}}

.q14-trigger-link strong,
.q14-trigger-location {{
  display: block;
}}

.q14-trigger-location {{
  margin-top: .15rem;
  color: #666;
  font-size: .8rem;
}}

.evidence-text {{
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  line-height: 1.4;
}}

.internal-context-note {{
  margin-bottom: .45rem;
  color: #666;
  font-size: .8rem;
  font-style: italic;
}}

.internal-context-section-title {{
  margin-top: .75rem;
  margin-bottom: .35rem;
  font-size: .78rem;
  font-weight: 700;
  text-transform: uppercase;
}}

.preserved-round {{
  margin-top: .5rem;
  padding: .55rem .65rem;
  border: 1px solid #ccc;
  border-radius: .35rem;
  background: rgba(255, 255, 255, .7);
}}

.preserved-round-header {{
  display: flex;
  justify-content: space-between;
  gap: .75rem;
  margin-bottom: .5rem;
}}

.preserved-round-assistant {{
  margin-bottom: .5rem;
}}

.preserved-round-action {{
  margin-top: .5rem;
  padding-top: .5rem;
  border-top: 1px solid #ddd;
}}

.evidence-body > div {{
  margin-top: .4rem;
}}

.evidence-body > div:first-child {{
  margin-top: 0;
}}

.evidence-body code {{
  font-size: .82rem;
}}

.raw-arguments {{
  margin:
    .15rem
    0
    .45rem
    1rem;
  color: #666;
}}

.observation {{
  padding: .45rem .55rem;
  border-radius: .35rem;
  background:
    rgba(255, 255, 255, .65);
}}

.observation-error {{
  background: #fff1f1;
  border: 1px solid #d7a2a2;
}}

.error-text {{
  margin-top: .4rem;
  color: #8a3030;
}}

.repair-badge {{
  display: inline-block;
  margin: .4rem 0;
  padding: .15rem .35rem;
  border-radius: .25rem;
  background: #fff0c2;
  font-size: .65rem;
  font-weight: 700;
}}

.muted {{
  color: #777;
  font-style: italic;
}}

.rubric-heading {{
  position: sticky;
  top: -1rem;
  z-index: 2;
  margin:
    -1rem
    -1rem
    1rem;
  padding:
    1rem
    1rem
    .75rem;
  background: white;
  border-bottom: 1px solid #ddd;
}}

.rubric-heading h2 {{
  margin-top: 0;
}}

.criterion-tabs {{
  display: grid;
  grid-template-columns:
    repeat(4, minmax(0, 1fr));
  gap: .35rem;
}}

.criterion-tab {{
  display: flex;
  justify-content: center;
  gap: .3rem;
  padding: .45rem .3rem;
  border: 1px solid #ccc;
  border-radius: .35rem;
  background: #f6f6f6;
}}

.criterion-tab.active {{
  background: #e4e4e4;
  border-color: #555;
  font-weight: 700;
}}

.criterion-tab.not-applicable {{
  color: #777;
}}

.criterion-tab-state {{
  min-width: 1.1rem;
  font-size: .72rem;
}}

.criterion-panel {{
  display: none;
}}

.criterion-panel.active {{
  display: block;
}}

.criterion-panel h3 {{
  margin-top: 0;
}}

.criterion-na,
.evidence-hint {{
  padding: .65rem .75rem;
  border-radius: .4rem;
  background: #f3f3f3;
}}

.verdict {{
  display: flex;
  gap: 1.5rem;
  margin: 1rem 0;
}}

textarea {{
  display: block;
  width: 100%;
  min-height: 8rem;
  margin: .4rem 0 1rem;
}}

.annotation-actions {{
  display: flex;
  gap: .6rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}}

.message {{
  padding: .75rem 1rem;
  background: #eef6ee;
  border: 1px solid #aacbaa;
}}

button {{
  padding: .6rem 1rem;
  cursor: pointer;
}}

@media (max-width: 900px) {{
  body {{
    height: auto;
    min-height: 100vh;
    display: block;
    overflow: auto;
  }}

  .review-layout {{
    grid-template-columns: 1fr;
  }}

  .case-list {{
    max-height: 16rem;
  }}

  .workspace {{
    grid-template-columns: 1fr;
  }}

  .evidence,
  .rubric {{
    height: auto;
    overflow: visible;
  }}
}}
</style>
</head>

<body>
<header>
  <h1>Evaluación cualitativa</h1>

  <form
    method="get"
    action="/"
    class="controls"
    id="navigation-form"
  >
    <label>
      Dataset
      <select
        name="dataset_id"
        class="navigation-control"
      >
        {dataset_options}
      </select>
    </label>

    <label>
      Anotador
      <select
        name="annotator_id"
        class="navigation-control"
      >
        {annotator_options}
      </select>
    </label>

    <label>
      Nuevo anotador
      <input
        name="new_annotator_id"
        autocomplete="off"
      >
    </label>

    <label>
      Split
      <select
        name="split"
        class="navigation-control"
      >
        {split_options}
      </select>
    </label>

    <label>
      Estado
      <select
        name="status"
        class="navigation-control"
      >
        {status_options}
      </select>
    </label>

    <button
      type="submit"
      formmethod="post"
      formaction="/annotator/create"
    >
      Registrar anotador
    </button>

    <button
      type="submit"
      formmethod="post"
      formaction="/annotator/delete"
      onclick="return confirm('¿Eliminar este anotador y todas sus anotaciones?')"
    >
      Eliminar anotador
    </button>
  </form>

  <p>
    Progreso del filtro:
    {completed_count}/{len(review_cases)} completados.
  </p>
  {message_html}
</header>

{case_html}

<script>
const navigationForm =
  document.getElementById(
    "navigation-form"
  );
const annotationForm =
  document.getElementById(
    "annotation-form"
  );

const tabs = [
  ...document.querySelectorAll(
    ".criterion-tab"
  ),
];
const panels = [
  ...document.querySelectorAll(
    ".criterion-panel"
  ),
];
const cards = [
  ...document.querySelectorAll(
    ".evidence-card"
  ),
];
const q14TriggerLinks = [
  ...document.querySelectorAll(
    ".q14-trigger-link"
  ),
];
const evidencePanel =
  document.querySelector(
    ".evidence"
  );
const rubricPanel =
  document.querySelector(
    ".rubric"
  );
const caseList =
  document.querySelector(
    ".case-list"
  );

let annotationDirty = false;
let activeCriterion = (
  tabs.find(
    (tab) =>
      tab.classList.contains(
        "active"
      )
  )?.dataset.criterion
  || null
);

function reviewStateKey() {{
  if (!annotationForm) {{
    return null;
  }}

  const datasetId =
    annotationForm.querySelector(
      'input[name="dataset_id"]'
    )?.value;
  const annotatorId =
    annotationForm.querySelector(
      'input[name="annotator_id"]'
    )?.value;
  const caseId =
    annotationForm.querySelector(
      'input[name="case_id"]'
    )?.value;

  if (
    !datasetId
    || !annotatorId
    || !caseId
  ) {{
    return null;
  }}

  return (
    "llm-judge-review:"
    + datasetId
    + ":"
    + annotatorId
    + ":"
    + caseId
  );
}}

function saveReviewState() {{
  const key =
    reviewStateKey();

  if (!key) {{
    return;
  }}

  sessionStorage.setItem(
    key,
    JSON.stringify({{
      activeCriterion,
      evidenceScrollTop:
        evidencePanel?.scrollTop
        ?? 0,
      rubricScrollTop:
        rubricPanel?.scrollTop
        ?? 0,
      caseListScrollTop:
        caseList?.scrollTop
        ?? 0,
    }})
  );
}}

function restoreReviewState() {{
  const key =
    reviewStateKey();

  if (!key) {{
    return false;
  }}

  const serialized =
    sessionStorage.getItem(
      key
    );

  if (!serialized) {{
    return false;
  }}

  sessionStorage.removeItem(
    key
  );

  try {{
    const state =
      JSON.parse(
        serialized
      );

    const criterionExists =
      tabs.some(
        (tab) =>
          tab.dataset.criterion
          === state.activeCriterion
      );

    if (criterionExists) {{
      activateCriterion(
        state.activeCriterion
      );
    }}

    requestAnimationFrame(
      () => {{
        if (evidencePanel) {{
          evidencePanel.scrollTop =
            state.evidenceScrollTop
            ?? 0;
        }}

        if (rubricPanel) {{
          rubricPanel.scrollTop =
            state.rubricScrollTop
            ?? 0;
        }}

        if (caseList) {{
          caseList.scrollTop =
            state.caseListScrollTop
            ?? 0;
        }}
      }}
    );

    return true;
  }} catch {{
    return false;
  }}
}}

function checkboxFor(card) {{
  if (!activeCriterion) {{
    return null;
  }}

  return card.querySelector(
    `.evidence-checkbox[data-criterion="${{activeCriterion}}"]`
  );
}}

function refreshCards() {{
  cards.forEach((card) => {{
    const checkbox =
      checkboxFor(card);
    const selected =
      Boolean(checkbox?.checked);

    card.classList.toggle(
      "selectable",
      Boolean(checkbox)
    );
    card.classList.toggle(
      "selected-evidence",
      selected
    );

    card.querySelector(
      ".evidence-mark"
    ).textContent = checkbox
      ? (
          selected
          ? "✓"
          : "○"
        )
      : "—";
  }});
}}

function activateCriterion(
  criterionId
) {{
  activeCriterion =
    criterionId;

  tabs.forEach((tab) => {{
    tab.classList.toggle(
      "active",
      tab.dataset.criterion
      === criterionId
    );
  }});

  panels.forEach((panel) => {{
    panel.classList.toggle(
      "active",
      panel.dataset.criterion
      === criterionId
    );
  }});

  refreshCards();

  evidencePanel?.classList.toggle(
    "q14-active",
    criterionId === "Q1.4"
  );
  rubricPanel?.classList.toggle(
    "q14-active",
    criterionId === "Q1.4"
  );
}}

let q14HighlightTimeout = null;

function clearQ14Highlight() {{
  document
    .querySelectorAll(
      ".q14-trigger-highlight"
    )
    .forEach((element) => {{
      element.classList.remove(
        "q14-trigger-highlight"
      );
    }});
}}

q14TriggerLinks.forEach((link) => {{
  link.addEventListener(
    "click",
    () => {{
      clearQ14Highlight();

      let evidenceRefs = [];

      try {{
        evidenceRefs = JSON.parse(
          link.dataset.triggerRefs
          || "[]"
        );
      }} catch {{
        return;
      }}

      evidenceRefs.forEach(
        (evidenceRef) => {{
          const card = cards.find(
            (item) =>
              item.dataset.evidenceRef
              === evidenceRef
          );

          card?.classList.add(
            "q14-trigger-highlight"
          );
        }}
      );

      const targetId =
        link.dataset.triggerTarget;
      const target =
        cards.find(
          (item) =>
            item.dataset.evidenceRef
            === targetId
        )
        || document.getElementById(
          targetId
        );

      target?.classList.add(
        "q14-trigger-highlight"
      );
      target?.scrollIntoView({{
        behavior: "smooth",
        block: "center",
      }});

      if (q14HighlightTimeout) {{
        window.clearTimeout(
          q14HighlightTimeout
        );
      }}

      q14HighlightTimeout =
        window.setTimeout(
          clearQ14Highlight,
          1800
        );
    }}
  );
}});

tabs.forEach((tab) => {{
  tab.addEventListener(
    "click",
    () => activateCriterion(
      tab.dataset.criterion
    )
  );
}});

cards.forEach((card) => {{
  function toggleEvidence() {{
    const checkbox =
      checkboxFor(card);

    if (!checkbox) {{
      return;
    }}

    checkbox.checked =
      !checkbox.checked;

    checkbox.dispatchEvent(
      new Event(
        "change",
        {{
          bubbles: true,
        }}
      )
    );

    refreshCards();
  }}

  card.addEventListener(
    "click",
    toggleEvidence
  );

  card.addEventListener(
    "keydown",
    (event) => {{
      if (
        event.key === "Enter"
        || event.key === " "
      ) {{
        event.preventDefault();
        toggleEvidence();
      }}
    }}
  );
}});

if (annotationForm) {{
  annotationForm.addEventListener(
    "input",
    () => {{
      annotationDirty = true;
    }}
  );

  annotationForm.addEventListener(
    "change",
    () => {{
      annotationDirty = true;
    }}
  );

  annotationForm.addEventListener(
    "submit",
    (event) => {{
      if (
        event.submitter
        ?.formAction
        .endsWith(
          "/annotation/delete"
        )
      ) {{
        annotationDirty = false;
        return;
      }}

      let completedCriteria = 0;

      for (
        const panel
        of panels
      ) {{
        if (
          panel.dataset.applicable
          !== "true"
        ) {{
          continue;
        }}

        const criterionId =
          panel.dataset.criterion;

        const verdict =
          annotationForm.querySelector(
            `input[name="${{criterionId}}.verdict"]:checked`
          );

        const reason =
          annotationForm.querySelector(
            `textarea[name="${{criterionId}}.reason"]`
          )?.value.trim();

        const evidence =
          document.querySelector(
            `.evidence-checkbox[data-criterion="${{criterionId}}"]:checked`
          );

        const started = Boolean(
          verdict
          || reason
          || evidence
        );

        if (!started) {{
          continue;
        }}

        if (
          !verdict
          || !reason
          || !evidence
        ) {{
          event.preventDefault();

          activateCriterion(
            criterionId
          );

          window.alert(
            `${{criterionId}} está empezado `
            + "pero incompleto. Requiere "
            + "veredicto, justificación "
            + "y al menos una evidencia."
          );

          return;
        }}

        completedCriteria += 1;
      }}

      if (completedCriteria === 0) {{
        event.preventDefault();

        const firstApplicable =
          panels.find(
            (panel) =>
              panel.dataset.applicable
              === "true"
          );

        if (firstApplicable) {{
          activateCriterion(
            firstApplicable.dataset.criterion
          );
        }}

        window.alert(
          "Completá al menos un criterio "
          + "antes de guardar."
        );

        return;
      }}

      saveReviewState();
      annotationDirty = false;
    }}
  );
}}

function allowNavigation() {{
  if (!annotationDirty) {{
    return true;
  }}

  const discard =
    window.confirm(
      "Hay cambios sin guardar. "
      + "¿Querés descartarlos?"
    );

  if (discard) {{
    annotationDirty = false;
  }}

  return discard;
}}

document
  .querySelectorAll(
    ".navigation-control"
  )
  .forEach((control) => {{
    const initialValue =
      control.value;

    control.addEventListener(
      "change",
      () => {{
        if (allowNavigation()) {{
          navigationForm.submit();
        }} else {{
          control.value =
            initialValue;
        }}
      }}
    );
  }});

document
  .querySelectorAll(
    ".case-item"
  )
  .forEach((link) => {{
    link.addEventListener(
      "click",
      (event) => {{
        if (!allowNavigation()) {{
          event.preventDefault();
        }}
      }}
    );
  }});

navigationForm
  .querySelectorAll(
    'button[type="submit"]'
  )
  .forEach((button) => {{
    button.addEventListener(
      "click",
      (event) => {{
        if (!allowNavigation()) {{
          event.preventDefault();
        }}
      }}
    );
  }});

window.addEventListener(
  "beforeunload",
  (event) => {{
    if (annotationDirty) {{
      event.preventDefault();
      event.returnValue = "";
    }}
  }}
);

const reviewStateRestored =
  restoreReviewState();

if (
  !reviewStateRestored
  && activeCriterion
) {{
  activateCriterion(
    activeCriterion
  );
}}
</script>

</body>
</html>
"""


class AnnotationHandler(BaseHTTPRequestHandler):
    """Handler HTTP de la interfaz local de anotación."""

    def _send_html(
        self,
        content: str,
        *,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        data = content.encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(data)),
        )
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        dataset_id = _query_value(
            query,
            "dataset_id",
            DATASET_CONFIG["dataset_id"],
        )
        annotator_id = _query_value(
            query,
            "annotator_id",
            "",
        )
        annotators = list_annotators(
            dataset_id,
            results_dir=RESULTS_DIR,
        )

        if annotator_id not in annotators:
            annotator_id = _default_annotator_id(
                dataset_id
            )
        split = _query_value(
            query,
            "split",
            "all",
        )
        status = _query_value(
            query,
            "status",
            "all",
        )
        case_id = _query_value(
            query,
            "case_id",
            "",
        )

        try:
            if annotator_id:
                review_cases = _load_selected_cases(
                    dataset_id,
                    annotator_id,
                    split,
                    status,
                )
                review_case = _selected_case(
                    review_cases,
                    case_id or None,
                )
            else:
                review_cases = []
                review_case = None
            page = _page_html(
                dataset_id=dataset_id,
                annotator_id=annotator_id,
                split=split,
                status=status,
                review_cases=review_cases,
                review_case=review_case,
            )
        except Exception as exc:
            page = _page_html(
                dataset_id=dataset_id,
                annotator_id=annotator_id,
                split=split,
                status=status,
                review_cases=[],
                review_case=None,
                message=str(exc),
            )

        self._send_html(page)

    def do_POST(self) -> None:
        if self.path not in {
            "/annotation",
            "/annotation/delete",
            "/annotator/create",
            "/annotator/delete",
        }:
            self.send_error(
                HTTPStatus.NOT_FOUND,
            )
            return

        content_length = int(
            self.headers.get(
                "Content-Length",
                "0",
            )
        )
        form = parse_qs(
            self.rfile.read(
                content_length
            ).decode("utf-8"),
            keep_blank_values=True,
        )

        dataset_id = _query_value(
            form,
            "dataset_id",
            DATASET_CONFIG["dataset_id"],
        )
        annotator_id = _query_value(
            form,
            "annotator_id",
            "",
        )
        split = _query_value(
            form,
            "split",
            "all",
        )
        status = _query_value(
            form,
            "status",
            "all",
        )
        if self.path in {
            "/annotator/create",
            "/annotator/delete",
        }:
            try:
                if self.path == "/annotator/create":
                    managed_annotator_id = _query_value(
                        form,
                        "new_annotator_id",
                        "",
                    ).strip()
                    create_annotator(
                        dataset_id,
                        managed_annotator_id,
                        results_dir=RESULTS_DIR,
                    )
                    redirect_annotator_id = managed_annotator_id
                else:
                    delete_annotator(
                        dataset_id,
                        annotator_id,
                        results_dir=RESULTS_DIR,
                    )
                    redirect_annotator_id = _default_annotator_id(
                        dataset_id
                    )

                location = "/?" + urlencode({
                    "dataset_id": dataset_id,
                    "annotator_id": redirect_annotator_id,
                    "status": status,
                    "split": split,
                })

                self.send_response(
                    HTTPStatus.SEE_OTHER
                )
                self.send_header(
                    "Location",
                    location,
                )
                self.end_headers()
                return

            except Exception as exc:
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    str(exc),
                )
                return
        case_id = _query_value(
            form,
            "case_id",
            "",
        )

        if self.path == "/annotation/delete":
            try:
                delete_human_annotation(
                    dataset_id,
                    annotator_id,
                    case_id,
                    results_dir=RESULTS_DIR,
                )

                location = "/?" + urlencode({
                    "dataset_id": dataset_id,
                    "annotator_id": annotator_id,
                    "split": split,
                    "status": status,
                    "case_id": case_id,
                })

                self.send_response(
                    HTTPStatus.SEE_OTHER
                )
                self.send_header(
                    "Location",
                    location,
                )
                self.end_headers()
                return

            except Exception as exc:
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    str(exc),
                )
                return

        action = _query_value(
            form,
            "action",
            "save",
        )

        try:
            review_cases = _load_selected_cases(
                dataset_id,
                annotator_id,
                split,
                status,
            )
            review_case = _selected_case(
                review_cases,
                case_id,
            )

            if review_case is None:
                raise ValueError(
                    "No se encontró el caso seleccionado."
                )

            annotation = _annotation_from_form(
                review_case,
                annotator_id,
                form,
            )

            if action == "update":
                update_human_annotation(
                    dataset_id,
                    annotation,
                    results_dir=RESULTS_DIR,
                )
            else:
                save_human_annotation(
                    dataset_id,
                    annotation,
                    results_dir=RESULTS_DIR,
                )

            location = "/?" + urlencode({
                "dataset_id": dataset_id,
                "annotator_id": annotator_id,
                "split": split,
                "status": status,
                "case_id": case_id,
            })

            self.send_response(
                HTTPStatus.SEE_OTHER
            )
            self.send_header(
                "Location",
                location,
            )
            self.end_headers()

        except Exception as exc:
            review_cases = _load_selected_cases(
                dataset_id,
                annotator_id,
                split,
                status,
            )
            review_case = _selected_case(
                review_cases,
                case_id,
            )
            page = _page_html(
                dataset_id=dataset_id,
                annotator_id=annotator_id,
                split=split,
                status=status,
                review_cases=review_cases,
                review_case=review_case,
                message=str(exc),
            )
            self._send_html(
                page,
                status=HTTPStatus.BAD_REQUEST,
            )

    def log_message(
        self,
        format: str,
        *args: object,
    ) -> None:
        """Evita ruido de requests HTTP en la terminal."""


def main() -> int:
    server = ThreadingHTTPServer(
        (HOST, PORT),
        AnnotationHandler,
    )
    url = f"http://{HOST}:{PORT}/"

    print(
        f"Reviewer cualitativo disponible en {url}"
    )
    print(
        "Ctrl+C para detenerlo."
    )

    threading.Timer(
        0.5,
        lambda: webbrowser.open(url),
    ).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())