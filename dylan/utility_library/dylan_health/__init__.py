"""Health check module for Dylan CLI.

This module provides comprehensive system diagnostics and health checks
for the Dylan development environment, verifying that all required
dependencies (Git, GitHub CLI, Claude Code) are properly installed and
configured.
"""

from dylan.utility_library.dylan_health.checks import (
    HealthCheckResult,
    HealthCheckStatus,
)
from dylan.utility_library.dylan_health.dylan_health_cli import health

__all__ = [
    "health",
    "HealthCheckResult",
    "HealthCheckStatus",
]
