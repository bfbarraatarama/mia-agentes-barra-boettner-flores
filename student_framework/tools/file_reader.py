from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Annotated, Literal

from pydantic import Field

from mia_agents.types import ToolSchema


"""
Herramienta: lector de archivo.
Dada una ruta relativa al sandbox, lee un archivo de texto UTF-8 o devuelve
un mensaje accionable ante errores recuperables.
"""


class _FileReaderPathError(ValueError):
    """Indica un error recuperable en el argumento `path`."""


_DirectoryEntryKind = Literal["file", "directory", "symlink", "other"]


@dataclass(frozen=True)
class _DirectoryEntry:
    """Representa una entrada inmediata de un directorio."""

    name: str
    kind: _DirectoryEntryKind


@dataclass(frozen=True)
class _DirectoryListing:
    """Representa un listado de directorio, posiblemente truncado."""

    entries: tuple[_DirectoryEntry, ...]
    total_count: int
    truncated: bool


_DIRECTORY_ENTRY_KIND_LABELS: dict[_DirectoryEntryKind, str] = {
    "file": "archivo",
    "directory": "directorio",
    "symlink": "enlace simbólico",
    "other": "otro tipo de entrada",
}


def _resolve_safe_path(path: str) -> Path:
    """Resuelve una ruta relativa y verifica que permanezca en el sandbox.

    El sandbox es el directorio de trabajo actual. La ruta devuelta es
    absoluta y ya fue resuelta, incluidos los enlaces simbólicos existentes.

    Raises
    ------
    _FileReaderPathError
        Si `path` no es una cadena no vacía, es absoluta, contiene `..`
        o se resuelve fuera del sandbox.
    """
    if not isinstance(path, str):
        raise _FileReaderPathError(
            "La ruta debe ser una cadena de texto relativa al sandbox; "
            f"recibí {path!r} ({type(path).__name__})."
        )

    if not path.strip():
        raise _FileReaderPathError(
            "La ruta está vacía. Indicá una ruta relativa al sandbox, "
            "por ejemplo "
            "'student_framework/examples/file_reader_demo.txt'."
        )

    posix_path = PurePosixPath(path)
    windows_path = PureWindowsPath(path)

    if (
        posix_path.is_absolute()
        or windows_path.is_absolute()
        or bool(windows_path.drive)
        or bool(windows_path.root)
    ):
        raise _FileReaderPathError(
            f"La ruta {path!r} es absoluta. "
            "file_reader solo acepta rutas relativas al sandbox."
        )

    if ".." in posix_path.parts or ".." in windows_path.parts:
        raise _FileReaderPathError(
            f"La ruta {path!r} contiene '..', lo cual no está permitido. "
            "Usá una ruta relativa que permanezca dentro del sandbox."
        )

    sandbox_root = Path.cwd().resolve()
    resolved_path = (sandbox_root / Path(path)).resolve(strict=False)

    try:
        resolved_path.relative_to(sandbox_root)
    except ValueError as exc:
        raise _FileReaderPathError(
            f"La ruta {path!r} se resuelve fuera del sandbox, "
            "posiblemente mediante un enlace simbólico. "
            "Usá una ruta relativa que permanezca dentro del sandbox."
        ) from exc

    return resolved_path


def _list_directory_entries(
    directory: Path,
    limit: int = 20,
) -> _DirectoryListing:
    """Lista las entradas inmediatas de un directorio.

    Las entradas se ordenan alfabéticamente, sin distinguir mayúsculas de
    minúsculas como criterio principal, y se truncan al límite indicado.

    Parameters
    ----------
    directory
        Ruta segura que debe existir y corresponder a un directorio.
    limit
        Cantidad máxima de entradas devueltas. Debe ser un entero positivo.

    Raises
    ------
    ValueError
        Si `limit` no es un entero positivo.
    FileNotFoundError
        Si `directory` no existe.
    NotADirectoryError
        Si `directory` no corresponde a un directorio.
    """
    if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
        raise ValueError(
            "El límite de entradas debe ser un entero positivo; "
            f"recibí {limit!r}."
        )

    if not directory.exists():
        raise FileNotFoundError(f"No existe el directorio: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(
            f"La ruta no corresponde a un directorio: {directory}"
        )

    entries: list[_DirectoryEntry] = []

    for entry in directory.iterdir():
        if entry.is_symlink():
            kind: _DirectoryEntryKind = "symlink"
        elif entry.is_file():
            kind = "file"
        elif entry.is_dir():
            kind = "directory"
        else:
            kind = "other"

        entries.append(
            _DirectoryEntry(
                name=entry.name,
                kind=kind,
            )
        )

    entries.sort(
        key=lambda entry: (
            entry.name.casefold(),
            entry.name,
        )
    )

    total_count = len(entries)
    selected_entries = tuple(entries[:limit])

    return _DirectoryListing(
        entries=selected_entries,
        total_count=total_count,
        truncated=total_count > limit,
    )


def _format_directory_listing(listing: _DirectoryListing) -> str:
    """Formatea un listado de directorio para incluirlo en el resultado de una herramienta."""
    if listing.total_count == 0:
        return "El directorio está vacío."

    formatted_entries = ", ".join(
        f"{entry.name!r} ({_DIRECTORY_ENTRY_KIND_LABELS[entry.kind]})"
        for entry in listing.entries
    )

    message = f"Entradas disponibles: {formatted_entries}."

    if listing.truncated:
        omitted_count = listing.total_count - len(listing.entries)
        message += (
            f" Se muestran {len(listing.entries)} de "
            f"{listing.total_count} entradas; "
            f"se omitieron {omitted_count}."
        )

    return message


def file_reader(
    path: Annotated[
        str,
        Field(
            description=(
                "Ruta relativa al sandbox del archivo de texto UTF-8 a leer. "
                "No se permiten rutas absolutas ni componentes '..'."
            )
        ),
    ],
) -> str:
    """Lee un archivo de texto UTF-8 ubicado dentro del sandbox.

    La herramienta accede al sistema de archivos mediante una ruta relativa.
    No acepta rutas absolutas, componentes `..` ni rutas que escapen del
    sandbox. Ante errores recuperables devuelve información accionable para
    corregir la ruta y volver a invocar la herramienta.
    """
  
    try:
        file_path = _resolve_safe_path(path)
    except _FileReaderPathError as exc:
        return str(exc)

    if not file_path.exists():
        parent_directory = file_path.parent
        requested_parent = str(Path(path).parent)

        if parent_directory.exists() and parent_directory.is_dir():
            listing = _list_directory_entries(parent_directory)

            return (
                f"No existe el archivo {path!r}. "
                f"El directorio contenedor {requested_parent!r} sí existe. "
                f"{_format_directory_listing(listing)} "
                "Verificá el nombre y volvé a invocar file_reader con una "
                "ruta relativa que apunte a un archivo disponible."
            )

        if parent_directory.exists():
            return (
                f"No existe el archivo {path!r} porque su ruta contenedora "
                f"{requested_parent!r} no corresponde a un directorio. "
                "Verificá los componentes de la ruta y volvé a invocar "
                "file_reader con una ruta relativa válida."
            )

        return (
            f"No existe el archivo {path!r} y tampoco existe su directorio "
            f"contenedor {requested_parent!r}. "
            "Verificá los componentes de la ruta y volvé a invocar "
            "file_reader con una ruta relativa válida."
        )
    
    if file_path.is_dir():
        listing = _list_directory_entries(file_path)

        return (
            f"La ruta {path!r} apunta a un directorio, no a un archivo. "
            f"{_format_directory_listing(listing)} "
            "Volvé a invocar file_reader con una ruta relativa que apunte "
            "a una entrada de tipo archivo."
        )

    if not file_path.is_file():
        return (
            f"La ruta {path!r} existe, pero no corresponde a un archivo "
            "regular. file_reader solo puede leer archivos regulares de "
            "texto codificados en UTF-8. Volvé a invocar la herramienta "
            "con una ruta relativa que apunte a un archivo compatible."
        )
    
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return (
            f"El archivo {path!r} existe, pero no puede leerse como texto "
            "codificado en UTF-8. Volvé a invocar file_reader con una ruta "
            "relativa que apunte a otro archivo de texto UTF-8."
        )
  
file_reader_schema = ToolSchema.from_callable(file_reader)
