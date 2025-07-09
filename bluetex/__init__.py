"""Bluetex: A LaTeX document cleaner and formatter.

Bluetex is a tool for cleaning and formatting LaTeX documents. It removes
comments, modernizes outdated syntax, improves spacing, and applies various
other formatting improvements to make LaTeX documents more readable and
consistent.
"""

from . import cli
from .__about__ import __version__
from .main import clean

__all__: list[str] = ["__version__", "cli", "clean"]
