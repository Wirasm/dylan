# Feature: Hello World Function

## Feature Description

Create a simple hello world function in a new file called `hello_world_test_from_archon.py`. The function should accept a name parameter, print a personalized greeting message to stdout, and return the greeting string for programmatic use. This is a demonstration feature that follows Python 3.12+ best practices with full type safety, Google-style docstrings, and comprehensive testing.

## User Story

As a developer
I want to have a simple hello world function with proper type hints and documentation
So that I can use it as a reference implementation for creating well-documented, type-safe Python functions in this project

## Problem Statement

The project needs a reference implementation demonstrating:
- Python 3.12+ type hints and modern syntax
- Google-style docstrings following project conventions
- Proper testing structure with unit tests
- Compliance with project linting and type checking requirements
- KISS principle: simple, maintainable code

## Solution Statement

Implement a standalone module `hello_world_test_from_archon.py` containing a `greet` function that:
- Accepts an optional name parameter (defaults to "World")
- Prints a greeting message to stdout
- Returns the greeting string for programmatic use
- Includes full type annotations using Python 3.12 syntax
- Has a comprehensive Google-style docstring
- Includes example usage in a `__main__` block
- Has corresponding unit tests in the test suite

## Relevant Files

### Existing Files for Reference

- **CLAUDE.md** (lines 1-330) - Project principles, coding standards, type safety requirements, testing conventions
  - Relevant because: Defines KISS/YAGNI principles, type safety as core rule, Google-style docstring requirements

- **pyproject.toml** (entire file) - Project configuration for linting, type checking, and testing
  - Relevant because: Shows ruff, mypy, and pytest configuration that the new code must pass

- **dylan/utility_library/shared/exit_command.py** - Example of simple utility functions with proper documentation
  - Relevant because: Demonstrates Google-style docstrings, type hints, and function design patterns used in the project

- **dylan/utility_library/shared/tests/test_exit_command.py** - Example test structure
  - Relevant because: Shows testing patterns, pytest conventions, and how to structure unit tests

### New Files

- **hello_world_test_from_archon.py** (new file at project root) - Main implementation
  - Contains the `greet()` function with type hints and docstring
  - Includes `__main__` block for direct execution

- **dylan/tests/test_hello_world_test_from_archon.py** (new test file) - Unit tests
  - Tests default behavior (no name provided)
  - Tests custom name behavior
  - Tests return value correctness
  - Tests output formatting

## Relevant research docstring

Use these documentation files and links to help with understanding the technology to use:

- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
  - Section 3.8: Comments and Docstrings
  - Shows proper format for function docstrings with Args, Returns, and Examples sections

- [Python Type Hints Documentation](https://docs.python.org/3.12/library/typing.html)
  - Type hints reference for Python 3.12
  - Modern syntax using `str | None` instead of `Optional[str]`

- [Real Python - Documenting Python Code](https://realpython.com/documenting-python-code/)
  - Complete guide to Python documentation
  - Best practices for docstrings and type hints working together

- [Python 3.12 Type Hint Improvements](https://www.andy-pearce.com/blog/posts/2023/Dec/whats-new-in-python-312-type-hint-improvements/)
  - New features in Python 3.12 for type hints
  - Use of modern union syntax with `|`

## Implementation Plan

### Phase 1: Foundation

Create the basic function implementation following Python 3.12 best practices:
- Define function signature with complete type annotations
- Write comprehensive Google-style docstring
- Implement simple logic following KISS principle
- Add `__main__` block for direct execution demonstration

### Phase 2: Core Implementation

Implement the `greet()` function in `hello_world_test_from_archon.py`:
- Accept optional `name` parameter with default value
- Use type hints: `def greet(name: str = "World") -> str:`
- Print formatted greeting to stdout
- Return the greeting string
- Include docstring with Args, Returns, and Examples sections

### Phase 3: Testing and Validation

Create comprehensive unit tests and validate code quality:
- Write unit tests in `dylan/tests/test_hello_world_test_from_archon.py`
- Test default behavior, custom names, return values, and output
- Run linters (ruff) and type checker (mypy)
- Verify all tests pass with zero regressions

## Step by Step Tasks

### 1. Create the main module file

- Create `hello_world_test_from_archon.py` at the project root
- Add module-level docstring explaining the purpose
- Define the `greet()` function with type hints
- Implement function logic: print and return greeting
- Add comprehensive Google-style docstring with Args, Returns, and Examples
- Add `__main__` block for demonstrating usage
- Follow Python 3.12 modern syntax (`str` type hints, f-strings)

### 2. Create the test file

- Create `dylan/tests/test_hello_world_test_from_archon.py`
- Import pytest and the `greet` function
- Mark tests with `@pytest.mark.unit` decorator
- Write test for default behavior: `test_greet_default()`
- Write test for custom name: `test_greet_custom_name()`
- Write test for return value: `test_greet_return_value()`
- Write test for output verification using `capsys` fixture
- Follow existing test patterns from `test_exit_command.py`

### 3. Run linting checks

- Execute `uv run ruff check hello_world_test_from_archon.py`
- Execute `uv run ruff check dylan/tests/test_hello_world_test_from_archon.py`
- Fix any linting issues (naming, formatting, imports)
- Ensure line length is within 100 characters

### 4. Run type checking

- Execute `uv run mypy hello_world_test_from_archon.py --strict`
- Execute `uv run mypy dylan/tests/test_hello_world_test_from_archon.py`
- Verify no type errors are reported
- Ensure all functions have complete type annotations

### 5. Run unit tests

- Execute `uv run pytest dylan/tests/test_hello_world_test_from_archon.py -v`
- Verify all tests pass
- Check test coverage includes all function paths
- Confirm zero test failures or errors

### 6. Run full validation suite

- Execute all validation commands listed below
- Verify module can be imported successfully
- Test direct execution: `uv run python hello_world_test_from_archon.py`
- Test with custom name: `uv run python hello_world_test_from_archon.py "Claude"`
- Confirm zero regressions in existing tests

## Testing Strategy

See `CLAUDE.md` for complete testing requirements. Every file in `dylan/` must have a corresponding test file in `dylan/tests/`.

### Unit Tests

All unit tests should be marked with `@pytest.mark.unit` decorator and placed in `dylan/tests/test_hello_world_test_from_archon.py`:

1. **test_greet_default()** - Verify function works with default "World" parameter
   - Assert return value is "Hello, World!"
   - Verify correct output to stdout

2. **test_greet_custom_name()** - Verify function works with custom name
   - Test with single name: "Alice"
   - Assert return value is "Hello, Alice!"
   - Verify correct output to stdout

3. **test_greet_return_value()** - Verify return type is string
   - Assert return value is of type `str`
   - Verify return value matches expected format

4. **test_greet_empty_string()** - Edge case: empty string as name
   - Test with empty string: `greet("")`
   - Assert return value is "Hello, !"

5. **test_greet_special_characters()** - Edge case: name with special characters
   - Test with name containing unicode: "José"
   - Assert proper handling of special characters

### Integration Tests

Not applicable for this simple standalone function. No integration with other components required.

### Edge Cases

- Empty string as name parameter
- Name with unicode/special characters (émojis, accents)
- Very long name strings (test string length limits)
- Whitespace-only name strings
- Name with newline or tab characters

## Acceptance Criteria

1. **Functionality**
   - Function accepts optional name parameter with default "World"
   - Function prints greeting message to stdout
   - Function returns greeting string
   - Module can be executed directly via `__main__` block

2. **Code Quality**
   - All functions have complete type annotations (passes `mypy --strict`)
   - All functions have Google-style docstrings
   - Code passes all ruff linting checks
   - Code follows KISS principle - no unnecessary complexity

3. **Testing**
   - Unit tests achieve 100% code coverage
   - All tests pass with zero failures
   - Tests are properly marked with `@pytest.mark.unit`
   - Tests follow existing project patterns

4. **Documentation**
   - Docstring includes clear description
   - Docstring documents Args section
   - Docstring documents Returns section
   - Docstring includes Examples section
   - Module docstring explains purpose

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

**Linting checks:**
```bash
uv run ruff check hello_world_test_from_archon.py
uv run ruff check dylan/tests/test_hello_world_test_from_archon.py
```

**Type checking:**
```bash
uv run mypy hello_world_test_from_archon.py --strict
uv run mypy dylan/tests/test_hello_world_test_from_archon.py
```

**Unit tests:**
```bash
uv run pytest dylan/tests/test_hello_world_test_from_archon.py -v -m unit
```

**Full test suite (verify zero regressions):**
```bash
uv run pytest dylan/tests/ -v
```

**Manual execution tests:**
```bash
# Test default behavior
uv run python hello_world_test_from_archon.py

# Test module import
uv run python -c "from hello_world_test_from_archon import greet; print(greet('Claude'))"
```

**Required validation commands:**
- `uv run ruff check hello_world_test_from_archon.py` - Lint check must pass
- `uv run mypy hello_world_test_from_archon.py --strict` - Type check must pass
- `uv run pytest dylan/tests/test_hello_world_test_from_archon.py -v` - All tests must pass

## Notes

### Design Decisions

- **File location**: Placed at project root for easy access and demonstration
- **Function name**: `greet()` is more descriptive than `hello_world()`
- **Return value**: Function both prints and returns for maximum flexibility
- **Default parameter**: "World" follows traditional hello world convention

### Future Considerations

This is a simple demonstration feature. Potential enhancements could include:
- Support for multiple languages/localization
- Customizable greeting messages beyond "Hello"
- Integration with Dylan CLI as a subcommand
- Extended greeting formats (time-based greetings, etc.)

However, following YAGNI principle, these features should only be added if explicitly needed.

### Additional Context

This feature demonstrates the project's commitment to:
- Type safety as a core rule (strict mypy checking)
- Comprehensive documentation (Google-style docstrings)
- Thorough testing (unit tests for all code paths)
- Simple, maintainable code (KISS principle)
- Modern Python practices (Python 3.12+ syntax)
