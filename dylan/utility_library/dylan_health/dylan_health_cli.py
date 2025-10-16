"""CLI interface for Dylan health check command.

This module defines the Typer command interface for running health checks
from the command line.
"""

import sys

import typer
from rich.console import Console

from dylan.utility_library.dylan_health.dylan_health_runner import (
    format_results_json,
    format_results_table,
    run_all_checks,
)
from dylan.utility_library.shared.error_handling import handle_dylan_errors
from dylan.utility_library.shared.ui_theme import COLORS

console = Console()


@handle_dylan_errors(utility_name="health")
def health(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed output including additional information for each check",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output results in JSON format for scripting and automation",
    ),
) -> None:
    """Check system health and dependencies.

    Performs comprehensive diagnostics on your Dylan development environment,
    verifying that all required dependencies (Git, GitHub CLI, Claude Code)
    are properly installed and configured.

    Args:
        verbose: If True, displays detailed output with extra information.
        json_output: If True, outputs results in JSON format instead of table.

    Returns:
        None. Exits with code 0 if healthy, 1 if unhealthy.
    """
    # Run all health checks
    report = run_all_checks()

    # Output results based on format
    if json_output:
        # JSON output mode
        json_str = format_results_json(report)
        console.print(json_str)
    else:
        # Table output mode
        console.print()  # Empty line for spacing
        table = format_results_table(report)
        console.print(table)

        # Show detailed info in verbose mode
        if verbose:
            console.print(f"\n[bold {COLORS['primary']}]Detailed Information:[/]")
            for result in report.results:
                if result.details:
                    console.print(f"  [{COLORS['muted']}]• {result.name}:[/] {result.details}")

        # Display overall summary
        console.print()
        if report.overall_healthy:
            console.print(
                f"[{COLORS['success']}]✓ Environment is healthy![/] All checks passed or have minor warnings."
            )
        else:
            console.print(
                f"[{COLORS['error']}]✗ Environment has issues.[/] Please address the failed checks above."
            )
        console.print()

    # Exit with appropriate code
    sys.exit(0 if report.overall_healthy else 1)
