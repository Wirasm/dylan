"""Tests for the goodbye command CLI."""

from typer.testing import CliRunner

from dylan.utility_library.dylan_goodbye.dylan_goodbye_cli import goodbye

runner = CliRunner()


def test_goodbye_command_executes() -> None:
    """Test that the goodbye command executes without errors."""
    # Create a Typer app with the goodbye command for testing
    import typer

    app = typer.Typer()
    app.command()(goodbye)

    result = runner.invoke(app)

    assert result.exit_code == 0


def test_goodbye_output_content() -> None:
    """Test that the goodbye command outputs expected content."""
    # Create a Typer app with the goodbye command for testing
    import typer

    app = typer.Typer()
    app.command()(goodbye)

    result = runner.invoke(app)

    # Check that output contains the key elements
    assert "Goodbye!" in result.stdout
    assert "Thanks for using Dylan" in result.stdout
    assert "See you next time!" in result.stdout


def test_goodbye_accepts_no_arguments() -> None:
    """Test that the goodbye command works with no arguments."""
    # Create a Typer app with the goodbye command for testing
    import typer

    app = typer.Typer()
    app.command()(goodbye)

    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "Goodbye!" in result.stdout
