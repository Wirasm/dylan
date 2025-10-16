"""Pytest fixtures for the dylan_health module."""

import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from git import Repo


@pytest.fixture
def mock_subprocess_run(monkeypatch: pytest.MonkeyPatch) -> Callable[[dict[str, Any]], None]:
    """Mock subprocess.run for testing external commands.

    Returns:
        A function that configures the mock behavior based on command.
    """

    def _configure_mock(command_responses: dict[str, Any]) -> None:
        """Configure mock subprocess.run responses.

        Args:
            command_responses: Dictionary mapping command strings to response dicts.
                Each response dict can contain: stdout, stderr, returncode, exception.
        """

        def mock_run(cmd: list[str], *args: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
            cmd_key = " ".join(cmd)
            response = command_responses.get(cmd_key, {})

            if "exception" in response:
                raise response["exception"]

            return subprocess.CompletedProcess(
                args=cmd,
                returncode=response.get("returncode", 0),
                stdout=response.get("stdout", ""),
                stderr=response.get("stderr", ""),
            )

        monkeypatch.setattr(subprocess, "run", mock_run)

    return _configure_mock


@pytest.fixture
def temp_git_repo() -> Any:
    """Create a temporary git repository for testing.

    Returns:
        Path to the temporary repository directory.

    Yields:
        Path object pointing to the temporary git repository.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        repo = Repo.init(repo_path)

        # Create initial commit
        test_file = repo_path / "test.txt"
        test_file.write_text("test content")
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")

        # Add remote
        repo.create_remote("origin", "https://github.com/test/repo.git")

        yield repo_path


@pytest.fixture
def mock_git_repo(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Mock GitPython Repo for testing.

    Returns:
        MagicMock configured to behave like a git repository.
    """
    mock_repo = MagicMock()
    mock_repo.working_dir = "/fake/repo/path"
    mock_repo.is_dirty.return_value = False
    mock_repo.head.is_detached = False
    mock_repo.active_branch.name = "main"

    # Mock remotes as an object with both dict-like and attribute access
    mock_remote = MagicMock()
    mock_remote.urls = ["https://github.com/test/repo.git"]
    mock_remotes = MagicMock()
    mock_remotes.__contains__ = lambda self, key: key == "origin"
    mock_remotes.origin = mock_remote
    mock_repo.remotes = mock_remotes

    def mock_repo_init(*args: Any, **kwargs: Any) -> MagicMock:
        return mock_repo

    monkeypatch.setattr("dylan.utility_library.dylan_health.checks.Repo", mock_repo_init)

    return mock_repo


@pytest.fixture
def successful_git_version() -> dict[str, Any]:
    """Response for successful git --version command.

    Returns:
        Dict with stdout containing git version string.
    """
    return {
        "git --version": {
            "stdout": "git version 2.39.2",
            "returncode": 0,
        }
    }


@pytest.fixture
def successful_gh_version() -> dict[str, Any]:
    """Response for successful gh --version command.

    Returns:
        Dict with stdout containing gh version string.
    """
    return {
        "gh --version": {
            "stdout": "gh version 2.40.0 (2023-12-15)\n",
            "returncode": 0,
        },
        "gh auth status": {
            "stdout": "Logged in to github.com as testuser\n",
            "returncode": 0,
        },
    }


@pytest.fixture
def successful_claude_version() -> dict[str, Any]:
    """Response for successful claude --version command.

    Returns:
        Dict with stdout containing claude version string.
    """
    return {
        "claude --version": {
            "stdout": "Claude Code CLI v1.0.0",
            "returncode": 0,
        }
    }
