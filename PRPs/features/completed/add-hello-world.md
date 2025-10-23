# Feature: Add Hello World Python Script

## Feature Description

This feature adds a simple "hello.py" script to the root directory of the Dylan project. The script will serve as a minimal demonstration of Python execution and can be used for testing purposes or as a starting point for quick script development. The implementation follows the project's KISS (Keep It Simple, Stupid) principle by creating the simplest possible working script with proper Python conventions including type hints, Google-style docstrings, and executable permissions.

## User Story

As a developer working with the Dylan project
I want to have a simple hello.py script in the root directory
So that I can quickly test Python execution, verify my environment setup, and have a minimal example for reference

## Problem Statement

The project currently lacks a simple, standalone Python script in the root directory that can be used for:
- Quick testing of Python environment setup
- Demonstrating basic Python execution with `uv run`
- Providing a minimal example for new contributors
- Serving as a template for simple utility scripts

## Solution Statement

Create a `hello.py` file in the project root directory that:
- Prints "Hello, World!" to the console
- Follows Python best practices with type hints and docstrings
- Can be executed directly with `uv run python hello.py`
- Includes a shebang line for direct execution on Unix systems
- Adheres to the project's code quality standards (ruff, mypy, black)

## Relevant Files

### Existing Files

- `CLAUDE.md` (lines 1-330) - Contains project principles, code standards, and development workflow
  - Lines 5-21: Core principles (KISS, YAGNI) that guide simple implementations
  - Lines 20-21: Requirement to use `uv run` for script execution
  - Lines 90-107: Development commands for linting, type checking, and formatting

- `pyproject.toml` (lines 1-124) - Project configuration and dependencies
  - Lines 10-24: Project metadata and dependencies
  - Lines 42-82: Code quality tool configurations (black, ruff, mypy)
  - Lines 89-95: Mypy configuration requiring type hints

### New Files

- `hello.py` - The new Python script to be created in the root directory
  - Will contain a simple main function that prints "Hello, World!"
  - Must include type hints and Google-style docstrings
  - Should have executable permissions with proper shebang

- `tests/test_hello.py` - Unit tests for the hello.py script
  - Will test the main function output
  - Will verify the script can be imported and executed
  - Must follow pytest conventions with proper markers

## Relevant research docstring

Use these documentation files and links to help with understanding the technology to use:

- [Python Type Hints - PEP 484](https://peps.python.org/pep-0484/)
  - [Basic type hints syntax](https://peps.python.org/pep-0484/#type-definition-syntax)
  - Type annotations for function signatures and return types

- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
  - [Function docstring format](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods)
  - Module-level docstrings with examples

- [Python shebang best practices](https://docs.python.org/3/using/unix.html#miscellaneous)
  - Using `#!/usr/bin/env python3` for portability
  - Making scripts executable with proper permissions

- [uv documentation - Running scripts](https://docs.astral.sh/uv/guides/scripts/)
  - [Script execution with uv run](https://docs.astral.sh/uv/guides/scripts/#running-scripts)
  - Best practices for Python script execution in uv environments

## Implementation Plan

### Phase 1: Foundation

Create the basic hello.py script structure with minimal functionality. Set up the file with proper Python conventions including shebang, module docstring, and type hints. Ensure the script follows the project's KISS principle by keeping it as simple as possible while still meeting code quality standards.

### Phase 2: Core Implementation

Implement the main function that prints "Hello, World!" to stdout. Add proper type annotations and Google-style docstrings. Verify the script can be executed with `uv run python hello.py` and passes all linting and type checking requirements.

### Phase 3: Integration

Add unit tests to validate the script's functionality. Ensure the implementation integrates seamlessly with the project's testing infrastructure and CI/CD pipeline. Run all validation commands to confirm zero regressions.

## Step by Step Tasks

### Step 1: Create hello.py script

- Create `hello.py` in the root directory with the following structure:
  - Add shebang line: `#!/usr/bin/env python3`
  - Add module-level docstring explaining the script's purpose
  - Define a `main() -> None` function with proper type hints
  - Implement print statement: `print("Hello, World!")`
  - Add `if __name__ == "__main__":` guard with `main()` call
  - Include Google-style docstring for the main function

### Step 2: Verify code quality standards

- Run `uv run ruff check hello.py` to ensure linting passes
- Run `uv run mypy hello.py` to verify type hints are correct
- Run `uv run black hello.py --check` to validate formatting
- Fix any issues identified by the tools

### Step 3: Test script execution

- Execute the script with `uv run python hello.py`
- Verify "Hello, World!" is printed to stdout
- Confirm no errors or warnings are produced
- Test direct execution (if permissions allow)

### Step 4: Create unit tests

- Create `tests/test_hello.py` with proper test structure
- Import pytest and the hello module
- Write `test_main_output()` function using `capsys` fixture to capture stdout
- Verify the output matches "Hello, World!\n"
- Mark test with `@pytest.mark.unit` decorator
- Add module-level docstring to test file

### Step 5: Run validation commands

- Execute `uv run ruff check .` to lint all code including new files
- Execute `uv run mypy .` to type check the entire project
- Execute `uv run pytest tests/test_hello.py -v` to run unit tests
- Verify all commands pass with zero errors
- Confirm no regressions in existing functionality

## Testing Strategy

See `CLAUDE.md` for complete testing requirements. Every file in `src/` must have a corresponding test file in `tests/`. Since this is a root-level script (not in src/), we'll create tests/test_hello.py to maintain consistency.

### Unit Tests

Mark with `@pytest.mark.unit`. Test the individual function in isolation:

- `test_main_output()` - Verify that calling `main()` prints "Hello, World!" to stdout
  - Use pytest's `capsys` fixture to capture stdout
  - Assert captured output equals "Hello, World!\n"
  - Verify function returns None

- `test_main_callable()` - Verify the main function is callable
  - Import the main function
  - Assert it's callable with `callable(main)`
  - Verify it has proper type annotations

### Integration Tests

Not applicable for this simple standalone script. No integration with other components is required.

### Edge Cases

- Empty/None edge cases not applicable for this simple script
- No user input or external dependencies to test
- Script should work in any Python 3.12+ environment

## Acceptance Criteria

- [ ] `hello.py` file exists in the root directory
- [ ] Script prints "Hello, World!" when executed with `uv run python hello.py`
- [ ] Script has proper type hints on all functions (mypy passes)
- [ ] Script has Google-style docstrings for module and functions
- [ ] Script passes ruff linting with zero errors
- [ ] Script is formatted with black (line length 100)
- [ ] Unit tests exist in `tests/test_hello.py` and pass
- [ ] All validation commands execute successfully with zero regressions
- [ ] Script follows KISS principle - minimal, simple implementation

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

**Required validation commands:**

- `uv run ruff check .` - Lint check must pass for entire project
- `uv run mypy .` - Type check must pass for entire project
- `uv run pytest tests/test_hello.py -v` - Unit tests for hello.py must pass
- `uv run python hello.py` - Script execution must print "Hello, World!"

**Additional validation:**

- `uv run black hello.py --check` - Verify formatting is correct
- `uv run black tests/test_hello.py --check` - Verify test file formatting
- `cat hello.py` - Manual review of code structure and docstrings
- `cat tests/test_hello.py` - Manual review of test structure

**Full regression test:**

- `uv run pytest dylan/ -v` - Ensure no regressions in existing tests (if any exist)

## Notes

- This is intentionally a minimal implementation following the KISS principle
- The script is placed in the root directory as requested, not in src/ or concept_library/
- No external dependencies are needed beyond Python standard library
- The script serves as a simple example and testing tool for the project
- Future enhancements could include command-line arguments, but YAGNI principle applies
- Since the script is not in src/, it won't be part of the main package distribution
- The script can serve as a template for other simple utility scripts
- Tests are placed in tests/ to maintain consistency with project structure
