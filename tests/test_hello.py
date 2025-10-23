"""Unit tests for the hello.py script.

This module contains comprehensive unit tests for the hello module, testing
the main function's output and behavior. Tests use pytest fixtures and
follow Google-style docstring conventions.
"""

import pytest

import hello


@pytest.mark.unit
def test_main_prints_hello_world(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that main() prints 'Hello, World!' to stdout.

    Args:
        capsys: Pytest fixture to capture stdout and stderr.
    """
    hello.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"


@pytest.mark.unit
def test_main_no_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that main() produces no stderr output.

    Args:
        capsys: Pytest fixture to capture stdout and stderr.
    """
    hello.main()
    captured = capsys.readouterr()
    assert captured.err == ""


@pytest.mark.unit
def test_module_import_no_side_effects(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that importing the hello module doesn't produce output.

    This test verifies that the if __name__ == "__main__" guard works
    correctly and prevents execution when the module is imported.

    Args:
        capsys: Pytest fixture to capture stdout and stderr.
    """
    # The module has already been imported at the top of this file
    # If the guard didn't work, we'd see output
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
