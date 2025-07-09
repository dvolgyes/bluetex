"""Tests for the legacy CLI implementation.

This module contains tests for the legacy argparse-based CLI to ensure
backward compatibility is maintained.
"""

from pathlib import Path

import pytest

from bluetex.legacy_cli import main as legacy_main


@pytest.fixture()
def infiles(tmp_path: Path):
    """Create temporary test files."""
    tmp_files = [tmp_path / f"infile_{i}.tex" for i in range(1, 4)]
    [tmp_file.write_text(f"{tmp_file.name}\na+b=c") for tmp_file in tmp_files]
    yield tmp_files


def test_legacy_cli_stdout(infiles: list[Path], capsys):
    """Test legacy CLI with stdout output."""
    infile = infiles[0]

    return_value = legacy_main([str(infile)])

    stdout, _ = capsys.readouterr()

    assert return_value == 0
    assert stdout == "infile_1.tex\na+b = c"
    # Original file should be unchanged
    assert infile.read_text() == "infile_1.tex\na+b=c"


def test_legacy_cli_inplace(infiles: list[Path]):
    """Test legacy CLI with in-place modification."""
    infile = infiles[0]

    return_value = legacy_main(["-i", str(infile)])

    assert return_value == 1  # Changed files return 1
    assert infile.read_text() == "infile_1.tex\na+b = c"


def test_legacy_cli_multiple_files(infiles: list[Path]):
    """Test legacy CLI with multiple files."""
    return_value = legacy_main(["-i", *[str(infile) for infile in infiles]])

    assert return_value == 1  # Changed files return 1
    for infile in infiles:
        assert infile.read_text() == f"{infile.name}\na+b = c"


def test_legacy_cli_encoding(tmp_path: Path):
    """Test legacy CLI with custom encoding."""
    infile = tmp_path / "infile_encoding.tex"
    test_content = "äöüéкий的"
    infile.write_text(test_content, encoding="utf8")

    return_value = legacy_main(["-i", "-e", "utf8", str(infile)])

    assert return_value == 0
    assert infile.read_text(encoding="utf8") == test_content


def test_legacy_cli_keep_comments(tmp_path: Path, capsys):
    """Test legacy CLI with keep comments option."""
    infile = tmp_path / "infile_comments.tex"
    infile.write_text("a+b=c % comment\n")

    return_value = legacy_main(["-c", str(infile)])

    stdout, _ = capsys.readouterr()

    assert return_value == 0
    assert "% comment" in stdout


def test_legacy_cli_keep_dollar(tmp_path: Path, capsys):
    """Test legacy CLI with keep dollar option."""
    infile = tmp_path / "infile_dollar.tex"
    infile.write_text("a $b+c$ d")

    return_value = legacy_main(["-d", str(infile)])

    stdout, _ = capsys.readouterr()

    assert return_value == 0
    assert "$b+c$" in stdout


def test_legacy_cli_version(capsys):
    """Test legacy CLI version option."""
    with pytest.raises(SystemExit) as excinfo:
        legacy_main(["--version"])

    assert excinfo.value.code == 0
    stdout, _ = capsys.readouterr()
    assert "bluetex" in stdout
    assert "Python" in stdout


def test_legacy_cli_help(capsys):
    """Test legacy CLI help option."""
    with pytest.raises(SystemExit) as excinfo:
        legacy_main(["--help"])

    assert excinfo.value.code == 0
    stdout, _ = capsys.readouterr()
    assert "Clean up LaTeX files" in stdout
    assert "--in-place" in stdout
    assert "--encoding" in stdout
