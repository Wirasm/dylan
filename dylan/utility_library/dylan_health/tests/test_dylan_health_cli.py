"""Unit tests for health check CLI interface."""

from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from dylan.cli import app
from dylan.utility_library.dylan_health.checks import HealthCheckResult, HealthCheckStatus
from dylan.utility_library.dylan_health.dylan_health_runner import HealthCheckReport

runner = CliRunner()


@pytest.mark.unit
def test_health_command_success() -> None:
    """Test health command exits with 0 when environment is healthy."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Git Installation",
                status=HealthCheckStatus.PASS,
                message="Git is installed",
            ),
            HealthCheckResult(
                name="GitHub CLI",
                status=HealthCheckStatus.PASS,
                message="Authenticated",
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health"])

        assert result.exit_code == 0
        assert "healthy" in result.stdout.lower()


@pytest.mark.unit
def test_health_command_failure() -> None:
    """Test health command exits with 1 when environment has issues."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Git Installation",
                status=HealthCheckStatus.FAIL,
                message="Git is not installed",
            ),
            HealthCheckResult(
                name="GitHub CLI",
                status=HealthCheckStatus.PASS,
                message="Authenticated",
            ),
        ],
        overall_healthy=False,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health"])

        assert result.exit_code == 1
        assert "issues" in result.stdout.lower()


@pytest.mark.unit
def test_health_command_verbose() -> None:
    """Test health command with --verbose flag shows detailed output."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Git Installation",
                status=HealthCheckStatus.PASS,
                message="Git is installed",
                details="git version 2.39.2",
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health", "--verbose"])

        assert result.exit_code == 0
        assert "Detailed Information" in result.stdout
        assert "git version 2.39.2" in result.stdout


@pytest.mark.unit
def test_health_command_json() -> None:
    """Test health command with --json flag outputs valid JSON."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Git Installation",
                status=HealthCheckStatus.PASS,
                message="Git is installed",
                details="git version 2.39.2",
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health", "--json"])

        assert result.exit_code == 0
        # Verify JSON-like structure in output
        assert "overall_healthy" in result.stdout
        assert "checks" in result.stdout
        assert "Git Installation" in result.stdout


@pytest.mark.unit
def test_health_command_verbose_short_flag() -> None:
    """Test health command with -v short flag."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Test Check",
                status=HealthCheckStatus.PASS,
                message="OK",
                details="Extra details",
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health", "-v"])

        assert result.exit_code == 0
        assert "Detailed Information" in result.stdout
        assert "Extra details" in result.stdout


@pytest.mark.unit
def test_health_command_with_warnings() -> None:
    """Test health command with warnings still exits 0."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Git Branch",
                status=HealthCheckStatus.WARN,
                message="Detached HEAD state",
            ),
            HealthCheckResult(
                name="Git Installation",
                status=HealthCheckStatus.PASS,
                message="Installed",
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health"])

        assert result.exit_code == 0
        assert "healthy" in result.stdout.lower()


@pytest.mark.unit
def test_health_command_verbose_without_details() -> None:
    """Test verbose mode when some checks have no details."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Check With Details",
                status=HealthCheckStatus.PASS,
                message="OK",
                details="Some details",
            ),
            HealthCheckResult(
                name="Check Without Details",
                status=HealthCheckStatus.PASS,
                message="OK",
                details=None,
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health", "--verbose"])

        assert result.exit_code == 0
        assert "Some details" in result.stdout
        # Check that we only show details for checks that have them


@pytest.mark.unit
def test_health_command_help() -> None:
    """Test health command --help shows usage information."""
    result = runner.invoke(app, ["health", "--help"])

    assert result.exit_code == 0
    assert "Check system health and dependencies" in result.stdout
    assert "--verbose" in result.stdout
    assert "--json" in result.stdout


@pytest.mark.unit
def test_health_command_integration() -> None:
    """Test full health command through main CLI app."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Test Check",
                status=HealthCheckStatus.PASS,
                message="All good",
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health"])

        assert result.exit_code == 0
        mock_run.assert_called_once()


@pytest.mark.unit
def test_health_command_mixed_status() -> None:
    """Test health command with mixed check statuses."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Pass Check",
                status=HealthCheckStatus.PASS,
                message="OK",
            ),
            HealthCheckResult(
                name="Warn Check",
                status=HealthCheckStatus.WARN,
                message="Warning",
            ),
            HealthCheckResult(
                name="Fail Check",
                status=HealthCheckStatus.FAIL,
                message="Error",
            ),
        ],
        overall_healthy=False,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health"])

        assert result.exit_code == 1
        # Should contain table with all status types
        assert "PASS" in result.stdout or "✓" in result.stdout
        assert "WARN" in result.stdout or "⚠" in result.stdout
        assert "FAIL" in result.stdout or "✗" in result.stdout


@pytest.mark.unit
def test_health_command_json_with_failure() -> None:
    """Test JSON output when environment is unhealthy."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Failed Check",
                status=HealthCheckStatus.FAIL,
                message="Error occurred",
                details="Error details",
            ),
        ],
        overall_healthy=False,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = mock_report

        result = runner.invoke(app, ["health", "--json"])

        assert result.exit_code == 1
        assert '"overall_healthy": false' in result.stdout.lower()
        assert "Failed Check" in result.stdout


@pytest.mark.unit
def test_health_command_runs_all_checks() -> None:
    """Test that health command actually runs all checks."""
    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run:
        mock_run.return_value = HealthCheckReport(results=[], overall_healthy=True)

        runner.invoke(app, ["health"])

        # Verify run_all_checks was called
        mock_run.assert_called_once()


@pytest.mark.unit
def test_health_command_table_format() -> None:
    """Test that default output uses table format."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Test",
                status=HealthCheckStatus.PASS,
                message="OK",
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run, \
         patch("dylan.utility_library.dylan_health.dylan_health_cli.format_results_table") as mock_table:
        mock_run.return_value = mock_report

        runner.invoke(app, ["health"])

        # Verify table formatting was called
        mock_table.assert_called_once_with(mock_report)


@pytest.mark.unit
def test_health_command_json_format() -> None:
    """Test that --json flag uses JSON formatter."""
    mock_report = HealthCheckReport(
        results=[
            HealthCheckResult(
                name="Test",
                status=HealthCheckStatus.PASS,
                message="OK",
            ),
        ],
        overall_healthy=True,
    )

    with patch("dylan.utility_library.dylan_health.dylan_health_cli.run_all_checks") as mock_run, \
         patch("dylan.utility_library.dylan_health.dylan_health_cli.format_results_json") as mock_json:
        mock_run.return_value = mock_report
        mock_json.return_value = '{"test": "json"}'

        runner.invoke(app, ["health", "--json"])

        # Verify JSON formatting was called
        mock_json.assert_called_once_with(mock_report)
