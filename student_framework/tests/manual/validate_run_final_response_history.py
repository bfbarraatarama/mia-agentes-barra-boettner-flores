"""Validación manual de la persistencia de respuestas finales en MyAgent.run().

Uso:

    python student_framework/tests/manual/validate_run_final_response_history.py

Opcionalmente, puede indicarse la cantidad de intentos:

    python student_framework/tests/manual/validate_run_final_response_history.py 50
"""

from __future__ import annotations

import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPOSITORY_ROOT))

from student_framework import build_agent


DEFAULT_TRIALS = 30


def _compact(value: str, limit: int = 100) -> str:
    """Compacta respuestas anormalmente largas para la salida de terminal."""

    value = value.replace("\n", "\\n")

    if len(value) <= limit:
        return repr(value)

    return repr(value[:limit] + "...")


def _read_trials() -> int:
    """Lee una cantidad opcional de intentos desde la línea de comandos."""

    if len(sys.argv) == 1:
        return DEFAULT_TRIALS

    if len(sys.argv) != 2:
        raise SystemExit(
            "Uso: python "
            "student_framework/tests/manual/"
            "validate_run_final_response_history.py [intentos]"
        )

    try:
        trials = int(sys.argv[1])
    except ValueError as error:
        raise SystemExit("La cantidad de intentos debe ser un entero.") from error

    if trials <= 0:
        raise SystemExit("La cantidad de intentos debe ser mayor que cero.")

    return trials


def main() -> None:
    trials = _read_trials()
    stored_count = 0
    recalled_count = 0

    for attempt in range(1, trials + 1):
        word_length = 5 + (attempt - 1) % 10
        agent = build_agent()

        first = agent.run(
            f"Inventá una única palabra inexistente de exactamente "
            f"{word_length} letras. Respondé exclusivamente con la palabra: "
            "sin comillas, sin signos de puntuación, sin explicaciones, "
            "sin prefijos, sin texto adicional y sin usar herramientas."
        )

        first_answer = (first.answer or "").strip()

        stored_correctly = (
            bool(agent._history)
            and agent._history[-1]
            == {
                "role": "assistant",
                "content": first.answer,
            }
        )

        second = agent.run(
            "Repetí exactamente, carácter por carácter, la respuesta final "
            "del turno anterior. Respondé exclusivamente con esa misma "
            "palabra: sin comillas, sin signos de puntuación, sin "
            "explicaciones, sin prefijos, sin texto adicional y sin usar "
            "herramientas."
        )

        second_answer = (second.answer or "").strip()
        recalled_exactly = first_answer == second_answer

        if stored_correctly:
            stored_count += 1

        if recalled_exactly:
            recalled_count += 1

        print(f"Intento {attempt:02d}/{trials}")
        print(f"  Primera:  {_compact(first_answer)}")
        print(f"  Segunda:  {_compact(second_answer)}")
        print(
            "  Historial: "
            f"{'OK' if stored_correctly else 'FALLO'}"
        )
        print(
            "  Coincide:  "
            f"{'OK' if recalled_exactly else 'FALLO'}"
        )

    print()
    print("=== RESULTADO FINAL ===")
    print(f"Persistencia en historial: {stored_count}/{trials}")
    print(f"Recuperación literal:      {recalled_count}/{trials}")


if __name__ == "__main__":
    main()