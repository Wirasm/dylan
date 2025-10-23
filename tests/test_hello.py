"""Unit tests for the hello.py script.

This module contains unit tests that verify the functionality of the hello.py
script, including output validation and function callability.
"""

import pytest

import hello


@pytest.mark.unit
def test_main_output(capsys) -> None:
    """Test that main() prints 'Hello, World!' to stdout.

    Args:
        capsys: Pytest fixture to capture stdout and stderr.
    """
    hello.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"
    assert captured.err == ""


@pytest.mark.unit
def test_main_callable() -> None:
    """Test that the main function is callable and has proper type annotations.

    Verifies that:
    - The main function can be imported
    - The function is callable
    - The function has the expected signature
    """
    assert callable(hello.main)

    # Verify function signature with type hints
    import inspect
    sig = inspect.signature(hello.main)
    assert sig.return_annotation == None or str(sig.return_annotation) == "None"


@pytest.mark.unit
def test_main_returns_none() -> None:
    """Test that main() returns None.

    Verifies that the function executes without errors and returns None as expected.
    """
    result = hello.main()
    assert result is None
