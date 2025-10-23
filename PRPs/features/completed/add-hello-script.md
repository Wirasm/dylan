# Feature: Add Hello Script

## Feature Description

Create a simple, well-structured "Hello World" Python script in the root directory of the project. This script will serve as a basic example demonstrating Python best practices including proper script structure, type annotations, docstrings, and executable configuration. The script follows the project's KISS (Keep It Simple, Stupid) and YAGNI (You Aren't Gonna Need It) principles by providing minimal functionality with maximum clarity.

## User Story

As a developer or user of this project
I want to have a simple hello script in the root directory
So that I can quickly test the Python environment setup and have a basic example of proper Python script structure

## Problem Statement

The project currently lacks a simple, executable script in the root directory that can be used to:
- Verify Python environment setup
- Demonstrate basic Python script best practices
- Provide a quick reference for proper script structure including type annotations and docstrings
- Serve as a minimal example for new contributors

## Solution Statement

Create a `hello.py` script in the root directory that:
- Prints "Hello, World!" to the console
- Follows Python best practices including shebang line, main function pattern, type annotations, and Google-style docstrings
- Is executable via `uv run python hello.py`
- Adheres to all project linting and type checking requirements (ruff, mypy, black)
- Can serve as a template for simple Python scripts in the project

## Relevant Files

### Existing Files

- `CLAUDE.md` (lines 1-330) - Contains project principles (KISS, YAGNI), coding standards, type annotation requirements, Google-style docstring requirements, and the mandate to use `uv run` for executing scripts
- `pyproject.toml` (lines 1-124) - Defines project configuration including Python version (3.12+), linting rules (ruff), type checking rules (mypy with strict mode), and formatting rules (black)
- `.python-version` - Specifies Python version for the project

### New Files

- `hello.py` - New simple hello world script in the root directory
- `tests/test_hello.py` - Unit tests for the hello script (per CLAUDE.md requirement that every file in src/ must have corresponding test, though this is a root-level script we should still test it)

## Relevant Research Documentation

Use these documentation files and links to help with understanding the technology to use:

- [Python Official Documentation - Modules](https://docs.python.org/3/tutorial/modules.html)
  - [Python Scripts and __main__](https://docs.python.org/3/library/__main__.html)
  - Understanding how to structure Python scripts with the main guard pattern
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
  - [Shebang Lines](https://peps.python.org/pep-0008/#id49)
  - Standard style guide for Python code
- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
  - [Function Docstrings](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods)
  - Google-style docstring format required by the project
- [Python Type Hints - PEP 484](https://peps.python.org/pep-0484/)
  - [Basic Type Annotations](https://docs.python.org/3/library/typing.html)
  - Type annotation requirements for strict mypy compliance
- [UV Documentation - Running Scripts](https://docs.astral.sh/uv/)
  - [uv run command](https://docs.astral.sh/uv/guides/scripts/)
  - How to run Python scripts using uv package manager

## Implementation Plan

### Phase 1: Foundation

Create the basic hello script structure following Python best practices:
- Set up proper shebang line for Unix/Linux compatibility
- Implement main function pattern with type annotations
- Add comprehensive Google-style docstrings
- Ensure the script can be run with `uv run python hello.py`

### Phase 2: Core Implementation

Implement the hello world functionality with:
- Clean, minimal implementation following KISS principle
- Type annotations for all functions (strict mypy compliance)
- Google-style docstrings for module and functions
- Proper error handling (if needed)

### Phase 3: Integration

Ensure the script integrates with project tooling:
- Verify ruff linting passes
- Verify mypy type checking passes
- Verify black formatting is correct
- Create corresponding unit tests

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### 1. Create the hello.py script in root directory

- Create `hello.py` in the root directory (`/tmp/agent-work-orders/sandbox-wo-b1cb7e30/`)
- Add proper shebang line: `#!/usr/bin/env python3`
- Add comprehensive module-level Google-style docstring explaining the script's purpose
- Implement `main()` function with proper type annotations (return type `-> None`)
- Add Google-style docstring to `main()` function
- Implement `print("Hello, World!")` inside main function
- Add proper `if __name__ == "__main__":` guard
- Call `main()` within the guard

### 2. Verify the script runs correctly

- Test the script runs with: `uv run python hello.py`
- Verify output is exactly: `Hello, World!`
- Test that the script is properly structured and imports can be tested

### 3. Run linting and type checking

- Run ruff linting: `uv run ruff check hello.py`
- Fix any linting issues identified
- Run mypy type checking: `uv run mypy hello.py`
- Fix any type checking issues identified
- Run black formatting check: `uv run black --check hello.py`
- Apply black formatting if needed: `uv run black hello.py`

### 4. Create unit tests for the hello script

- Create `tests/test_hello.py` file
- Add proper module-level docstring
- Import pytest and the hello module
- Create test function `test_main_prints_hello_world()` with Google-style docstring
- Use pytest's `capsys` fixture to capture stdout
- Test that calling `main()` prints "Hello, World!\n" to stdout
- Mark test with `@pytest.mark.unit` decorator per project testing requirements
- Add any additional edge case tests if needed

### 5. Run all validation commands

- Execute all validation commands listed below to ensure zero regressions
- Fix any issues that arise
- Ensure all tests pass with 100% success rate

## Testing Strategy

See `CLAUDE.md` for complete testing requirements. Every file must have comprehensive tests.

### Unit Tests

- **test_main_prints_hello_world**: Verify that calling `main()` prints "Hello, World!" to stdout using pytest's capsys fixture
- Mark all tests with `@pytest.mark.unit` decorator
- Tests should be isolated and not depend on external state
- Use proper Google-style docstrings for all test functions

### Integration Tests

Not applicable for this simple script. This is a standalone script with no integration points.

### Edge Cases

- **Test import**: Verify the module can be imported without executing main (guard works correctly)
- **Test stdout content**: Verify exact output including newline character
- **Test no side effects**: Verify importing the module doesn't produce output

## Acceptance Criteria

1. `hello.py` script exists in the root directory
2. Script can be executed with `uv run python hello.py` and outputs "Hello, World!"
3. Script includes proper shebang line for Unix/Linux compatibility
4. Script uses main function pattern with `if __name__ == "__main__":` guard
5. All functions have complete type annotations
6. All functions and the module have Google-style docstrings
7. Script passes ruff linting with zero errors
8. Script passes mypy type checking with zero errors
9. Script is formatted according to black standards
10. Unit tests exist in `tests/test_hello.py` and all tests pass
11. Test coverage for the main functionality is 100%
12. Code follows project's KISS and YAGNI principles

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

**Required validation commands:**

```bash
# Run the hello script
uv run python hello.py

# Lint check must pass
uv run ruff check hello.py

# Type check must pass
uv run mypy hello.py

# Format check must pass
uv run black --check hello.py

# All unit tests must pass
uv run pytest tests/test_hello.py -v -m unit

# Run full test suite to ensure no regressions
uv run pytest tests/ -v

# Verify test coverage for hello script
uv run pytest tests/test_hello.py --cov=hello --cov-report=term-missing
```

**Expected outputs:**

- `uv run python hello.py` should output: `Hello, World!`
- All linting commands should pass with zero errors
- All type checking should pass with zero errors
- All tests should pass with 100% success rate
- Test coverage should be 100% for the hello module

## Notes

### Design Decisions

- **Root Directory Placement**: The script is placed in the root directory for easy access and visibility
- **Minimal Implementation**: Following KISS principle, the script does the minimum required
- **Type Annotations**: Even though the script is simple, type annotations are included to demonstrate best practices and satisfy strict mypy requirements
- **Main Function Pattern**: Using the main function pattern even for a simple script demonstrates proper Python structure
- **Testing**: Including tests even for a simple script demonstrates the project's commitment to testing and provides an example for contributors

### Future Considerations

- This script can serve as a template for other simple utility scripts
- The testing approach can be used as a reference for testing other standalone scripts
- Could potentially be extended to accept command-line arguments if needed (but YAGNI applies here)

### Additional Context

- The script follows the project's convention of using `uv run` for execution
- All code adheres to the project's strict mypy and ruff configuration
- The implementation prioritizes simplicity and clarity over clever or complex solutions
