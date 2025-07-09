from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture
from click.testing import CliRunner

from bluetex.cli import main as legacy_main
from bluetex.cli.main import main as click_main


@pytest.fixture()
def infiles(tmp_path: Path):
    tmp_files = [tmp_path / f"infile_{i}.tex" for i in range(1, 4)]
    [tmp_file.write_text(f"{tmp_file.name}\na+b=c") for tmp_file in tmp_files]
    yield tmp_files


# Tests for the legacy CLI (accessed through bluetex.cli.main which imports from legacy_cli)
def test_cli_stdout(infiles: list[Path], capsys: CaptureFixture):
    infile = infiles[0]

    return_value = legacy_main([str(infile)])

    sdtout, _ = capsys.readouterr()

    assert return_value == 0
    assert sdtout == "infile_1.tex\na+b = c"
    assert infile.read_text() == "infile_1.tex\na+b=c"


def test_cli_encoding(tmp_path: Path):
    infile = tmp_path / "infile_encoding.tex"
    result = "äöüéкий的"
    infile.write_text(result, encoding="utf8")

    return_value = legacy_main(["-i", "-e", "utf8", str(infile)])

    assert return_value == 0
    assert infile.read_text(encoding="utf8") == result


def test_cli_inplace(infiles: list[Path]):
    infile = infiles[0]

    return_value = legacy_main(["-i", str(infile)])

    assert return_value == 1
    assert infile.read_text() == "infile_1.tex\na+b = c"


def test_cli_multiple_files(infiles: list[Path]):
    return_value = legacy_main(["-i", *[str(infile) for infile in infiles]])

    assert return_value == 1
    for infile in infiles:
        assert infile.read_text() == f"{infile.name}\na+b = c"


# Tests for the new Click-based CLI
def test_click_cli_stdout(infiles: list[Path]):
    """Test new Click CLI with stdout output."""
    runner = CliRunner()
    infile = infiles[0]

    result = runner.invoke(click_main, [str(infile)])

    assert result.exit_code == 0
    assert result.output == "infile_1.tex\na+b = c"
    # Original file should be unchanged
    assert infile.read_text() == "infile_1.tex\na+b=c"


def test_click_cli_inplace(infiles: list[Path]):
    """Test new Click CLI with in-place modification."""
    runner = CliRunner()
    infile = infiles[0]

    result = runner.invoke(click_main, ["-i", str(infile)])

    assert result.exit_code == 1  # Changed files return 1
    assert infile.read_text() == "infile_1.tex\na+b = c"


def test_click_cli_multiple_files(infiles: list[Path]):
    """Test new Click CLI with multiple files."""
    runner = CliRunner()

    result = runner.invoke(click_main, ["-i", *[str(infile) for infile in infiles]])

    assert result.exit_code == 1  # Changed files return 1
    for infile in infiles:
        assert infile.read_text() == f"{infile.name}\na+b = c"


def test_click_cli_encoding(tmp_path: Path):
    """Test new Click CLI with custom encoding."""
    runner = CliRunner()
    infile = tmp_path / "infile_encoding.tex"
    result = "äöüéкий的"
    infile.write_text(result, encoding="utf8")

    result_run = runner.invoke(click_main, ["-i", "-e", "utf8", str(infile)])

    assert result_run.exit_code == 0
    assert infile.read_text(encoding="utf8") == result


def test_click_cli_keep_comments(tmp_path: Path):
    """Test new Click CLI with keep comments option."""
    runner = CliRunner()
    infile = tmp_path / "infile_comments.tex"
    infile.write_text("a+b=c % comment\n")

    result = runner.invoke(click_main, ["-c", str(infile)])

    assert result.exit_code == 0
    assert "% comment" in result.output


def test_click_cli_keep_dollar(tmp_path: Path):
    """Test new Click CLI with keep dollar option."""
    runner = CliRunner()
    infile = tmp_path / "infile_dollar.tex"
    infile.write_text("a $b+c$ d")

    result = runner.invoke(click_main, ["-d", str(infile)])

    assert result.exit_code == 0
    assert "$b+c$" in result.output


def test_click_cli_logfile(tmp_path: Path):
    """Test new Click CLI with log file option."""
    runner = CliRunner()
    infile = tmp_path / "infile.tex"
    infile.write_text("a+b=c")
    logfile = tmp_path / "test.log"

    result = runner.invoke(
        click_main, ["--logfile", str(logfile), "--loglevel", "DEBUG", str(infile)]
    )

    assert result.exit_code == 0
    assert logfile.exists()
    log_content = logfile.read_text()
    assert "Processing" in log_content


def test_click_cli_loglevel(tmp_path: Path):
    """Test new Click CLI with different log levels."""
    runner = CliRunner()
    infile = tmp_path / "infile.tex"
    infile.write_text("a+b=c")

    # Test with DEBUG level
    result = runner.invoke(click_main, ["--loglevel", "DEBUG", str(infile)])
    assert result.exit_code == 0

    # Test with ERROR level
    result = runner.invoke(click_main, ["--loglevel", "ERROR", str(infile)])
    assert result.exit_code == 0


def test_click_cli_version():
    """Test new Click CLI version option."""
    runner = CliRunner()

    result = runner.invoke(click_main, ["--version"])

    assert result.exit_code == 0
    assert "bluetex" in result.output
    assert "Python" in result.output


def test_click_cli_help():
    """Test new Click CLI help option."""
    runner = CliRunner()

    result = runner.invoke(click_main, ["--help"])

    assert result.exit_code == 0
    assert "Clean up LaTeX files" in result.output
    assert "--in-place" in result.output
    assert "--encoding" in result.output


def test_click_cli_nonexistent_file():
    """Test new Click CLI with non-existent file."""
    runner = CliRunner()

    result = runner.invoke(click_main, ["nonexistent.tex"])

    assert result.exit_code != 0
    assert "does not exist" in result.output or "No such file" in result.output


def test_click_cli_error_handling(tmp_path: Path):
    """Test new Click CLI error handling."""
    runner = CliRunner()

    # Create a directory where we expect a file
    dir_path = tmp_path / "directory"
    dir_path.mkdir()

    # Try to process a directory as a file
    result = runner.invoke(click_main, [str(dir_path)])

    # Should handle the error gracefully
    assert result.exit_code != 0
