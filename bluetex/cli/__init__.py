"""CLI module for bluetex.

This module provides command-line interface functionality for bluetex.
It imports the legacy main function for backward compatibility while
the new Click-based CLI is in the main.py module.
"""

# Import the legacy main function for backward compatibility
from ..legacy_cli import main

__all__: list[str] = ["main"]
