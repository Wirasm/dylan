# Dylan Goodbye Command

A simple CLI command that prints a friendly farewell message when invoked.

## Purpose

The `goodbye` command provides users with a polite way to exit or conclude their Dylan CLI session. It complements the existing welcome message shown when Dylan is invoked without arguments, creating a complete and friendly user experience.

## Usage

```bash
# Print farewell message
dylan goodbye
```

## Command Output

The command displays a stylized farewell message using Dylan's UI theme:
- Arrow and spark symbols for visual consistency
- Branded colors matching other Dylan commands
- Friendly farewell text

## Implementation

The goodbye command is implemented as a simple Typer command with no arguments or options. It uses the shared UI theme components (`ARROW`, `SPARK`, `COLORS`) to maintain visual consistency with other Dylan utilities.

## Testing

Run the unit tests:

```bash
uv run pytest dylan/utility_library/dylan_goodbye/tests/ -v
```

## Architecture

- **dylan_goodbye_cli.py**: Core CLI implementation using Typer and Rich
- **tests/test_goodbye_cli.py**: Unit tests for the goodbye command
- **__init__.py**: Package exports

## Design Principles

Following KISS (Keep It Simple, Stupid) and YAGNI (You Aren't Gonna Need It):
- Minimal functionality with no unnecessary features
- No external dependencies beyond project requirements
- Simple, self-contained implementation
- Consistent with existing command patterns
