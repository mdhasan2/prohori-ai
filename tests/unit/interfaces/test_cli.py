import sys
from pathlib import Path

import pytest

import prohori_ai.interfaces.cli as cli


def test_cli_main_starts_workflow(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # Use a temporary directory for SQLite checkpoint and approvals.
    monkeypatch.chdir(tmp_path)

    # Prevent argparse from reading pytest's -v and other arguments.
    monkeypatch.setattr(
        sys,
        "argv",
        ["prohori-ai"],
    )

    # Press Enter at the investigation approval prompt.
    # An empty response means reject.
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "",
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Run ID:" in output
    assert "Target" in output
    assert "Controlled validation:" in output
    assert '"gate": "investigation"' in output
    assert '"status": "cancelled"' in output
