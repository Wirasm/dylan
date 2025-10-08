#!/usr/bin/env python3
"""CLI interface for the goodbye command."""

from rich.console import Console

from ..shared.ui_theme import ARROW, COLORS, SPARK

console = Console()


def goodbye() -> None:
    """Print a friendly farewell message.

    Examples:
        # Say goodbye
        dylan goodbye
    """
    console.print(
        f"\n[{COLORS['primary']}]{ARROW}[/] [bold]Goodbye![/bold] [{COLORS['accent']}]{SPARK}[/]"
    )
    console.print("[dim]Thanks for using Dylan. See you next time![/dim]\n")
