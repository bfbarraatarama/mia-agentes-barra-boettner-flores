from __future__ import annotations
from typing import Annotated, Any, Literal
from pydantic import Field
from mia_agents.types import ToolSchema

Operator = Literal["+", "-", "*", "%"]

SUPPORTED_OPERATORS = ("+", "-", "*", "%")

"""
Herramienta: calculadora
Dado 2 numeros y una operacion, la ejecuta y devuelve el resultado.
Manejo de errores: en lugar de fallar, la herramienta devuelve
un mensaje accionable que le permite al LLM corregir los argumentos y volver a
intentar.
"""


def _coerce_number(name: str, value: Any) -> float | str:
  """Validacion que verifica que los parametros sean numeros"""
  if isinstance(value, bool):
    return (
      f"El parámetro '{name}' no es numérico: recibí {value!r} (booleano). "
      f"Debe ser un número, por ejemplo 3 o 2.5."
    )
  try:
    return float(value)
  except (TypeError, ValueError):
    return (
      f"El parámetro '{name}' no es numérico: recibí {value!r} "
      f"({type(value).__name__}) y no puede interpretarse como número. "
      f"Debe ser un número, por ejemplo 3 o 2.5."
    )


def calculator(
    a: Annotated[float, Field(description="Primer operando.")],
    b: Annotated[float, Field(description="Segundo operando.")],
    op: Annotated[Operator, Field(description="Operador: +, -, *, %.")],
) -> str:
  """Aplica una operación binaria y devuelve el resultado.
  Ante errores recuperables devuelve un mensaje accionable (no lanza
  excepción) para que el LLM pueda reintentar con argumentos válidos.
  """
  if op not in SUPPORTED_OPERATORS:
    permitidos = ", ".join(SUPPORTED_OPERATORS)
    return (
      f"Operador no soportado: {op!r}. "
      f"Los operadores permitidos son: {permitidos}."
    )

  a_num = _coerce_number("a", a)
  if isinstance(a_num, str):
    return a_num
  b_num = _coerce_number("b", b)
  if isinstance(b_num, str):
    return b_num

  if op == "+":
    result = a_num + b_num
  elif op == "-":
    result = a_num - b_num
  elif op == "*":
    result = a_num * b_num
  else:
    if b_num == 0:
      return (
        "No se puede calcular el módulo por cero: el parámetro 'b' debe ser "
        "distinto de 0 para la operación '%'."
      )
    result = a_num % b_num
  return str(result)


calculator_schema = ToolSchema.from_callable(calculator)