"""Tests for hello_world_test_from_archon module."""

import pytest

from hello_world_test_from_archon import greet


def test_greet_default() -> None:
    """Test greet function with default World parameter."""
    result = greet()
    assert result == "Hello, World!"
    assert isinstance(result, str)


def test_greet_custom_name() -> None:
    """Test greet function with custom name."""
    result = greet("Alice")
    assert result == "Hello, Alice!"
    assert isinstance(result, str)


def test_greet_return_value() -> None:
    """Test that greet returns correct string type and format."""
    result = greet("Bob")
    assert isinstance(result, str)
    assert result == "Hello, Bob!"
    assert result.startswith("Hello, ")
    assert result.endswith("!")


def test_greet_output(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that greet prints to stdout correctly."""
    greet("Charlie")
    captured = capsys.readouterr()
    assert captured.out == "Hello, Charlie!\n"


def test_greet_empty_string() -> None:
    """Test greet with empty string as name."""
    result = greet("")
    assert result == "Hello, !"
    assert isinstance(result, str)


def test_greet_special_characters() -> None:
    """Test greet with special characters and unicode."""
    result = greet("José")
    assert result == "Hello, José!"
    assert isinstance(result, str)


def test_greet_with_spaces() -> None:
    """Test greet with name containing spaces."""
    result = greet("Jane Doe")
    assert result == "Hello, Jane Doe!"
    assert isinstance(result, str)


def test_greet_unicode_emoji() -> None:
    """Test greet with emoji characters."""
    result = greet("Alice 👋")
    assert result == "Hello, Alice 👋!"
    assert isinstance(result, str)
