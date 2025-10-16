"""Unit tests for individual health check functions."""

import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from git import GitError, InvalidGitRepositoryError

from dylan.utility_library.dylan_health.checks import (
    HealthCheckStatus,
    check_claude_code_installed,
    check_gh_cli_installed,
    check_git_branch,
    check_git_installed,
    check_git_remote,
    check_git_repo,
    check_project_structure,
)


@pytest.mark.unit
def test_check_git_installed_success(
    mock_subprocess_run: Any, successful_git_version: dict[str, Any]
) -> None:
    """Test successful git installation check."""
    mock_subprocess_run(successful_git_version)

    result = check_git_installed()

    assert result.status == HealthCheckStatus.PASS
    assert "git version 2.39.2" in result.message
    assert result.name == "Git Installation"
    assert result.details is not None


@pytest.mark.unit
def test_check_git_installed_failure(mock_subprocess_run: Any) -> None:
    """Test git installation check when git is not found."""
    mock_subprocess_run(
        {
            "git --version": {
                "exception": FileNotFoundError("git not found"),
            }
        }
    )

    result = check_git_installed()

    assert result.status == HealthCheckStatus.FAIL
    assert "not installed" in result.message.lower()
    assert result.details is not None
    assert "https://git-scm.com/" in result.details


@pytest.mark.unit
def test_check_git_installed_timeout(mock_subprocess_run: Any) -> None:
    """Test git installation check when command times out."""
    mock_subprocess_run(
        {
            "git --version": {
                "exception": subprocess.TimeoutExpired(cmd="git --version", timeout=5),
            }
        }
    )

    result = check_git_installed()

    assert result.status == HealthCheckStatus.FAIL
    assert "timed out" in result.message.lower()


@pytest.mark.unit
def test_check_git_repo_success(mock_git_repo: MagicMock) -> None:
    """Test successful git repository check."""
    result = check_git_repo()

    assert result.status == HealthCheckStatus.PASS
    assert "Git repository" in result.message
    assert result.details is not None


@pytest.mark.unit
def test_check_git_repo_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test git repository check when not in a git repo."""

    def mock_repo_init(*args: Any, **kwargs: Any) -> None:
        raise InvalidGitRepositoryError("Not a git repository")

    monkeypatch.setattr("dylan.utility_library.dylan_health.checks.Repo", mock_repo_init)

    result = check_git_repo()

    assert result.status == HealthCheckStatus.FAIL
    assert "Not a Git repository" in result.message


@pytest.mark.unit
def test_check_git_branch_clean(mock_git_repo: MagicMock) -> None:
    """Test git branch check with clean working tree."""
    mock_git_repo.is_dirty.return_value = False

    result = check_git_branch()

    assert result.status == HealthCheckStatus.PASS
    assert "main" in result.message
    assert "clean" in result.message.lower()


@pytest.mark.unit
def test_check_git_branch_dirty(mock_git_repo: MagicMock) -> None:
    """Test git branch check with uncommitted changes."""
    mock_git_repo.is_dirty.return_value = True

    result = check_git_branch()

    assert result.status == HealthCheckStatus.PASS
    assert "main" in result.message
    assert "uncommitted changes" in result.message.lower()


@pytest.mark.unit
def test_check_git_branch_detached_head(mock_git_repo: MagicMock) -> None:
    """Test git branch check in detached HEAD state."""
    mock_git_repo.head.is_detached = True
    mock_git_repo.head.commit.hexsha = "abc123def456789"

    result = check_git_branch()

    assert result.status == HealthCheckStatus.WARN
    assert "detached HEAD" in result.message


@pytest.mark.unit
def test_check_git_branch_not_in_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test git branch check when not in a repository."""

    def mock_repo_init(*args: Any, **kwargs: Any) -> None:
        raise InvalidGitRepositoryError("Not a git repository")

    monkeypatch.setattr("dylan.utility_library.dylan_health.checks.Repo", mock_repo_init)

    result = check_git_branch()

    assert result.status == HealthCheckStatus.FAIL
    assert "Not in a Git repository" in result.message


@pytest.mark.unit
def test_check_git_remote_exists(mock_git_repo: MagicMock) -> None:
    """Test git remote check when origin is configured."""
    result = check_git_remote()

    assert result.status == HealthCheckStatus.PASS
    assert "origin" in result.message.lower()
    assert result.details is not None
    assert "https://github.com/test/repo.git" in result.details


@pytest.mark.unit
def test_check_git_remote_missing(mock_git_repo: MagicMock) -> None:
    """Test git remote check when no remote is configured."""
    mock_remotes = MagicMock()
    mock_remotes.__contains__ = lambda self, key: False
    mock_git_repo.remotes = mock_remotes

    result = check_git_remote()

    assert result.status == HealthCheckStatus.WARN
    assert "No 'origin' remote" in result.message


@pytest.mark.unit
def test_check_git_remote_not_in_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test git remote check when not in a repository."""

    def mock_repo_init(*args: Any, **kwargs: Any) -> None:
        raise InvalidGitRepositoryError("Not a git repository")

    monkeypatch.setattr("dylan.utility_library.dylan_health.checks.Repo", mock_repo_init)

    result = check_git_remote()

    assert result.status == HealthCheckStatus.FAIL


@pytest.mark.unit
def test_check_gh_cli_installed_and_authenticated(
    mock_subprocess_run: Any, successful_gh_version: dict[str, Any]
) -> None:
    """Test gh CLI check when installed and authenticated."""
    mock_subprocess_run(successful_gh_version)

    result = check_gh_cli_installed()

    assert result.status == HealthCheckStatus.PASS
    assert "Authenticated" in result.message
    assert "gh version" in result.message


@pytest.mark.unit
def test_check_gh_cli_installed_not_authenticated(mock_subprocess_run: Any) -> None:
    """Test gh CLI check when installed but not authenticated."""
    mock_subprocess_run(
        {
            "gh --version": {
                "stdout": "gh version 2.40.0 (2023-12-15)\n",
                "returncode": 0,
            },
            "gh auth status": {
                "exception": subprocess.CalledProcessError(
                    returncode=1, cmd="gh auth status", stderr="Not authenticated"
                ),
            },
        }
    )

    result = check_gh_cli_installed()

    assert result.status == HealthCheckStatus.WARN
    assert "Not authenticated" in result.message
    assert result.details is not None
    assert "gh auth login" in result.details


@pytest.mark.unit
def test_check_gh_cli_not_installed(mock_subprocess_run: Any) -> None:
    """Test gh CLI check when not installed."""
    mock_subprocess_run(
        {
            "gh --version": {
                "exception": FileNotFoundError("gh not found"),
            }
        }
    )

    result = check_gh_cli_installed()

    assert result.status == HealthCheckStatus.FAIL
    assert "not installed" in result.message.lower()
    assert result.details is not None
    assert "https://cli.github.com/" in result.details


@pytest.mark.unit
def test_check_claude_code_installed_success(
    mock_subprocess_run: Any, successful_claude_version: dict[str, Any]
) -> None:
    """Test successful Claude Code installation check."""
    mock_subprocess_run(successful_claude_version)

    result = check_claude_code_installed()

    assert result.status == HealthCheckStatus.PASS
    assert "Claude Code" in result.message
    assert "v1.0.0" in result.message


@pytest.mark.unit
def test_check_claude_code_not_installed(mock_subprocess_run: Any) -> None:
    """Test Claude Code check when not installed."""
    mock_subprocess_run(
        {
            "claude --version": {
                "exception": FileNotFoundError("claude not found"),
            }
        }
    )

    result = check_claude_code_installed()

    assert result.status == HealthCheckStatus.FAIL
    assert "not installed" in result.message.lower()
    assert result.details is not None
    assert "https://claude.ai/code" in result.details


@pytest.mark.unit
def test_check_project_structure_complete(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test project structure check when all files exist."""
    monkeypatch.chdir(tmp_path)

    # Create required files
    (tmp_path / "pyproject.toml").touch()
    (tmp_path / "README.md").touch()
    (tmp_path / ".git").mkdir()

    result = check_project_structure()

    assert result.status == HealthCheckStatus.PASS
    assert "All required" in result.message
    assert result.details is not None
    assert "pyproject.toml" in result.details


@pytest.mark.unit
def test_check_project_structure_missing_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test project structure check when some files are missing."""
    monkeypatch.chdir(tmp_path)

    # Only create some files
    (tmp_path / "pyproject.toml").touch()
    (tmp_path / ".git").mkdir()
    # README.md is missing

    result = check_project_structure()

    assert result.status == HealthCheckStatus.WARN
    assert "Some project files are missing" in result.message
    assert "README.md" in result.details


@pytest.mark.unit
def test_check_project_structure_no_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test project structure check when no files exist."""
    monkeypatch.chdir(tmp_path)

    result = check_project_structure()

    assert result.status == HealthCheckStatus.FAIL
    assert "No project files found" in result.message


@pytest.mark.unit
def test_check_git_repo_git_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test git repository check when GitError is raised."""

    def mock_repo_init(*args: Any, **kwargs: Any) -> None:
        raise GitError("Git command failed")

    monkeypatch.setattr("dylan.utility_library.dylan_health.checks.Repo", mock_repo_init)

    result = check_git_repo()

    assert result.status == HealthCheckStatus.FAIL
    assert "Error accessing" in result.message


@pytest.mark.unit
def test_check_git_branch_git_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test git branch check when GitError is raised."""

    def mock_repo_init(*args: Any, **kwargs: Any) -> MagicMock:
        mock_repo = MagicMock()
        mock_repo.head.is_detached = False
        # Make active_branch raise GitError when accessed
        type(mock_repo).active_branch = property(lambda self: (_ for _ in ()).throw(GitError("Git error")))
        return mock_repo

    monkeypatch.setattr("dylan.utility_library.dylan_health.checks.Repo", mock_repo_init)

    result = check_git_branch()

    assert result.status == HealthCheckStatus.FAIL
    assert "Error checking branch" in result.message


@pytest.mark.unit
def test_check_git_remote_git_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test git remote check when GitError is raised."""

    def mock_repo_init(*args: Any, **kwargs: Any) -> MagicMock:
        mock_repo = MagicMock()
        # Make remotes raise GitError when accessed with 'in' operator
        mock_remotes = MagicMock()
        mock_remotes.__contains__ = MagicMock(side_effect=GitError("Git error"))
        mock_repo.remotes = mock_remotes
        return mock_repo

    monkeypatch.setattr("dylan.utility_library.dylan_health.checks.Repo", mock_repo_init)

    result = check_git_remote()

    assert result.status == HealthCheckStatus.FAIL
    assert "Error checking remote" in result.message


@pytest.mark.unit
def test_check_gh_cli_timeout(mock_subprocess_run: Any) -> None:
    """Test gh CLI check when authentication check times out."""
    mock_subprocess_run(
        {
            "gh --version": {
                "stdout": "gh version 2.40.0\n",
                "returncode": 0,
            },
            "gh auth status": {
                "exception": subprocess.TimeoutExpired(cmd="gh auth status", timeout=5),
            },
        }
    )

    result = check_gh_cli_installed()

    assert result.status == HealthCheckStatus.WARN
    assert "timed out" in result.message.lower()


@pytest.mark.unit
def test_check_claude_code_timeout(mock_subprocess_run: Any) -> None:
    """Test Claude Code check when command times out."""
    mock_subprocess_run(
        {
            "claude --version": {
                "exception": subprocess.TimeoutExpired(cmd="claude --version", timeout=5),
            }
        }
    )

    result = check_claude_code_installed()

    assert result.status == HealthCheckStatus.FAIL
    assert "timed out" in result.message.lower()


@pytest.mark.unit
def test_check_git_installed_called_process_error(mock_subprocess_run: Any) -> None:
    """Test git installation check when command returns non-zero exit code."""
    mock_subprocess_run(
        {
            "git --version": {
                "stdout": "",
                "stderr": "git: command failed",
                "returncode": 1,
                "exception": subprocess.CalledProcessError(
                    returncode=1, cmd="git --version", stderr="git: command failed"
                ),
            }
        }
    )

    result = check_git_installed()

    assert result.status == HealthCheckStatus.FAIL
    assert "command failed" in result.message.lower()


@pytest.mark.unit
def test_check_gh_cli_version_error(mock_subprocess_run: Any) -> None:
    """Test gh CLI check when version command fails."""
    mock_subprocess_run(
        {
            "gh --version": {
                "exception": subprocess.CalledProcessError(
                    returncode=1, cmd="gh --version", stderr="gh: command failed"
                ),
            }
        }
    )

    result = check_gh_cli_installed()

    assert result.status == HealthCheckStatus.FAIL
    assert "command failed" in result.message.lower()


@pytest.mark.unit
def test_check_claude_code_called_process_error(mock_subprocess_run: Any) -> None:
    """Test Claude Code check when command fails."""
    mock_subprocess_run(
        {
            "claude --version": {
                "exception": subprocess.CalledProcessError(
                    returncode=1, cmd="claude --version", stderr="claude: command failed"
                ),
            }
        }
    )

    result = check_claude_code_installed()

    assert result.status == HealthCheckStatus.FAIL
    assert "command failed" in result.message.lower()
