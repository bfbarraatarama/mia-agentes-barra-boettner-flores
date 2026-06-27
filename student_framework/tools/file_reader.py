from __future__ import annotations

from pathlib import Path
from typing import Annotated

from pydantic import Field

from mia_agents.types import ToolSchema

"""
Herramienta: lector de archivo.
Dada una ruta a un archivo de texto UTF-8, devuelve una cadena de caracteres con el contenido.
"""

def file_reader(
    path: Annotated[str, Field(description="Ruta del archivo de texto UTF-8 a leer.")],
) -> str:
    """Lee un archivo de texto UTF-8 y devuelve su contenido."""
  
    file_path = Path(path).expanduser()

    if not file_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    
    if not file_path.is_file():
        raise ValueError(f"La ruta no corresponde a un archivo regular: {path}")
    
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"El archivo no es texto UTF-8: {path}") from exc
  
  
file_reader_schema = ToolSchema.from_callable(file_reader)