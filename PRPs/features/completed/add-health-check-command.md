# Feature: Health Check Command

## Feature Description

Add a `dylan health` command to the Dylan CLI that performs comprehensive system diagnostics and health checks on the development environment. This command will verify that all required dependencies (Git, GitHub CLI, Claude Code) are properly installed and configured, check the current project state, and provide actionable feedback to users about any issues that need attention.

The health check command will serve as a first-stop diagnostic tool for users experiencing issues with Dylan utilities, reducing troubleshooting time and improving the overall user experience. It will display results in a visually appealing format using Rich's table and panel components, consistent with Dylan's existing UI theme.

## User Story

As a developer using Dylan CLI tools
I want to run a health check command
So that I can quickly verify my environment is properly configured and identify any issues before running other Dylan commands

## Problem Statement

Users of Dylan CLI often encounter issues due to:
- Missing or improperly configured dependencies (Git, GitHub CLI, Claude Code)
- Incorrect repository state or branch configuration
- Authentication issues with GitHub or Claude Code
- Misconfigured project settings or missing required files

Currently, there is no unified way to diagnose these issues. Users must manually check each dependency and configuration, which is time-consuming and error-prone. This leads to frustration and support burden when commands fail due to environment issues.

## Solution Statement

Implement a `dylan health` CLI command that automatically checks all critical dependencies and configuration requirements. The command will:

1. Verify system dependencies (Git, gh CLI, Claude Code) are installed and accessible
2. Check project configuration (git repo, branch status, remote configuration)
3. Validate authentication status for GitHub and Claude Code
4. Test basic functionality of each dependency
5. Display results in a clear, color-coded format with actionable recommendations
6. Return appropriate exit codes for scripting and CI/CD integration

The implementation will follow Dylan's existing patterns for CLI commands, using Typer for argument parsing, Rich for UI presentation, and consistent error handling.

## Relevant Files

### Existing Files to Reference

- **dylan/cli.py** (lines 1-84)
  - Main CLI entry point where the health command will be registered
  - Shows pattern for adding commands with `@app.command()` decorator
  - Demonstrates use of UI theme constants for consistent styling

- **dylan/utility_library/shared/config.py** (lines 1-21)
  - Configuration constants including repository URLs and dependency package names
  - Defines error messages for missing dependencies
  - Will be extended with health check related constants

- **dylan/utility_library/shared/ui_theme.py**
  - UI theme components (COLORS, ARROW, SPARK) for consistent look and feel
  - Provides color constants for success, error, warning, and info states
  - Will be used for health check result visualization

- **dylan/utility_library/shared/error_handling.py**
  - Error handling patterns with `@handle_dylan_errors()` decorator
  - User-friendly error messages with context
  - Pattern to follow for health check error scenarios

- **dylan/utility_library/provider_clis/provider_claude_code.py**
  - Shows how to check for Claude Code installation
  - Provides subprocess execution patterns for running external commands
  - Will be referenced for Claude Code health checks

- **dylan/utility_library/provider_clis/shared/subprocess_utils.py**
  - Subprocess utilities for running external commands
  - Error handling for command execution
  - Will be used for dependency version checks

- **dylan/utility_library/dylan_review/dylan_review_cli.py**
  - Example CLI interface implementation pattern
  - Shows integration with shared UI components
  - Demonstrates proper use of Typer options and arguments

- **dylan/utility_library/dylan_standup/standup_cli.py**
  - Another CLI command implementation for reference
  - Shows pattern for commands with options and flags
  - Demonstrates integration with error handling decorator

### New Files

#### Core Implementation

- **dylan/utility_library/dylan_health/__init__.py**
  - Package initialization for health check module
  - Exports public API

- **dylan/utility_library/dylan_health/dylan_health_cli.py**
  - CLI interface implementation
  - Command definition with Typer
  - Options for verbose output, JSON format, etc.

- **dylan/utility_library/dylan_health/dylan_health_runner.py**
  - Core health check logic
  - Dependency verification functions
  - Project state validation
  - Result aggregation and reporting

- **dylan/utility_library/dylan_health/checks.py**
  - Individual health check functions
  - Each check returns standardized result object
  - Checks include: Git, GitHub CLI, Claude Code, repository state, authentication

#### Testing

- **dylan/utility_library/dylan_health/tests/__init__.py**
  - Test package initialization

- **dylan/utility_library/dylan_health/tests/conftest.py**
  - Pytest fixtures for health check tests
  - Mock dependency executables
  - Mock git repository states

- **dylan/utility_library/dylan_health/tests/test_dylan_health_cli.py**
  - CLI interface tests
  - Command invocation tests
  - Option/flag tests

- **dylan/utility_library/dylan_health/tests/test_dylan_health_runner.py**
  - Core logic tests
  - Result aggregation tests
  - Error handling tests

- **dylan/utility_library/dylan_health/tests/test_checks.py**
  - Unit tests for individual health checks
  - Mock subprocess calls
  - Test all pass/fail scenarios

## Relevant Research & Documentation

Use these documentation files and links to help with understanding the technology to use:

- [Typer - Python CLI Framework](https://typer.tiangolo.com/)
  - [Commands and Arguments](https://typer.tiangolo.com/tutorial/commands/)
  - [Options and Flags](https://typer.tiangolo.com/tutorial/options/)
  - [Testing Typer Applications](https://typer.tiangolo.com/tutorial/testing/)
  - Building CLI commands with type hints, automatic help generation, and parameter validation

- [Rich - Python Terminal Formatting](https://rich.readthedocs.io/)
  - [Tables](https://rich.readthedocs.io/en/stable/tables.html)
  - [Panels](https://rich.readthedocs.io/en/stable/panel.html)
  - [Console Status](https://rich.readthedocs.io/en/stable/console.html#status)
  - Beautiful terminal output with colors, tables, progress indicators

- [GitPython Documentation](https://gitpython.readthedocs.io/)
  - [Repository](https://gitpython.readthedocs.io/en/stable/reference.html#git.repo.base.Repo)
  - [Remote Operations](https://gitpython.readthedocs.io/en/stable/reference.html#git.remote.Remote)
  - Checking git repository state, branch info, remote configuration

- [Pytest Documentation](https://docs.pytest.org/)
  - [Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
  - [Mocking](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
  - [Parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html)
  - Testing patterns and best practices

- [Python subprocess module](https://docs.python.org/3/library/subprocess.html)
  - [subprocess.run()](https://docs.python.org/3/3/library/subprocess.html#subprocess.run)
  - [Handling exceptions](https://docs.python.org/3/library/subprocess.html#subprocess.CalledProcessError)
  - Running external commands and capturing output

- [CLI Health Check Best Practices (2025)](https://betterstack.com/community/guides/monitoring/kubernetes-health-checks/)
  - Clear status codes: 0 for healthy, non-zero for unhealthy
  - Dedicated endpoints for different check types
  - Appropriate timeouts and retry logic
  - Comprehensive yet concise output

## Implementation Plan

### Phase 1: Foundation

**Setup Module Structure**
- Create `dylan/utility_library/dylan_health/` directory
- Create `__init__.py` with package docstring
- Create empty `checks.py` for individual check functions
- Create empty `dylan_health_runner.py` for core logic
- Create empty `dylan_health_cli.py` for CLI interface

**Define Data Models**
- Create Pydantic models or dataclasses for health check results
- Define `HealthCheckResult` with fields: name, status (PASS/FAIL/WARN), message, details
- Define `HealthCheckReport` to aggregate all check results
- Ensure type safety with proper type hints

### Phase 2: Core Implementation

**Implement Individual Health Checks** (in `checks.py`)
- `check_git_installed()`: Verify git is installed and get version
- `check_git_repo()`: Verify current directory is a git repository
- `check_git_branch()`: Check current branch and clean/dirty state
- `check_git_remote()`: Verify remote repository is configured
- `check_gh_cli_installed()`: Verify GitHub CLI is installed and authenticated
- `check_claude_code_installed()`: Verify Claude Code is installed and get version
- `check_project_structure()`: Verify expected project files exist (pyproject.toml, etc.)
- Each function returns a `HealthCheckResult` object with standardized format

**Implement Core Runner Logic** (in `dylan_health_runner.py`)
- `run_all_checks()`: Execute all health checks in sequence
- `run_specific_check()`: Execute individual check by name (for future extensibility)
- Aggregate results into `HealthCheckReport`
- Determine overall health status (all pass = healthy, any fail = unhealthy)
- Format results for display using Rich components

**Implement CLI Interface** (in `dylan_health_cli.py`)
- Define `health()` command function with Typer
- Add `--verbose` flag for detailed output
- Add `--json` flag for machine-readable output
- Add `--check` option to run specific checks only
- Call runner and display results using Rich
- Return appropriate exit codes (0 = healthy, 1 = unhealthy)
- Apply `@handle_dylan_errors()` decorator for error handling

**Register Command in Main CLI** (update `dylan/cli.py`)
- Import `health` command from `dylan_health_cli`
- Add command to app with `@app.command()`
- Add to help table in main callback
- Ensure consistent styling with existing commands

### Phase 3: Integration

**Testing Setup**
- Create test directory structure: `dylan/utility_library/dylan_health/tests/`
- Create `conftest.py` with fixtures for mocking dependencies
- Fixtures: `mock_git_repo`, `mock_subprocess`, `mock_claude_provider`, etc.

**Add Configuration Constants** (update `dylan/utility_library/shared/config.py`)
- Add health check related messages
- Add dependency version requirements if needed
- Document expected environment variables

**CLI Integration**
- Test command invocation through main CLI
- Verify help text displays correctly
- Test with various option combinations
- Ensure consistent UI theme with other commands

**Documentation**
- Add usage examples to CLAUDE.md
- Document all health check types
- Document exit codes and their meanings
- Add troubleshooting guide for common failures

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. Create Module Structure

- Create directory: `dylan/utility_library/dylan_health/`
- Create `dylan/utility_library/dylan_health/__init__.py` with module docstring
- Create empty `dylan/utility_library/dylan_health/checks.py` with module docstring
- Create empty `dylan/utility_library/dylan_health/dylan_health_runner.py` with module docstring
- Create empty `dylan/utility_library/dylan_health/dylan_health_cli.py` with module docstring

### 2. Define Data Models and Types

- In `checks.py`, define `HealthCheckStatus` enum (PASS, FAIL, WARN)
- Define `HealthCheckResult` dataclass with fields: name, status, message, details (optional)
- Add type hints for all fields
- Add Google-style docstrings

### 3. Implement Individual Health Checks

- In `checks.py`, implement `check_git_installed() -> HealthCheckResult`
  - Run `git --version` subprocess
  - Parse version output
  - Return PASS with version or FAIL with error message
  - Add structured logging with correlation context
  - Add type hints and docstring

- Implement `check_git_repo() -> HealthCheckResult`
  - Use GitPython to check if current directory is a repo
  - Return PASS if repo exists, FAIL otherwise
  - Include repository path in details
  - Add structured logging and type hints

- Implement `check_git_branch() -> HealthCheckResult`
  - Get current branch name
  - Check if working tree is clean
  - Return status with branch info and clean/dirty state
  - Add structured logging and type hints

- Implement `check_git_remote() -> HealthCheckResult`
  - Check if remote 'origin' exists
  - Get remote URL
  - Return PASS with remote info or FAIL if no remote
  - Add structured logging and type hints

- Implement `check_gh_cli_installed() -> HealthCheckResult`
  - Run `gh --version` subprocess
  - Check authentication status with `gh auth status`
  - Return PASS if installed and authenticated, WARN if not authenticated, FAIL if not installed
  - Add structured logging and type hints

- Implement `check_claude_code_installed() -> HealthCheckResult`
  - Run `claude --version` subprocess
  - Parse version output
  - Return PASS with version or FAIL with installation instructions
  - Add structured logging and type hints

- Implement `check_project_structure() -> HealthCheckResult`
  - Check for existence of `pyproject.toml`, `README.md`, `.git/`
  - Return PASS if all exist, WARN if some missing
  - Include list of missing files in details
  - Add structured logging and type hints

### 4. Implement Runner Logic

- In `dylan_health_runner.py`, import all check functions from `checks.py`
- Define `HealthCheckReport` dataclass to hold list of results and overall status
- Implement `run_all_checks() -> HealthCheckReport`
  - Execute all check functions in sequence
  - Collect all results
  - Determine overall health status (any FAIL = unhealthy)
  - Return aggregated report
  - Add structured logging with correlation context
  - Add type hints and Google-style docstring

- Implement `format_results_table(report: HealthCheckReport) -> Table`
  - Create Rich Table with columns: Check, Status, Details
  - Add rows for each check result
  - Use color coding: green for PASS, red for FAIL, yellow for WARN
  - Return formatted table
  - Add type hints and docstring

- Implement `format_results_json(report: HealthCheckReport) -> str`
  - Convert report to JSON format for machine consumption
  - Include all check details
  - Return JSON string
  - Add type hints and docstring

### 5. Implement CLI Interface

- In `dylan_health_cli.py`, import Typer, Rich Console, and runner functions
- Import UI theme constants from `shared/ui_theme.py`
- Import error handling decorator from `shared/error_handling.py`
- Define `health()` command function with Typer decorators:
  - Add `verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output")`
  - Add `json_output: bool = typer.Option(False, "--json", help="Output results in JSON format")`
  - Add proper type hints with return type `None`
- Implement function body:
  - Call `run_all_checks()` from runner
  - If `json_output`, print JSON and exit
  - Otherwise, display results using Rich table
  - Show summary message (overall status)
  - Exit with code 0 if healthy, 1 if unhealthy
  - Apply `@handle_dylan_errors(utility_name="health")` decorator
  - Add Google-style docstring

### 6. Register Command in Main CLI

- Edit `dylan/cli.py`
- Import health command: `from .utility_library.dylan_health.dylan_health_cli import health`
- Add command registration: `app.command(name="health", help="Check system health and dependencies")(health)`
- In the `_main()` callback, add row to help table:
  ```python
  table.add_row(
      "health",
      "Check system health and dependencies",
      "dylan health --verbose"
  )
  ```
- Ensure proper ordering in the table (suggest after standup, before review)

### 7. Create Test Structure

- Create directory: `dylan/utility_library/dylan_health/tests/`
- Create `dylan/utility_library/dylan_health/tests/__init__.py` (empty)
- Create `dylan/utility_library/dylan_health/tests/conftest.py` with fixtures:
  - `@pytest.fixture mock_git_command()` - mock subprocess for git commands
  - `@pytest.fixture mock_gh_command()` - mock subprocess for gh commands
  - `@pytest.fixture mock_claude_command()` - mock subprocess for claude commands
  - `@pytest.fixture temp_git_repo()` - create temporary git repository for testing
  - All fixtures must have type hints and docstrings

### 8. Write Unit Tests for Health Checks

- Create `dylan/utility_library/dylan_health/tests/test_checks.py`
- Import pytest and check functions
- Write tests for each check function:
  - `test_check_git_installed_success()` - git is installed and returns version
  - `test_check_git_installed_failure()` - git command not found
  - `test_check_git_repo_success()` - current directory is a git repo
  - `test_check_git_repo_failure()` - current directory is not a git repo
  - `test_check_git_branch_clean()` - working tree is clean
  - `test_check_git_branch_dirty()` - working tree has uncommitted changes
  - `test_check_git_remote_exists()` - remote origin is configured
  - `test_check_git_remote_missing()` - no remote configured
  - `test_check_gh_cli_installed_and_authenticated()` - gh CLI installed and logged in
  - `test_check_gh_cli_installed_not_authenticated()` - gh CLI installed but not logged in
  - `test_check_gh_cli_not_installed()` - gh CLI not found
  - `test_check_claude_code_installed_success()` - claude installed with version
  - `test_check_claude_code_not_installed()` - claude command not found
  - `test_check_project_structure_complete()` - all required files exist
  - `test_check_project_structure_missing_files()` - some files missing
- Use appropriate fixtures and mocking
- Mark all tests with `@pytest.mark.unit`
- All tests must have type hints

### 9. Write Tests for Runner Logic

- Create `dylan/utility_library/dylan_health/tests/test_dylan_health_runner.py`
- Write tests:
  - `test_run_all_checks_all_pass()` - all checks return PASS
  - `test_run_all_checks_with_failures()` - some checks return FAIL
  - `test_run_all_checks_with_warnings()` - some checks return WARN
  - `test_format_results_table()` - verify table formatting
  - `test_format_results_json()` - verify JSON output format
- Mock individual check functions to return controlled results
- Mark all tests with `@pytest.mark.unit`
- All tests must have type hints

### 10. Write Tests for CLI Interface

- Create `dylan/utility_library/dylan_health/tests/test_dylan_health_cli.py`
- Import CliRunner from Typer for testing
- Write tests:
  - `test_health_command_success()` - command exits with 0 when healthy
  - `test_health_command_failure()` - command exits with 1 when unhealthy
  - `test_health_command_verbose()` - verbose flag shows detailed output
  - `test_health_command_json()` - json flag outputs valid JSON
  - `test_health_command_integration()` - full command through main CLI app
- Mock runner functions to control output
- Mark all tests with `@pytest.mark.unit`
- All tests must have type hints

### 11. Run Validation Commands

Execute every command to validate the feature works correctly with zero regressions:

- Run linter: `uv run ruff check dylan/`
  - Fix any linting errors
- Run type checker: `uv run mypy dylan/`
  - Fix any type errors
- Run unit tests: `uv run pytest dylan/utility_library/dylan_health/tests/ -m unit -v`
  - Ensure all tests pass
- Run full test suite: `uv run pytest dylan/ -v`
  - Ensure zero regressions in existing tests
- Test CLI command manually: `uv run dylan health`
  - Verify output is formatted correctly
  - Check exit codes work properly
- Test CLI command with flags: `uv run dylan health --verbose`
  - Verify verbose output
- Test CLI command JSON output: `uv run dylan health --json`
  - Verify valid JSON output
- Test CLI help: `uv run dylan health --help`
  - Verify help text is clear and accurate
- Test main CLI integration: `uv run dylan`
  - Verify health command appears in command list

## Testing Strategy

See `CLAUDE.md` for complete testing requirements. Every file in `dylan/utility_library/dylan_health/` must have a corresponding test file in `dylan/utility_library/dylan_health/tests/`.

### Unit Tests

All unit tests must:
- Be marked with `@pytest.mark.unit`
- Have complete type hints including return types
- Have Google-style docstrings
- Mock external dependencies (subprocess calls, file system, GitPython)
- Test both success and failure scenarios
- Test edge cases

**Check Functions Tests** (`test_checks.py`):
- Test each individual health check function in isolation
- Mock subprocess calls to git, gh, claude commands
- Test success scenarios with expected output
- Test failure scenarios (command not found, errors)
- Test warning scenarios (e.g., gh installed but not authenticated)
- Verify HealthCheckResult objects have correct status and messages

**Runner Logic Tests** (`test_dylan_health_runner.py`):
- Mock all individual check functions
- Test aggregation of results into HealthCheckReport
- Test overall status determination logic
- Test table formatting output
- Test JSON formatting output
- Verify proper type conversions

**CLI Interface Tests** (`test_dylan_health_cli.py`):
- Use Typer's CliRunner for command testing
- Mock runner functions to control results
- Test exit codes (0 for healthy, 1 for unhealthy)
- Test --verbose flag behavior
- Test --json flag behavior
- Test command help text
- Test integration with main CLI app

### Integration Tests

If the feature interacts with multiple components, integration tests should:
- Be marked with `@pytest.mark.integration`
- Test actual command execution in a controlled environment
- Use real temporary git repositories (not mocked)
- Verify end-to-end flow from CLI to output
- Place in `dylan/utility_library/dylan_health/tests/test_integration.py` if needed

**Potential Integration Tests**:
- `test_health_check_in_real_git_repo()` - Run health check in actual temporary git repo
- `test_health_check_with_missing_dependencies()` - Test behavior when dependencies unavailable
- `test_health_check_output_format()` - Verify Rich table renders correctly

### Edge Cases

Edge cases that need to be tested:
- Git repository in detached HEAD state
- Git repository with no commits yet
- Git repository with no remote configured
- Git repository in a submodule
- GitHub CLI installed but authentication expired
- Claude Code installed but different version than expected
- Running health check outside of a git repository
- Running health check with corrupted .git directory
- Subprocess commands timing out or hanging
- Subprocess commands returning unexpected output formats
- Missing pyproject.toml or other required files
- Symbolic links or unusual file system structures

## Acceptance Criteria

1. **Command Registration**: `dylan health` command is registered and appears in main help
2. **Dependency Checks**: All critical dependencies (git, gh, claude) are checked and reported
3. **Repository Checks**: Git repository state is validated (branch, clean/dirty, remote)
4. **Project Checks**: Expected project files are verified (pyproject.toml, etc.)
5. **Output Format**: Results displayed in clear, color-coded Rich table
6. **Exit Codes**: Command exits with 0 when healthy, 1 when unhealthy
7. **Verbose Mode**: `--verbose` flag shows detailed information
8. **JSON Output**: `--json` flag outputs valid, parseable JSON
9. **Error Handling**: Errors are caught and displayed with helpful messages
10. **Type Safety**: All code passes mypy strict type checking with zero errors
11. **Linting**: All code passes ruff linting with zero errors
12. **Test Coverage**: All functions have unit tests with >90% coverage
13. **Documentation**: Google-style docstrings on all public functions and classes
14. **Integration**: Command integrates seamlessly with existing Dylan CLI architecture
15. **UI Consistency**: Output styling matches Dylan's UI theme (colors, formatting)

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

**Required validation commands:**

```bash
# Lint check must pass
uv run ruff check dylan/

# Type check must pass
uv run mypy dylan/

# Unit tests must pass
uv run pytest dylan/utility_library/dylan_health/tests/ -m unit -v

# All tests must pass with zero regressions
uv run pytest dylan/ -v

# Manual testing: Basic health check
uv run dylan health

# Manual testing: Verbose output
uv run dylan health --verbose

# Manual testing: JSON output
uv run dylan health --json

# Manual testing: Command help
uv run dylan health --help

# Manual testing: Main CLI integration
uv run dylan

# Verify health command in help table
uv run dylan --help
```

**Expected Outcomes:**
- All linting and type checks pass with zero errors
- All tests pass with zero failures
- `dylan health` displays formatted table with check results
- `dylan health --verbose` shows additional details
- `dylan health --json` outputs valid JSON
- `dylan health --help` shows clear usage information
- `dylan` (main CLI) shows health command in commands table
- Exit code is 0 when all checks pass, 1 when any check fails

## Notes

### Implementation Considerations

1. **Dependency Resilience**: Health checks should not fail catastrophically if a dependency is missing. Each check should gracefully handle errors and report them as failures.

2. **Performance**: Health checks should execute quickly (< 3 seconds total). Use timeouts on subprocess calls to prevent hanging.

3. **Extensibility**: The health check system should be designed to easily add new checks in the future. Consider a registry pattern if more than 10 checks are needed.

4. **Security**: Be cautious with subprocess execution. Always use proper escaping and avoid shell=True. Use subprocess.run() with explicit arguments list.

5. **Cross-Platform**: Ensure health checks work on macOS, Linux, and Windows. Note that some commands may have different output formats or locations across platforms.

6. **Logging**: Use structured logging with correlation IDs for all operations. This helps with debugging when health checks fail.

7. **Future Enhancements**: Consider adding:
   - `--fix` flag to automatically attempt fixing common issues
   - `--check <name>` to run specific checks only
   - Caching of check results to speed up repeated runs
   - Integration with monitoring/telemetry systems

### Related Dylan Commands

The health check command complements existing Dylan utilities:
- Run before `dylan review` to ensure environment is ready
- Run after installation to verify setup
- Run when troubleshooting issues with other commands
- Can be integrated into CI/CD pipelines as a validation step

### Dependencies

This feature uses only existing dependencies in `pyproject.toml`:
- `typer>=0.15.4` - CLI framework
- `rich>=14.0.0` - Terminal formatting
- `gitpython>=3.1.44` - Git repository operations

No new dependencies need to be added.

### Testing Infrastructure

All tests use existing pytest infrastructure:
- Run with `uv run pytest`
- Use fixtures from `dylan/conftest.py` and module-specific conftest files
- Follow existing test patterns from other Dylan utilities
- Mark tests with `@pytest.mark.unit` for unit tests

### Documentation Updates

After implementation, update:
- `CLAUDE.md` - Add health command usage examples
- `README.md` - Add health command to feature list (if applicable)
- Consider adding troubleshooting section based on common health check failures
