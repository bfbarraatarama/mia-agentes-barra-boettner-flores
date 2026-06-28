from __future__ import annotations
from typing import Annotated, Literal
from pydantic import Field
from mia_agents.types import ToolSchema

Operator = Literal["+", "-", "*", "%"]

"""
Herramienta: calculadora
Dado 2 numeros y una operacion, la ejecuta y devuelve el resultado
"""

def calculator(
    a: Annotated[float, Field(description="Primer operando.")],
    b: Annotated[float, Field(description="Segundo operando.")],
    op: Annotated[Operator, Field(description="Operador: +, -, *, %.")],
) -> str:
  a_int = float(a)
  b_int = float(b)
  """Aplica una operación binaria y devuelve el resultado."""
  if op == "+":
    result = a_int + b_int
  elif op == "-":
    result = a_int - b_int
  elif op == "*":
    result = a_int * b_int
  elif op == "%":
    result = a_int % b_int
  else:
    raise ValueError(f"Operador no soportado: {op!r}")
  return str(result)


calculator_schema = ToolSchema.from_callable(calculator)