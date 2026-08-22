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


@dataclass(frozen=True)
class CriterionDefinition:
    """Definición versionada de un criterio cualitativo."""

    id: CriterionId
    name: str
    question: str
    pass_description: str
    fail_description: str
    applicability: CriterionApplicability


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