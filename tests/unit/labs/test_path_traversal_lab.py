from pathlib import Path

import pytest
from fastapi import HTTPException
from labs.path_traversal.app import main as lab


@pytest.fixture
def lab_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, Path]:
    public = tmp_path / "public"
    private = tmp_path / "private"

    public.mkdir()
    private.mkdir()

    (public / "readme.txt").write_text(
        "This file is intentionally public.\n",
        encoding="utf-8",
    )

    (private / "proof.txt").write_text(
        "PROHORI_PATH_TRAVERSAL_PROOF",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        lab,
        "PUBLIC_DIR",
        public,
    )

    return public, private


def test_vulnerable_reader_allows_public_file(
    lab_files: tuple[Path, Path],
) -> None:

    del lab_files

    result = lab.read_file_vulnerable("readme.txt")

    assert result == "This file is intentionally public.\n"


def test_vulnerable_reader_reproduces_path_traversal(
    lab_files: tuple[Path, Path],
) -> None:
    del lab_files

    result = lab.read_file_vulnerable("../private/proof.txt")

    assert result == "PROHORI_PATH_TRAVERSAL_PROOF"


def test_remediated_reader_allows_public_file(
    lab_files: tuple[Path, Path],
) -> None:
    del lab_files

    result = lab.read_file_remediated("readme.txt")

    assert result == "This file is intentionally public.\n"


def test_remediated_reader_blocks_path_traversal(lab_files: tuple[Path, Path]) -> None:
    del lab_files

    with pytest.raises(
        HTTPException,
    ) as exc_info:
        lab.read_file_remediated("../private/proof.txt")

    assert exc_info.value.status_code == 403


def test_remediated_reader_blocks_absolute_escape(lab_files: tuple[Path, Path]) -> None:
    _, private = lab_files

    with pytest.raises(
        HTTPException,
    ) as exc_info:
        lab.read_file_remediated(str(private / "proof.txt"))
    assert exc_info.value.status_code == 403
