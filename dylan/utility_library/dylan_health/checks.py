"""Individual health check functions for Dylan CLI.

This module contains all individual health check functions that verify
the state of dependencies, repository configuration, and project structure.
Each check returns a standardized HealthCheckResult object.
"""

import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from git import GitError, InvalidGitRepositoryError, Repo


class HealthCheckStatus(Enum):
    """Status of a health check result."""

    PASS = "pass"  # noqa: S105 - Not a password, just an enum value
    FAIL = "fail"
    WARN = "warn"


@dataclass
class HealthCheckResult:
    """Result of an individual health check.

    Attributes:
        name: Human-readable name of the check.
        status: Status of the check (PASS, FAIL, or WARN).
        message: Brief description of the result.
        details: Optional additional information about the check result.
    """

    name: str
    status: HealthCheckStatus
    message: str
    details: str | None = None


def check_git_installed() -> HealthCheckResult:
    """Check if Git is installed and accessible.

    Returns:
        HealthCheckResult with Git version if installed, error message otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        version = result.stdout.strip()
        return HealthCheckResult(
            name="Git Installation",
            status=HealthCheckStatus.PASS,
            message=f"Git is installed: {version}",
            details=version,
        )
    except FileNotFoundError:
        return HealthCheckResult(
            name="Git Installation",
            status=HealthCheckStatus.FAIL,
            message="Git is not installed or not in PATH",
            details="Install Git from https://git-scm.com/",
        )
    except subprocess.TimeoutExpired:
        return HealthCheckResult(
            name="Git Installation",
            status=HealthCheckStatus.FAIL,
            message="Git command timed out",
            details="Git may be installed but not responding",
        )
    except subprocess.CalledProcessError as e:
        return HealthCheckResult(
            name="Git Installation",
            status=HealthCheckStatus.FAIL,
            message="Git command failed",
            details=f"Error: {e.stderr}",
        )


def check_git_repo() -> HealthCheckResult:
    """Check if current directory is a Git repository.

    Returns:
        HealthCheckResult with repository path if valid, error message otherwise.
    """
    try:
        repo = Repo(".", search_parent_directories=True)
        repo_path = Path(repo.working_dir).resolve()
        return HealthCheckResult(
            name="Git Repository",
            status=HealthCheckStatus.PASS,
            message="Current directory is a Git repository",
            details=str(repo_path),
        )
    except InvalidGitRepositoryError:
        return HealthCheckResult(
            name="Git Repository",
            status=HealthCheckStatus.FAIL,
            message="Not a Git repository",
            details="Run 'git init' to initialize a repository",
        )
    except GitError as e:
        return HealthCheckResult(
            name="Git Repository",
            status=HealthCheckStatus.FAIL,
            message="Error accessing Git repository",
            details=str(e),
        )


def check_git_branch() -> HealthCheckResult:
    """Check current Git branch and working tree status.

    Returns:
        HealthCheckResult with branch name and clean/dirty status.
    """
    try:
        repo = Repo(".", search_parent_directories=True)

        # Handle detached HEAD state
        if repo.head.is_detached:
            return HealthCheckResult(
                name="Git Branch",
                status=HealthCheckStatus.WARN,
                message="Repository is in detached HEAD state",
                details=f"Current commit: {repo.head.commit.hexsha[:7]}",
            )

        branch_name = repo.active_branch.name
        is_dirty = repo.is_dirty()

        if is_dirty:
            status_text = "has uncommitted changes"
            details = f"Branch: {branch_name} (dirty)"
        else:
            status_text = "is clean"
            details = f"Branch: {branch_name} (clean)"

        return HealthCheckResult(
            name="Git Branch",
            status=HealthCheckStatus.PASS,
            message=f"On branch '{branch_name}' - working tree {status_text}",
            details=details,
        )
    except InvalidGitRepositoryError:
        return HealthCheckResult(
            name="Git Branch",
            status=HealthCheckStatus.FAIL,
            message="Not in a Git repository",
            details="Cannot check branch status",
        )
    except GitError as e:
        return HealthCheckResult(
            name="Git Branch",
            status=HealthCheckStatus.FAIL,
            message="Error checking branch status",
            details=str(e),
        )


def check_git_remote() -> HealthCheckResult:
    """Check if Git remote 'origin' is configured.

    Returns:
        HealthCheckResult with remote URL if configured, warning otherwise.
    """
    try:
        repo = Repo(".", search_parent_directories=True)

        if "origin" not in repo.remotes:
            return HealthCheckResult(
                name="Git Remote",
                status=HealthCheckStatus.WARN,
                message="No 'origin' remote configured",
                details="Configure with: git remote add origin <url>",
            )

        origin = repo.remotes.origin
        remote_url = list(origin.urls)[0] if origin.urls else "No URL"

        return HealthCheckResult(
            name="Git Remote",
            status=HealthCheckStatus.PASS,
            message="Remote 'origin' is configured",
            details=remote_url,
        )
    except InvalidGitRepositoryError:
        return HealthCheckResult(
            name="Git Remote",
            status=HealthCheckStatus.FAIL,
            message="Not in a Git repository",
            details="Cannot check remote configuration",
        )
    except GitError as e:
        return HealthCheckResult(
            name="Git Remote",
            status=HealthCheckStatus.FAIL,
            message="Error checking remote configuration",
            details=str(e),
        )


def check_gh_cli_installed() -> HealthCheckResult:
    """Check if GitHub CLI is installed and authenticated.

    Returns:
        HealthCheckResult indicating installation and authentication status.
    """
    # First check if gh is installed
    try:
        result = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        version = result.stdout.strip().split("\n")[0]
    except FileNotFoundError:
        return HealthCheckResult(
            name="GitHub CLI",
            status=HealthCheckStatus.FAIL,
            message="GitHub CLI is not installed",
            details="Install from https://cli.github.com/",
        )
    except subprocess.TimeoutExpired:
        return HealthCheckResult(
            name="GitHub CLI",
            status=HealthCheckStatus.FAIL,
            message="GitHub CLI command timed out",
            details="gh may be installed but not responding",
        )
    except subprocess.CalledProcessError as e:
        return HealthCheckResult(
            name="GitHub CLI",
            status=HealthCheckStatus.FAIL,
            message="GitHub CLI command failed",
            details=f"Error: {e.stderr}",
        )

    # Check authentication status
    try:
        subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        return HealthCheckResult(
            name="GitHub CLI",
            status=HealthCheckStatus.PASS,
            message=f"{version} - Authenticated",
            details="Authentication successful",
        )
    except subprocess.CalledProcessError:
        return HealthCheckResult(
            name="GitHub CLI",
            status=HealthCheckStatus.WARN,
            message=f"{version} - Not authenticated",
            details="Run 'gh auth login' to authenticate",
        )
    except subprocess.TimeoutExpired:
        return HealthCheckResult(
            name="GitHub CLI",
            status=HealthCheckStatus.WARN,
            message=f"{version} - Auth check timed out",
            details="Could not verify authentication status",
        )


def check_claude_code_installed() -> HealthCheckResult:
    """Check if Claude Code CLI is installed.

    Returns:
        HealthCheckResult with Claude version if installed, error message otherwise.
    """
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        version = result.stdout.strip()
        return HealthCheckResult(
            name="Claude Code CLI",
            status=HealthCheckStatus.PASS,
            message=f"Claude Code is installed: {version}",
            details=version,
        )
    except FileNotFoundError:
        return HealthCheckResult(
            name="Claude Code CLI",
            status=HealthCheckStatus.FAIL,
            message="Claude Code CLI is not installed",
            details="Install from https://claude.ai/code",
        )
    except subprocess.TimeoutExpired:
        return HealthCheckResult(
            name="Claude Code CLI",
            status=HealthCheckStatus.FAIL,
            message="Claude command timed out",
            details="Claude may be installed but not responding",
        )
    except subprocess.CalledProcessError as e:
        return HealthCheckResult(
            name="Claude Code CLI",
            status=HealthCheckStatus.FAIL,
            message="Claude command failed",
            details=f"Error: {e.stderr}",
        )


def check_project_structure() -> HealthCheckResult:
    """Check if expected project files exist.

    Returns:
        HealthCheckResult indicating which required files are present or missing.
    """
    required_files = ["pyproject.toml", "README.md", ".git"]
    missing_files = []

    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)

    if not missing_files:
        return HealthCheckResult(
            name="Project Structure",
            status=HealthCheckStatus.PASS,
            message="All required project files exist",
            details=f"Found: {', '.join(required_files)}",
        )

    if len(missing_files) == len(required_files):
        return HealthCheckResult(
            name="Project Structure",
            status=HealthCheckStatus.FAIL,
            message="No project files found",
            details=f"Missing: {', '.join(missing_files)}",
        )

    return HealthCheckResult(
        name="Project Structure",
        status=HealthCheckStatus.WARN,
        message="Some project files are missing",
        details=f"Missing: {', '.join(missing_files)}",
    )
