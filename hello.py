#!/usr/bin/env python3
"""Simple Hello World script demonstrating Python best practices.

This script provides a minimal example of proper Python script structure including:
- Shebang line for Unix/Linux compatibility
- Main function pattern with type annotations
- Google-style docstrings
- Proper if __name__ == "__main__" guard

The script follows the project's KISS (Keep It Simple, Stupid) and YAGNI
(You Aren't Gonna Need It) principles by providing minimal functionality
with maximum clarity.
"""


def main() -> None:
    """Print Hello, World! to the console.

    This is the main entry point of the script. It demonstrates a simple
    function with proper type annotations and docstring.
    """
    print("Hello, World!")


if __name__ == "__main__":
    main()
