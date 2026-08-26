import pytest

from prohori_ai.main import main


def test_main_prints_project_name(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main()

    captured = capsys.readouterr()

    assert captured.out == "Prohori AI\n"
