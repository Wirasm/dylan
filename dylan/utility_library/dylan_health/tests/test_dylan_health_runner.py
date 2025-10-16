"""Unit tests for health check runner logic."""

import json
from unittest.mock import patch

import pytest
from rich.table import Table

from dylan.utility_library.dylan_health.checks import HealthCheckResult, HealthCheckStatus
from dylan.utility_library.dylan_health.dylan_health_runner import (
    HealthCheckReport,
    format_results_json,
    format_results_table,
    run_all_checks,
)


@pytest.mark.unit
def test_run_all_checks_all_pass() -> None:
    """Test run_all_checks when all checks return PASS."""
    with patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_installed") as mock_git, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_repo") as mock_repo, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_branch") as mock_branch, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_remote") as mock_remote, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_gh_cli_installed") as mock_gh, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_claude_code_installed") as mock_claude, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_project_structure") as mock_structure:

        # Configure all mocks to return PASS
        mock_git.return_value = HealthCheckResult(
            name="Git Installation", status=HealthCheckStatus.PASS, message="Git installed"
        )
        mock_repo.return_value = HealthCheckResult(
            name="Git Repository", status=HealthCheckStatus.PASS, message="Valid repo"
        )
        mock_branch.return_value = HealthCheckResult(
            name="Git Branch", status=HealthCheckStatus.PASS, message="On main"
        )
        mock_remote.return_value = HealthCheckResult(
            name="Git Remote", status=HealthCheckStatus.PASS, message="Remote configured"
        )
        mock_gh.return_value = HealthCheckResult(
            name="GitHub CLI", status=HealthCheckStatus.PASS, message="Authenticated"
        )
        mock_claude.return_value = HealthCheckResult(
            name="Claude Code", status=HealthCheckStatus.PASS, message="Installed"
        )
        mock_structure.return_value = HealthCheckResult(
            name="Project Structure", status=HealthCheckStatus.PASS, message="All files present"
        )

        report = run_all_checks()

        assert len(report.results) == 7
        assert report.overall_healthy is True
        assert all(r.status == HealthCheckStatus.PASS for r in report.results)


@pytest.mark.unit
def test_run_all_checks_with_failures() -> None:
    """Test run_all_checks when some checks return FAIL."""
    with patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_installed") as mock_git, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_repo") as mock_repo, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_branch") as mock_branch, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_remote") as mock_remote, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_gh_cli_installed") as mock_gh, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_claude_code_installed") as mock_claude, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_project_structure") as mock_structure:

        # Mix of PASS and FAIL
        mock_git.return_value = HealthCheckResult(
            name="Git Installation", status=HealthCheckStatus.FAIL, message="Not installed"
        )
        mock_repo.return_value = HealthCheckResult(
            name="Git Repository", status=HealthCheckStatus.PASS, message="Valid repo"
        )
        mock_branch.return_value = HealthCheckResult(
            name="Git Branch", status=HealthCheckStatus.PASS, message="On main"
        )
        mock_remote.return_value = HealthCheckResult(
            name="Git Remote", status=HealthCheckStatus.PASS, message="Remote configured"
        )
        mock_gh.return_value = HealthCheckResult(
            name="GitHub CLI", status=HealthCheckStatus.FAIL, message="Not installed"
        )
        mock_claude.return_value = HealthCheckResult(
            name="Claude Code", status=HealthCheckStatus.PASS, message="Installed"
        )
        mock_structure.return_value = HealthCheckResult(
            name="Project Structure", status=HealthCheckStatus.PASS, message="All files present"
        )

        report = run_all_checks()

        assert len(report.results) == 7
        assert report.overall_healthy is False
        assert sum(1 for r in report.results if r.status == HealthCheckStatus.FAIL) == 2


@pytest.mark.unit
def test_run_all_checks_with_warnings() -> None:
    """Test run_all_checks when some checks return WARN."""
    with patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_installed") as mock_git, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_repo") as mock_repo, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_branch") as mock_branch, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_remote") as mock_remote, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_gh_cli_installed") as mock_gh, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_claude_code_installed") as mock_claude, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_project_structure") as mock_structure:

        # All PASS except one WARN
        mock_git.return_value = HealthCheckResult(
            name="Git Installation", status=HealthCheckStatus.PASS, message="Installed"
        )
        mock_repo.return_value = HealthCheckResult(
            name="Git Repository", status=HealthCheckStatus.PASS, message="Valid repo"
        )
        mock_branch.return_value = HealthCheckResult(
            name="Git Branch", status=HealthCheckStatus.WARN, message="Detached HEAD"
        )
        mock_remote.return_value = HealthCheckResult(
            name="Git Remote", status=HealthCheckStatus.PASS, message="Remote configured"
        )
        mock_gh.return_value = HealthCheckResult(
            name="GitHub CLI", status=HealthCheckStatus.WARN, message="Not authenticated"
        )
        mock_claude.return_value = HealthCheckResult(
            name="Claude Code", status=HealthCheckStatus.PASS, message="Installed"
        )
        mock_structure.return_value = HealthCheckResult(
            name="Project Structure", status=HealthCheckStatus.PASS, message="All files present"
        )

        report = run_all_checks()

        assert len(report.results) == 7
        # Warnings don't make it unhealthy, only failures do
        assert report.overall_healthy is True
        assert sum(1 for r in report.results if r.status == HealthCheckStatus.WARN) == 2


@pytest.mark.unit
def test_format_results_table() -> None:
    """Test format_results_table creates a valid Rich table."""
    results = [
        HealthCheckResult(
            name="Test Check 1", status=HealthCheckStatus.PASS, message="Success"
        ),
        HealthCheckResult(
            name="Test Check 2", status=HealthCheckStatus.WARN, message="Warning"
        ),
        HealthCheckResult(
            name="Test Check 3", status=HealthCheckStatus.FAIL, message="Failed"
        ),
    ]
    report = HealthCheckReport(results=results, overall_healthy=False)

    table = format_results_table(report)

    assert isinstance(table, Table)
    assert table.title == "Dylan Health Check Results"
    assert len(table.columns) == 3
    # Check column names
    assert table.columns[0].header == "Check"
    assert table.columns[1].header == "Status"
    assert table.columns[2].header == "Message"


@pytest.mark.unit
def test_format_results_json() -> None:
    """Test format_results_json produces valid JSON."""
    results = [
        HealthCheckResult(
            name="Test Check 1",
            status=HealthCheckStatus.PASS,
            message="Success",
            details="Extra info",
        ),
        HealthCheckResult(
            name="Test Check 2",
            status=HealthCheckStatus.FAIL,
            message="Failed",
            details=None,
        ),
    ]
    report = HealthCheckReport(results=results, overall_healthy=False)

    json_str = format_results_json(report)

    # Parse JSON to verify it's valid
    data = json.loads(json_str)

    assert data["overall_healthy"] is False
    assert len(data["checks"]) == 2
    assert data["checks"][0]["name"] == "Test Check 1"
    assert data["checks"][0]["status"] == "pass"
    assert data["checks"][0]["message"] == "Success"
    assert data["checks"][0]["details"] == "Extra info"
    assert data["checks"][1]["status"] == "fail"
    assert data["checks"][1]["details"] is None


@pytest.mark.unit
def test_format_results_json_empty_report() -> None:
    """Test format_results_json with empty results."""
    report = HealthCheckReport(results=[], overall_healthy=True)

    json_str = format_results_json(report)
    data = json.loads(json_str)

    assert data["overall_healthy"] is True
    assert data["checks"] == []


@pytest.mark.unit
def test_health_check_report_dataclass() -> None:
    """Test HealthCheckReport dataclass attributes."""
    results = [
        HealthCheckResult(
            name="Test", status=HealthCheckStatus.PASS, message="Test message"
        )
    ]
    report = HealthCheckReport(results=results, overall_healthy=True)

    assert len(report.results) == 1
    assert report.overall_healthy is True
    assert report.results[0].name == "Test"


@pytest.mark.unit
def test_run_all_checks_calls_all_functions() -> None:
    """Test that run_all_checks calls all individual check functions."""
    with patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_installed") as mock_git, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_repo") as mock_repo, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_branch") as mock_branch, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_git_remote") as mock_remote, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_gh_cli_installed") as mock_gh, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_claude_code_installed") as mock_claude, \
         patch("dylan.utility_library.dylan_health.dylan_health_runner.check_project_structure") as mock_structure:

        # Set return values
        for mock in [mock_git, mock_repo, mock_branch, mock_remote, mock_gh, mock_claude, mock_structure]:
            mock.return_value = HealthCheckResult(
                name="Test", status=HealthCheckStatus.PASS, message="OK"
            )

        run_all_checks()

        # Verify all functions were called exactly once
        mock_git.assert_called_once()
        mock_repo.assert_called_once()
        mock_branch.assert_called_once()
        mock_remote.assert_called_once()
        mock_gh.assert_called_once()
        mock_claude.assert_called_once()
        mock_structure.assert_called_once()


@pytest.mark.unit
def test_format_results_table_with_all_status_types() -> None:
    """Test format_results_table handles all status types correctly."""
    results = [
        HealthCheckResult(
            name="Pass Check", status=HealthCheckStatus.PASS, message="All good"
        ),
        HealthCheckResult(
            name="Warn Check", status=HealthCheckStatus.WARN, message="Be careful"
        ),
        HealthCheckResult(
            name="Fail Check", status=HealthCheckStatus.FAIL, message="Error occurred"
        ),
    ]
    report = HealthCheckReport(results=results, overall_healthy=False)

    table = format_results_table(report)

    # Verify table was created successfully with all status types
    assert isinstance(table, Table)
    assert len(table.rows) == 3
