from pathlib import Path

import pytest

import prohori_ai.interfaces.cli as cli


def test_cli_main_starts_workflow(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "",
    )

    cli.main()

    captured = capsys.readouterr()

    assert "Run ID:" in captured.out
