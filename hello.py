#!/usr/bin/env python3
"""A simple hello world script for testing Python execution.

This script demonstrates basic Python execution and can be used for:
- Quick testing of Python environment setup
- Demonstrating basic Python execution with `uv run`
- Providing a minimal example for new contributors
- Serving as a template for simple utility scripts

Example:
    $ uv run python hello.py
    Hello, World!
"""


def main() -> None:
    """Print a hello world message to stdout.

    This is the main entry point of the script. It prints "Hello, World!"
    to the console without any additional formatting or arguments.

    Returns:
        None
    """
    print("Hello, World!")


if __name__ == "__main__":
    main()
