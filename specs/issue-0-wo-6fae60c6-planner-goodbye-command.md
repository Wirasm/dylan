# Feature: Goodbye Command

## Feature Description

A simple CLI command that prints a friendly farewell message when invoked. This command provides users with a polite way to exit or conclude their Dylan CLI session, complementing the existing welcome message shown when Dylan is invoked without arguments.

## User Story

As a Dylan CLI user
I want to run a goodbye command
So that I can receive a friendly farewell message when ending my CLI session

## Problem Statement

The Dylan CLI currently provides a welcoming experience when users start their session (via the main help screen), but lacks a corresponding farewell mechanism. Users may want a friendly way to close their interaction with the tool, especially when working in long terminal sessions where a polite goodbye can improve the overall user experience.

## Solution Statement

Implement a simple `dylan goodbye` command that prints a stylized farewell message using Dylan's existing UI theme. The command will be lightweight, self-contained, and follow the KISS principle by providing only the essential functionality without unnecessary complexity. The implementation will use the existing UI theme components (colors, symbols, formatting) to maintain visual consistency with other Dylan commands.

## Relevant Files

- **dylan/cli.py** - Main CLI entry point where the new goodbye command will be registered
- **dylan/utility_library/shared/ui_theme.py** - Contains shared UI components (COLORS, ARROW, SPARK, create_header) that the goodbye command will use for consistent styling

### New Files

- **dylan/utility_library/dylan_goodbye/__init__.py** - Package initialization file
- **dylan/utility_library/dylan_goodbye/dylan_goodbye_cli.py** - CLI implementation for the goodbye command
- **dylan/utility_library/dylan_goodbye/tests/__init__.py** - Test package initialization
- **dylan/utility_library/dylan_goodbye/tests/test_goodbye_cli.py** - Unit tests for the goodbye command
- **dylan/utility_library/dylan_goodbye/README.md** - Documentation for the goodbye command

## Implementation Plan

### Phase 1: Foundation

Create the directory structure and package files for the new goodbye command utility. This includes creating the `dylan_goodbye` directory under `utility_library` with proper Python package initialization files.

### Phase 2: Core Implementation

Implement the goodbye command CLI function using Typer. The function will:
- Accept no required arguments
- Use Rich console for output
- Leverage existing ui_theme components for consistent styling
- Print a farewell message with Dylan's signature visual elements (arrow, spark, colors)

### Phase 3: Integration

Register the goodbye command in the main Dylan CLI (`dylan/cli.py`) and update the help table to include the new command. Ensure the command follows the same patterns as existing commands like `review`, `dev`, and `pr`.

## Step by Step Tasks

### Step 1: Create Directory Structure

- Create directory `dylan/utility_library/dylan_goodbye/`
- Create directory `dylan/utility_library/dylan_goodbye/tests/`

### Step 2: Create Package Initialization Files

- Create `dylan/utility_library/dylan_goodbye/__init__.py` with proper exports
- Create `dylan/utility_library/dylan_goodbye/tests/__init__.py`

### Step 3: Implement the Goodbye CLI

- Create `dylan/utility_library/dylan_goodbye/dylan_goodbye_cli.py`
- Implement the `goodbye()` function using Typer
- Use Rich console for styled output
- Import and use ui_theme components (COLORS, ARROW, SPARK, create_header)
- Create a farewell message with proper styling
- Add proper type hints for all function parameters and return types
- Include docstring with usage examples

### Step 4: Write Unit Tests

- Create `dylan/utility_library/dylan_goodbye/tests/test_goodbye_cli.py`
- Write test for successful command execution
- Test that the function prints expected output
- Use pytest fixtures as needed
- Ensure tests follow the project's testing conventions

### Step 5: Create Documentation

- Create `dylan/utility_library/dylan_goodbye/README.md`
- Document command purpose and usage
- Include examples of command invocation
- Follow documentation patterns from other utility READMEs

### Step 6: Register Command in Main CLI

- Edit `dylan/cli.py` to import the goodbye command
- Add the goodbye command using `app.command()`
- Update the help table in the `_main()` callback to include the goodbye command
- Ensure the command follows the naming and help text patterns of existing commands

### Step 7: Run Validation Commands

- Execute all validation commands listed below
- Fix any issues that arise
- Ensure zero regressions in existing functionality

## Testing Strategy

### Unit Tests

- **test_goodbye_command_executes**: Verify the goodbye function executes without errors
- **test_goodbye_output_format**: Test that output includes expected styling elements (colors, symbols)
- **test_goodbye_console_output**: Verify Rich console is used for output

### Integration Tests

- **Manual CLI test**: Run `dylan goodbye` from command line to verify end-to-end functionality
- **Help text test**: Verify `dylan --help` displays the goodbye command
- **Command registration test**: Verify the command is properly registered in the Typer app

### Edge Cases

- Running goodbye command with no arguments (expected behavior)
- Running goodbye command multiple times in succession (should work each time)
- Verifying goodbye doesn't interfere with other commands

## Acceptance Criteria

- [ ] `dylan goodbye` command executes successfully and prints a farewell message
- [ ] The farewell message uses Dylan's UI theme (colors, arrow, spark symbols)
- [ ] Command appears in `dylan --help` output with appropriate description
- [ ] All unit tests pass with 100% coverage of the goodbye module
- [ ] Code follows project conventions: type hints, docstrings, KISS/YAGNI principles
- [ ] No regressions in existing commands or functionality
- [ ] Documentation clearly explains command purpose and usage
- [ ] Code passes all linters (ruff, black, mypy)

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv sync

# Run the goodbye command
uv run dylan goodbye

# Verify command appears in help
uv run dylan --help

# Run all tests
uv run pytest dylan/utility_library/dylan_goodbye/tests/ -v

# Run type checking
uv run mypy dylan/utility_library/dylan_goodbye/

# Run linting
uv run ruff check dylan/utility_library/dylan_goodbye/

# Format code
uv run black dylan/utility_library/dylan_goodbye/

# Run all project tests to ensure no regressions
uv run pytest -v

# Test installation and command availability
uv pip install -e .
dylan goodbye
dylan --help
```

## Notes

- This is a simple utility command following KISS/YAGNI principles
- No external dependencies are required beyond what's already in the project
- The command is intentionally minimal and self-contained
- Future enhancements could include:
  - Optional custom farewell messages via command arguments
  - Random selection from multiple farewell messages
  - Integration with session statistics (if tracked in the future)
- These enhancements should only be added if user demand justifies the complexity
