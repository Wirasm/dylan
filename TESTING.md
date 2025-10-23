# Testing Guide for Dylan

This document outlines the testing approach and structure for the Dylan package.

## Current Testing Status

The testing framework is being set up with a focus on unit tests that don't require the actual Claude provider. This allows for faster and more reliable testing without triggering actual provider calls.

### Updated Testing Strategy

The current branch has implemented these changes:

1. Fixed import errors in test files
2. Updated package structure to ensure proper imports
3. Simplified subprocess and exit command tests
4. Temporarily skipped tests that would trigger real Claude provider calls
5. Added support for mocking provider behavior

## Testing Structure

Dylan uses a vertical slice architecture for testing, with tests located close to the modules they test:

```
dylan/
├── conftest.py           # Main conftest with shared fixtures
├── tests/                # Tests for core CLI
│   ├── __init__.py
│   └── test_cli.py       # Tests for the main CLI application
├── utility_library/
    ├── shared/           # Shared components
    │   ├── tests/        # Tests for shared utilities
    │       ├── __init__.py
    │       ├── test_exit_command.py
    │       └── test_subprocess_utils.py
    ├── dylan_review/
    │   ├── tests/
    │       ├── __init__.py
    │       ├── conftest.py  # Review-specific fixtures
    │       ├── test_dylan_review_cli.py
    │       └── test_dylan_review_runner.py
    ├── dylan_pr/
    │   ├── tests/
    │       ├── ...
    └── ...
```

## Running Tests

Tests are run using pytest with UV:

```bash
# Run all tests (includes skipped tests)
uv run pytest

# Run tests for a specific module
uv run pytest dylan/utility_library/dylan_review/tests/

# Run tests with coverage report
uv run pytest --cov=dylan

# Run a specific test file
uv run pytest dylan/utility_library/dylan_review/tests/test_dylan_review_runner.py

# Run tests without skipped tests
uv run pytest -k "not skip"
```

## Parallel Execution Testing

Dylan supports parallel test execution using pytest-xdist, which can significantly reduce test suite execution time by running tests concurrently across multiple CPU cores.

### What is Parallel Execution

pytest-xdist is a pytest plugin that distributes tests across multiple workers (processes), allowing tests to run simultaneously. This is particularly beneficial for:

- **Faster feedback loops**: Reduce test execution time during development
- **CI/CD cost savings**: Lower execution minutes in continuous integration pipelines
- **Better resource utilization**: Leverage multi-core systems effectively

### Installation

pytest-xdist is already installed as part of the development dependencies. If you need to install it separately:

```bash
uv add --dev pytest-xdist
```

### Basic Usage

Run tests in parallel using the `-n` option:

```bash
# Automatically detect and use all available CPU cores
uv run pytest -n auto

# Use a specific number of workers (e.g., 4 workers)
uv run pytest -n 4

# Run tests for a specific module in parallel
uv run pytest dylan/utility_library/dylan_review/tests/ -n auto

# Combine with other pytest options
uv run pytest -n auto -v --cov=dylan
```

### Performance Benefits

Parallel execution provides significant performance improvements:

- **Time savings**: 30-80% reduction in test execution time for large test suites
- **Scalability**: Automatically scales with available CPU cores
- **Cost reduction**: Lower CI/CD costs based on execution minutes

Example performance comparison:

```bash
# Measure sequential execution time
time uv run pytest

# Measure parallel execution time
time uv run pytest -n auto
```

For test suites with 50+ tests, parallel execution typically provides 50-70% time reduction on a 4-core system.

### Best Practices for Writing Parallel-Safe Tests

To ensure tests work correctly in parallel execution:

#### 1. Use Fixtures for Isolation

Always use pytest fixtures for test data and resources:

```python
def test_file_operations(tmp_path):
    """tmp_path provides isolated temp directory per test."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    assert test_file.exists()
```

#### 2. Avoid Global State

Don't rely on or modify global state:

```python
# Bad: Uses global state
counter = 0
def test_increment():
    global counter
    counter += 1
    assert counter == 1  # Will fail in parallel

# Good: Self-contained test
def test_increment():
    counter = 0
    counter += 1
    assert counter == 1
```

#### 3. Use Isolated Resources

Use fixtures that provide isolated resources:

```python
def test_with_mock(mock_claude_provider, tmp_path):
    """Use fixtures for isolated mocks and temp directories."""
    output_file = tmp_path / "output.txt"
    # Test implementation
```

#### 4. Make Tests Deterministic

Tests should not depend on execution order or timing:

```python
# Good: Deterministic result
def test_computation():
    result = sum(range(100))
    assert result == 4950

# Bad: Timing-dependent (avoid unless necessary)
def test_timing():
    start = time.time()
    time.sleep(1)
    assert time.time() - start >= 1  # Can be flaky
```

#### 5. Mock External Dependencies

Always mock external services and APIs:

```python
def test_api_call(mock_claude_provider):
    """Mock external dependencies to ensure test isolation."""
    # Test with mocked provider
```

### Common Issues and Solutions

#### Issue: Tests Pass Sequentially but Fail in Parallel

**Cause**: Tests are sharing state or resources

**Solution**:
- Check for shared file paths (use `tmp_path` fixture)
- Check for database connection limits (use connection pooling)
- Check for global state modification (ensure proper cleanup)
- Verify no race conditions in async code

```bash
# Run with single worker to identify isolation issues
uv run pytest -n 1
```

#### Issue: Tests Are Slower in Parallel for Small Test Suites

**Cause**: Parallel execution overhead exceeds benefits for small test suites

**Solution**:
- Only use parallel execution for test suites with 20+ tests
- Use sequential execution for quick smoke tests
- Profile your test suite to find the optimal number of workers

#### Issue: Flaky Tests in Parallel Mode

**Cause**: Tests have timing dependencies or race conditions

**Solution**:
- Review test for timing assumptions
- Ensure proper use of fixtures for setup/teardown
- Use pytest markers to run problematic tests sequentially:

```python
@pytest.mark.xdist_group(name="sequential")
def test_must_run_alone():
    """This test will run in a dedicated worker."""
    pass
```

#### Issue: File or Resource Conflicts

**Cause**: Multiple tests writing to the same file or using the same port

**Solution**:
- Always use `tmp_path` fixture for file operations
- Use dynamic port allocation for network tests
- Ensure proper cleanup in fixtures

### CI/CD Integration

Configure parallel execution in your CI/CD pipeline to reduce execution time and costs:

#### GitHub Actions Example

```yaml
- name: Run tests in parallel
  run: uv run pytest -n auto --maxfail=5
```

#### General CI/CD Recommendations

- Use `-n auto` to automatically scale to available cores
- Set `--maxfail` to stop early on multiple failures
- Consider using `--dist loadscope` for tests with module-level fixtures
- Monitor execution times to optimize worker count

### Advanced Configuration

Configure pytest-xdist in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = [
    "--import-mode=importlib",
    "-v",
    "--strict-markers",
    # Uncomment to enable parallel execution by default
    # "-n", "auto",
]
```

**Note**: Enabling parallel execution by default may not be suitable for all workflows. Evaluate your test suite characteristics before making it the default.

### When to Use Parallel vs Sequential Execution

**Use Parallel Execution When**:
- Test suite has 20+ tests
- Tests are well-isolated and independent
- Tests are I/O bound (file operations, network calls)
- Running on multi-core systems
- Optimizing CI/CD execution time

**Use Sequential Execution When**:
- Test suite has fewer than 20 tests
- Debugging test failures
- Tests require specific execution order
- Tests use shared resources that can't be isolated
- Running quick smoke tests

## Test Types

### Unit Tests
- Test individual functions and classes in isolation
- Located in each vertical's tests directory
- Naming: `test_<module>_<function>.py`

### Integration Tests
- Test interactions between components
- Located in each vertical's tests directory
- Prefix: `test_integration_*.py`

### Functional Tests
- Test CLI commands end-to-end
- Located in the root tests directory
- Limited use of mocks - simulate real usage
- Prefix: `test_functional_*.py`

## Fixtures

### Global Fixtures (in dylan/conftest.py)
- `mock_claude_provider`: Mocks the Claude Code provider for testing
- `temp_output_dir`: Creates a temporary directory for test outputs
- `cli_runner`: Provides a Typer CLI test runner
- `mock_git_repo`: Creates a mock git repository structure
- `mock_git_operations`: Mocks common git commands

### Vertical-Specific Fixtures
Each vertical slice has its own fixtures in its conftest.py file.

#### dylan_review
- `mock_git_diff`: Mock git diff output
- `sample_review_report`: Sample review report for testing
- `mock_review_runner`: Mock for the review runner module

#### dylan_pr
- `mock_git_branch_info`: Mock git branch information
- `mock_github_api`: Mock GitHub API responses
- `mock_gh_cli`: Mock GitHub CLI command responses
- `mock_pr_runner`: Mock for the PR runner module

## Mocking Strategy

- External dependencies (git, gh, claude) are mocked
- File operations use temporary directories
- Internal modules use fixture-based dependency injection
- Unit tests use fine-grained mocking
- Integration tests use coarser-grained mocking

## Adding New Tests

When adding new functionality:

1. Create unit tests for new modules in the appropriate tests directory
2. Update/add fixtures in the relevant conftest.py
3. Add integration tests for interactions with other components
4. Run the full test suite before submitting changes

For new vertical slices:

1. Create a tests directory within the vertical
2. Add a vertical-specific conftest.py
3. Implement appropriate unit, integration, and functional tests

## Code Coverage

Code coverage is tracked using pytest-cov:

```bash
# Generate coverage report
uv run pytest --cov=dylan --cov-report=term

# Generate HTML coverage report
uv run pytest --cov=dylan --cov-report=html
```

## Continuous Integration

The test suite runs automatically on:
- Pull requests to develop and main branches
- Direct pushes to develop and main branches

All tests must pass for PRs to be merged.