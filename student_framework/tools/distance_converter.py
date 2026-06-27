"""Herramienta: conversor de distancias.

Convierte un valor numérico entre unidades de distancia.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from mia_agents.types import ToolSchema

_CONVERSIONS: dict[tuple[str, str], float] = {
    ("km", "millas"): 0.621371,
    ("millas", "km"): 1.60934,
    ("metros", "pies"): 3.28084,
    ("pies", "metros"): 0.3048,
    ("km", "metros"): 1000.0,
    ("metros", "km"): 0.001,
    ("millas", "pies"): 5280.0,
    ("pies", "millas"): 0.000189394,
}


def distance_converter(
    value: Annotated[float, Field(description="Valor numérico a convertir.")],
    from_unit: Annotated[
        Literal["km", "millas", "metros", "pies"],
        Field(description="Unidad de origen."),
    ],
    to_unit: Annotated[
        Literal["km", "millas", "metros", "pies"],
        Field(description="Unidad de destino."),
    ],
) -> str:
    """Convierte un valor numérico entre unidades de distancia.

    Unidades soportadas: km, millas, metros, pies.
    """
    f = from_unit.lower().strip()
    t = to_unit.lower().strip()

    if f == t:
        return f"{value} {f}"

    if (f, t) not in _CONVERSIONS:
        raise ValueError(f"Conversión no soportada: {from_unit!r} → {to_unit!r}")

    result = value * _CONVERSIONS[(f, t)]
    return f"{value} {f} = {result:.4g} {t}"


distance_converter_schema = ToolSchema.from_callable(distance_converter)