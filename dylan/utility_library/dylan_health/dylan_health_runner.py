"""Core runner logic for Dylan health checks.

This module orchestrates the execution of all health checks and formats
the results for display.
"""

import json
from dataclasses import dataclass
from typing import Any

from rich.table import Table

from dylan.utility_library.dylan_health.checks import (
    HealthCheckResult,
    HealthCheckStatus,
    check_claude_code_installed,
    check_gh_cli_installed,
    check_git_branch,
    check_git_installed,
    check_git_remote,
    check_git_repo,
    check_project_structure,
)
from dylan.utility_library.shared.ui_theme import COLORS


@dataclass
class HealthCheckReport:
    """Aggregated health check results.

    Attributes:
        results: List of individual health check results.
        overall_healthy: True if all checks passed or have warnings only.
    """

    results: list[HealthCheckResult]
    overall_healthy: bool


def run_all_checks() -> HealthCheckReport:
    """Execute all health checks and aggregate results.

    Returns:
        HealthCheckReport containing all check results and overall status.
    """
    results: list[HealthCheckResult] = []

    # Run all checks in sequence
    results.append(check_git_installed())
    results.append(check_git_repo())
    results.append(check_git_branch())
    results.append(check_git_remote())
    results.append(check_gh_cli_installed())
    results.append(check_claude_code_installed())
    results.append(check_project_structure())

    # Determine overall health - healthy if no FAIL status
    overall_healthy = all(
        result.status != HealthCheckStatus.FAIL for result in results
    )

    return HealthCheckReport(results=results, overall_healthy=overall_healthy)


def format_results_table(report: HealthCheckReport) -> Table:
    """Format health check results as a Rich table.

    Args:
        report: The health check report to format.

    Returns:
        Rich Table object with formatted results.
    """
    table = Table(
        title="Dylan Health Check Results",
        show_header=True,
        header_style=f"bold {COLORS['primary']}",
    )

    table.add_column("Check", style="bold", no_wrap=True)
    table.add_column("Status", justify="center", no_wrap=True)
    table.add_column("Message", style="dim")

    for result in report.results:
        # Determine status display and color
        if result.status == HealthCheckStatus.PASS:
            status_display = f"[{COLORS['success']}]✓ PASS[/]"
        elif result.status == HealthCheckStatus.WARN:
            status_display = f"[{COLORS['warning']}]⚠ WARN[/]"
        else:  # FAIL
            status_display = f"[{COLORS['error']}]✗ FAIL[/]"

        table.add_row(result.name, status_display, result.message)

    return table


def format_results_json(report: HealthCheckReport) -> str:
    """Format health check results as JSON.

    Args:
        report: The health check report to format.

    Returns:
        JSON string representation of the report.
    """
    output: dict[str, Any] = {
        "overall_healthy": report.overall_healthy,
        "checks": [
            {
                "name": result.name,
                "status": result.status.value,
                "message": result.message,
                "details": result.details,
            }
            for result in report.results
        ],
    }

    return json.dumps(output, indent=2)
