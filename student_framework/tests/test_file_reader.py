import os
from pathlib import Path

import pytest

from student_framework.tools.file_reader import (
    _DirectoryEntry,
    _DirectoryListing,
    _FileReaderPathError,
    _format_directory_listing,
    _list_directory_entries,
    _resolve_safe_path,
    file_reader,
)


#--------------------------------------------------------------------------------------------------------
# Tests sobre _resolve_safe_path(...)
#--------------------------------------------------------------------------------------------------------


def test_resolve_safe_path_accepts_relative_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    resolved = _resolve_safe_path("documents/report.txt")

    assert resolved == tmp_path / "documents" / "report.txt"


@pytest.mark.parametrize("path", ["", "   "])
def test_resolve_safe_path_rejects_empty_path(
    path: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    with pytest.raises(_FileReaderPathError, match="vacía"):
        _resolve_safe_path(path)


@pytest.mark.parametrize(
    "path",
    [
        "/etc/passwd",
        r"C:\Windows\system.ini",
        r"\\server\share\file.txt",
    ],
)
def test_resolve_safe_path_rejects_absolute_paths(
    path: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    with pytest.raises(_FileReaderPathError, match="absoluta"):
        _resolve_safe_path(path)


@pytest.mark.parametrize(
    "path",
    [
        "../secret.txt",
        "documents/../secret.txt",
        r"..\secret.txt",
    ],
)
def test_resolve_safe_path_rejects_parent_navigation(
    path: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    with pytest.raises(_FileReaderPathError, match=r"\.\."):
        _resolve_safe_path(path)


def test_resolve_safe_path_rejects_symlink_escape(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sandbox = tmp_path / "sandbox"
    outside = tmp_path / "outside"

    sandbox.mkdir()
    outside.mkdir()
    (sandbox / "external").symlink_to(outside, target_is_directory=True)

    monkeypatch.chdir(sandbox)

    with pytest.raises(_FileReaderPathError, match="fuera del sandbox"):
        _resolve_safe_path("external/secret.txt")


#--------------------------------------------------------------------------------------------------------
# Tests sobre _list_directory_entries(...)
#--------------------------------------------------------------------------------------------------------


def test_list_directory_entries_returns_sorted_immediate_entries(
    tmp_path: Path,
) -> None:
    (tmp_path / "Beta.txt").write_text("beta", encoding="utf-8")
    (tmp_path / "alpha.txt").write_text("alpha", encoding="utf-8")
    (tmp_path / ".hidden").write_text("hidden", encoding="utf-8")

    nested_directory = tmp_path / "documents"
    nested_directory.mkdir()
    (nested_directory / "nested.txt").write_text("nested", encoding="utf-8")

    result = _list_directory_entries(tmp_path)

    assert result == _DirectoryListing(
        entries=(
            _DirectoryEntry(name=".hidden", kind="file"),
            _DirectoryEntry(name="alpha.txt", kind="file"),
            _DirectoryEntry(name="Beta.txt", kind="file"),
            _DirectoryEntry(name="documents", kind="directory"),
        ),
        total_count=4,
        truncated=False,
    )


def test_list_directory_entries_classifies_symlinks_without_following_them(
    tmp_path: Path,
) -> None:
    target_file = tmp_path / "target.txt"
    target_file.write_text("content", encoding="utf-8")

    target_directory = tmp_path / "target_directory"
    target_directory.mkdir()

    (tmp_path / "file_link").symlink_to(target_file)
    (tmp_path / "directory_link").symlink_to(
        target_directory,
        target_is_directory=True,
    )
    (tmp_path / "broken_link").symlink_to(tmp_path / "missing.txt")

    result = _list_directory_entries(tmp_path)

    entries_by_name = {
        entry.name: entry.kind
        for entry in result.entries
    }

    assert entries_by_name["file_link"] == "symlink"
    assert entries_by_name["directory_link"] == "symlink"
    assert entries_by_name["broken_link"] == "symlink"


def test_list_directory_entries_applies_limit_after_sorting(
    tmp_path: Path,
) -> None:
    for name in ["delta.txt", "beta.txt", "charlie.txt", "alpha.txt"]:
        (tmp_path / name).write_text(name, encoding="utf-8")

    result = _list_directory_entries(tmp_path, limit=2)

    assert result == _DirectoryListing(
        entries=(
            _DirectoryEntry(name="alpha.txt", kind="file"),
            _DirectoryEntry(name="beta.txt", kind="file"),
        ),
        total_count=4,
        truncated=True,
    )


def test_list_directory_entries_returns_empty_listing(
    tmp_path: Path,
) -> None:
    result = _list_directory_entries(tmp_path)

    assert result == _DirectoryListing(
        entries=(),
        total_count=0,
        truncated=False,
    )


def test_list_directory_entries_does_not_mark_exact_limit_as_truncated(
    tmp_path: Path,
) -> None:
    (tmp_path / "a.txt").touch()
    (tmp_path / "b.txt").touch()

    result = _list_directory_entries(tmp_path, limit=2)

    assert len(result.entries) == 2
    assert result.total_count == 2
    assert result.truncated is False


@pytest.mark.parametrize(
    "limit",
    [
        0,
        -1,
        1.5,
        "20",
        True,
        False,
        None,
    ],
)
def test_list_directory_entries_rejects_invalid_limit(
    limit: object,
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="entero positivo"):
        _list_directory_entries(tmp_path, limit=limit)  # type: ignore[arg-type]


def test_list_directory_entries_rejects_missing_directory(
    tmp_path: Path,
) -> None:
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileNotFoundError, match="No existe el directorio"):
        _list_directory_entries(missing_directory)


def test_list_directory_entries_rejects_regular_file(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "file.txt"
    file_path.write_text("content", encoding="utf-8")

    with pytest.raises(
        NotADirectoryError,
        match="no corresponde a un directorio",
    ):
        _list_directory_entries(file_path)


#--------------------------------------------------------------------------------------------------------
# Tests sobre _format_directory_listing(...)
#--------------------------------------------------------------------------------------------------------


def test_format_directory_listing_formats_entries() -> None:
    listing = _DirectoryListing(
        entries=(
            _DirectoryEntry(name="data", kind="directory"),
            _DirectoryEntry(name="report.txt", kind="file"),
            _DirectoryEntry(name="shared", kind="symlink"),
            _DirectoryEntry(name="socket", kind="other"),
        ),
        total_count=4,
        truncated=False,
    )

    result = _format_directory_listing(listing)

    assert result == (
        "Entradas disponibles: "
        "'data' (directorio), "
        "'report.txt' (archivo), "
        "'shared' (enlace simbólico), "
        "'socket' (otro tipo de entrada)."
    )


def test_format_directory_listing_formats_empty_directory() -> None:
    listing = _DirectoryListing(
        entries=(),
        total_count=0,
        truncated=False,
    )

    result = _format_directory_listing(listing)

    assert result == "El directorio está vacío."


def test_format_directory_listing_reports_truncation() -> None:
    listing = _DirectoryListing(
        entries=(
            _DirectoryEntry(name="a.txt", kind="file"),
            _DirectoryEntry(name="b.txt", kind="file"),
        ),
        total_count=5,
        truncated=True,
    )

    result = _format_directory_listing(listing)

    assert result == (
        "Entradas disponibles: "
        "'a.txt' (archivo), "
        "'b.txt' (archivo). "
        "Se muestran 2 de 5 entradas; se omitieron 3."
    )


#--------------------------------------------------------------------------------------------------------
# Tests sobre file_reader(...)
#--------------------------------------------------------------------------------------------------------


def test_file_reader_reads_utf8_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    file_path = tmp_path / "report.txt"
    file_path.write_text("Contenido del informe.", encoding="utf-8")

    result = file_reader("report.txt")

    assert result == "Contenido del informe."


def test_file_reader_returns_recoverable_path_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    result = file_reader("../secret.txt")

    assert "contiene '..'" in result
    assert "ruta relativa" in result
    assert "sandbox" in result


def test_file_reader_lists_parent_entries_when_file_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    documents = tmp_path / "documents"
    documents.mkdir()
    (documents / "report.txt").write_text("content", encoding="utf-8")
    (documents / "data").mkdir()

    result = file_reader("documents/reprot.txt")

    assert "No existe el archivo 'documents/reprot.txt'" in result
    assert "El directorio contenedor 'documents' sí existe" in result
    assert "'data' (directorio)" in result
    assert "'report.txt' (archivo)" in result
    assert "volvé a invocar file_reader" in result


def test_file_reader_reports_missing_parent_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    result = file_reader("missing/report.txt")

    assert "No existe el archivo 'missing/report.txt'" in result
    assert "tampoco existe su directorio contenedor 'missing'" in result
    assert "ruta relativa válida" in result


def test_file_reader_reports_non_directory_parent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    (tmp_path / "container.txt").write_text("content", encoding="utf-8")

    result = file_reader("container.txt/report.txt")

    assert "No existe el archivo 'container.txt/report.txt'" in result
    assert "ruta contenedora 'container.txt'" in result
    assert "no corresponde a un directorio" in result


def test_file_reader_lists_entries_when_path_is_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    documents = tmp_path / "documents"
    documents.mkdir()
    (documents / "report.txt").write_text("content", encoding="utf-8")
    (documents / "data").mkdir()

    result = file_reader("documents")

    assert "La ruta 'documents' apunta a un directorio" in result
    assert "'data' (directorio)" in result
    assert "'report.txt' (archivo)" in result
    assert "entrada de tipo archivo" in result


def test_file_reader_reports_empty_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    (tmp_path / "empty").mkdir()

    result = file_reader("empty")

    assert "La ruta 'empty' apunta a un directorio" in result
    assert "El directorio está vacío." in result


def test_file_reader_reports_truncated_directory_listing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    documents = tmp_path / "documents"
    documents.mkdir()

    for index in range(21):
        (documents / f"file_{index:02d}.txt").touch()

    result = file_reader("documents")

    assert "Se muestran 20 de 21 entradas" in result
    assert "se omitieron 1" in result
    assert "'file_19.txt' (archivo)" in result
    assert "'file_20.txt' (archivo)" not in result


@pytest.mark.skipif(
    not hasattr(os, "mkfifo"),
    reason="El sistema operativo no permite crear archivos FIFO.",
)
def test_file_reader_reports_non_regular_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    fifo_path = tmp_path / "input_pipe"
    os.mkfifo(fifo_path)

    result = file_reader("input_pipe")

    assert "La ruta 'input_pipe' existe" in result
    assert "no corresponde a un archivo regular" in result
    assert "archivo compatible" in result


def test_file_reader_reports_non_utf8_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    (tmp_path / "binary.dat").write_bytes(b"\xff\xfe\x00")

    result = file_reader("binary.dat")

    assert "El archivo 'binary.dat' existe" in result
    assert "no puede leerse como texto codificado en UTF-8" in result
    assert "otro archivo de texto UTF-8" in result