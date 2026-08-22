"""Rúbrica de calidad de planificación para la evaluación cualitativa M3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


CriterionId = Literal["Q1.1", "Q1.2", "Q1.3", "Q1.4"]
CriterionApplicability = Literal["always", "conditional"]

RUBRIC_VERSION = "planning-quality-v1"
DIMENSION_ID = "Q1"
DIMENSION_NAME = "Calidad de la planificación durante la trayectoria"
DIMENSION_DESCRIPTION = (
    "Evalúa la capacidad del agente para construir y mantener una estrategia "
    "orientada al objetivo, fundamentarla en la información obtenida, "
    "traducirla en acciones coherentes y revisarla cuando nueva evidencia "
    "lo requiere."
)

MATERIALITY_RULE = (
    "Un error aislado no hace fallar automáticamente un criterio. Una "
    "desviación es material cuando afecta decisiones posteriores sin ser "
    "corregida, sostiene una secuencia basada en la misma premisa o estrategia "
    "defectuosa, viola una dependencia con consecuencias relevantes o produce "
    "un segmento sostenido sin progreso ni obtención razonable de nueva "
    "información."
)

EVIDENCE_RULES = (
    "La unidad evaluada es el trial completo, incluidos todos sus attempts.",
    (
        "Las acciones efectivamente ejecutadas y las observaciones del mundo "
        "constituyen la evidencia primaria sobre lo que ocurrió."
    ),
    (
        "El contenido textual del agente puede aportar evidencia sobre una "
        "estrategia, subobjetivo o intención expresados, pero no prevalece "
        "sobre las acciones ni sobre las observaciones del mundo."
    ),
    (
        "No expresar explícitamente un plan no constituye por sí mismo un "
        "fallo; la planificación también puede inferirse de la trayectoria "
        "observable."
    ),
    (
        "Todas las acciones de una misma iteración se consideran decididas "
        "antes de observar cualquiera de sus resultados."
    ),
)

Q1_1_GUIDANCE = (
    (
        "Un error producido por una herramienta no implica por sí mismo una "
        "inconsistencia factual. Q1.1 evalúa cómo el agente interpreta y "
        "utiliza posteriormente la evidencia observable."
    ),
)

Q1_2_GUIDANCE = (
    (
        "No se exige que el agente explicite formalmente una descomposición "
        "en subobjetivos. La ausencia de esa verbalización no constituye por "
        "sí sola un FAIL."
    ),
)

Q1_4_APPLICABILITY_DESCRIPTION = (
    "Q1.4 sólo es evaluable cuando la trayectoria contiene una oportunidad "
    "observable de monitorear el resultado de una conducta y, cuando "
    "corresponde, revisar el curso de acción. Si esa oportunidad no aparece, "
    "el criterio es N/A porque la trayectoria no permite observar capacidad "
    "de replanificación."
)

Q1_4_CONTINUATION_TRIGGER = (
    "El trial contiene más de un attempt."
)

Q1_4_ERROR_TRIGGER = (
    "Existe una observación marcada como error antes de una iteración "
    "posterior."
)

Q1_4_REPETITION_TRIGGER = (
    "Una acción efectiva se repite en una iteración posterior con la misma "
    "herramienta, los mismos argumentos y el mismo resultado observable."
)

Q1_4_APPLICABILITY_TRIGGERS = (
    (
        Q1_4_CONTINUATION_TRIGGER,
        (
            "Entre attempts, el agente recibe un mensaje de continuación que "
            "indica que la trayectoria anterior no completó el desafío y abre "
            "una nueva oportunidad para ajustar su comportamiento."
        ),
    ),
    (
        Q1_4_ERROR_TRIGGER,
        (
            "El error aporta evidencia de que una acción no produjo un "
            "resultado válido y existe una decisión posterior en la que el "
            "agente puede reaccionar."
        ),
    ),
    (
        Q1_4_REPETITION_TRIGGER,
        (
            "La repetición permite observar si el agente incorpora un "
            "resultado ya obtenido o persiste sin obtener nueva información "
            "ni progreso."
        ),
    ),
)

Q1_4_APPLICABILITY_NOTES = (
    (
        "A efectos del trigger de error, una observación se marca como error "
        "cuando el paso persistido contiene un error o cuando su contenido "
        "observable comienza con 'Error:'."
    ),
    (
        "Para comparar repeticiones, los argumentos que pueden interpretarse "
        "como un objeto JSON se comparan estructuralmente; en caso contrario "
        "se compara su representación raw."
    ),
    (
        "Una repetición de acciones dentro de una misma iteración no activa "
        "por sí sola Q1.4, porque esas acciones fueron decididas antes de "
        "observar cualquiera de sus resultados."
    ),
    (
        "Un error ocurrido en la última iteración sin una decisión posterior "
        "no activa por sí solo Q1.4, porque no existe una oportunidad "
        "observable de reaccionar a ese error."
    ),
)

Q1_4_GUIDANCE = (
    (
        "Las condiciones de aplicabilidad no constituyen por sí mismas un "
        "FAIL. Una vez que Q1.4 aplica, PASS o FAIL depende de cómo el agente "
        "incorpora la evidencia disponible en sus decisiones posteriores."
    ),
)

Q1_4_NO_TRIGGER_REASON = (
    "No se detectó ninguno de los triggers determinísticos de Q1.4."
)

@dataclass(frozen=True)
class CriterionDefinition:
    """Definición versionada de un criterio cualitativo."""

    id: CriterionId
    name: str
    question: str
    pass_description: str
    fail_description: str
    applicability: CriterionApplicability
    guidance: tuple[str, ...] = ()
    applicability_description: str | None = None
    applicability_triggers: tuple[
        tuple[str, str],
        ...,
    ] = ()
    applicability_notes: tuple[str, ...] = ()


CRITERIA = (
    CriterionDefinition(
        id="Q1.1",
        name="Consistencia factual con la evidencia",
        question=(
            "¿Las decisiones del agente son compatibles con los hechos sobre "
            "el mundo que la trayectoria ya estableció?"
        ),
        pass_description=(
            "No hay decisiones materialmente basadas en hechos que la evidencia "
            "disponible ya haya contradicho. Se permiten hipótesis todavía no "
            "verificadas, inferencias razonables que luego resulten falsas y "
            "errores aislados corregidos al recibir información suficiente."
        ),
        fail_description=(
            "El agente basa materialmente una o más decisiones en una creencia "
            "que la evidencia disponible ya contradice y no corrige esa "
            "representación de forma adecuada."
        ),
        applicability="always",
        guidance=Q1_1_GUIDANCE,
    ),
    CriterionDefinition(
        id="Q1.2",
        name="Estructuración de subobjetivos y dependencias",
        question=(
            "¿El agente identifica y mantiene una estructura razonable de "
            "subobjetivos y prerrequisitos para alcanzar el objetivo?"
        ),
        pass_description=(
            "El agente identifica y mantiene razonablemente los subobjetivos, "
            "prerrequisitos y relaciones de orden relevantes para el objetivo."
        ),
        fail_description=(
            "La estrategia omite, pierde o estructura incorrectamente de forma "
            "material uno o más subobjetivos o prerrequisitos necesarios."
        ),
        applicability="always",
        guidance=Q1_2_GUIDANCE,
    ),
    CriterionDefinition(
        id="Q1.3",
        name="Consistencia de la ejecución con la estrategia",
        question=(
            "¿Las acciones efectivamente elegidas implementan de manera "
            "coherente la estrategia o el subobjetivo vigente?"
        ),
        pass_description=(
            "Las acciones implementan razonablemente la estrategia o el "
            "subobjetivo vigente. Cuando no hay una estrategia explicitada, "
            "mantienen una relación razonable con el progreso hacia el objetivo "
            "o con la reducción de una incertidumbre relevante."
        ),
        fail_description=(
            "Existe una divergencia material entre la estrategia o el "
            "subobjetivo vigente y las acciones elegidas sin nueva evidencia "
            "que la justifique, o un segmento material de acciones sin relación "
            "razonable con el progreso o una incertidumbre relevante."
        ),
        applicability="always",
    ),
    CriterionDefinition(
        id="Q1.4",
        name="Monitoreo y replanificación",
        question=(
            "Ante feedback adverso o evidencia observable de falta de progreso, "
            "¿el agente revisa adecuadamente su estrategia o su conducta?"
        ),
        pass_description=(
            "El agente incorpora el feedback o la falta de progreso y ajusta "
            "razonablemente sus decisiones o estrategia cuando corresponde."
        ),
        fail_description=(
            "El agente persiste materialmente en una acción, estrategia o "
            "premisa que el feedback o la falta de progreso ya mostraron "
            "inadecuada, sin nueva evidencia que justifique esa persistencia."
        ),
        applicability="conditional",
        guidance=Q1_4_GUIDANCE,
        applicability_description=Q1_4_APPLICABILITY_DESCRIPTION,
        applicability_triggers=Q1_4_APPLICABILITY_TRIGGERS,
        applicability_notes=Q1_4_APPLICABILITY_NOTES,
    ),
)

CRITERION_IDS: tuple[CriterionId, ...] = tuple(
    criterion.id
    for criterion in CRITERIA
)

CRITERIA_BY_ID = {
    criterion.id: criterion
    for criterion in CRITERIA
}

BOUNDARY_RULES = (
    "Q1.1 evalúa la consistencia con el estado conocido del mundo.",
    "Q1.2 evalúa la estructura de subobjetivos y dependencias del plan.",
    "Q1.3 evalúa si las acciones implementan la estrategia vigente.",
    (
        "Q1.4 evalúa si la estrategia o conducta se revisa ante feedback "
        "adverso o falta observable de progreso."
    ),
    (
        "El primer intento de una estrategia razonable corresponde a Q1.3; "
        "su persistencia después de feedback adverso corresponde a Q1.4."
    ),
    (
        "Una misma evidencia puede sustentar más de un FAIL solamente cuando "
        "demuestra defectos conceptualmente distintos."
    ),
)