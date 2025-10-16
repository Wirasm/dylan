"""Simple hello world module demonstrating Python 3.12+ best practices.

This module provides a basic greeting function that demonstrates:
- Python 3.12+ type hints with modern syntax
- Google-style docstrings
- Type safety compliance
- Simple, maintainable code following KISS principle
"""


def greet(name: str = "World") -> str:
    """Print and return a personalized greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        The formatted greeting string.

    Examples:
        >>> greet()
        Hello, World!
        'Hello, World!'

        >>> greet("Alice")
        Hello, Alice!
        'Hello, Alice!'

        >>> result = greet("Claude")
        Hello, Claude!
        >>> print(result)
        Hello, Claude!
    """
    greeting = f"Hello, {name}!"
    print(greeting)
    return greeting


if __name__ == "__main__":
    import sys

    # If name is provided as command line argument, use it
    if len(sys.argv) > 1:
        greet(sys.argv[1])
    else:
        greet()
