"""
Legacy CLI module for backward compatibility.

This module maintains compatibility with the old argparse-based CLI
while redirecting to the new click-based implementation. It preserves
the exact same command-line interface and behavior as the original.
"""

import argparse
from sys import version_info as vi

from .__about__ import __version__
from .main import clean


def main(argv: list[str] | None = None) -> int:
    """Legacy main function for backward compatibility.

    This function maintains the same interface as the original argparse-based CLI
    but processes files using the core clean function directly.

    Args:
        argv: Command-line arguments (uses sys.argv if None)

    Returns:
        Exit code: 0 for success, 1 if any files were modified (when using --in-place)
    """
    parser = _get_parser()
    args = parser.parse_args(argv)

    stdout: list[str] = []
    return_code = 0

    # Process each input file
    for fl in args.infiles:
        with open(fl.name, encoding=args.encoding) as f:
            content = f.read()

        # Clean the content using the core cleaning function
        out = clean(content, args.keep_comments, args.keep_dollar_math)

        if args.in_place:
            # Return code indicates if any changes were made
            return_code = return_code or int(content != out)
            with open(fl.name, "w", encoding=args.encoding) as f:
                f.write(out)
        else:
            stdout.append(out)

    if not args.in_place:
        # Output to stdout without trailing newline for consistency
        print("\n".join(stdout), end="")

    return return_code


def _get_parser() -> argparse.ArgumentParser:
    """Create argparse parser for legacy CLI.

    Returns:
        Configured argument parser with all CLI options
    """
    parser = argparse.ArgumentParser(description="Clean up LaTeX files.")

    parser.add_argument(
        "infiles",
        nargs="+",
        type=argparse.FileType("r"),
        help="input LaTeX file",
    )

    parser.add_argument(
        "-e",
        "--encoding",
        type=str,
        default=None,
        help="encoding to use for reading and writing files",
    )

    parser.add_argument(
        "-i", "--in-place", action="store_true", help="modify all files in place"
    )

    parser.add_argument(
        "-c", "--keep-comments", action="store_true", help="keep comments"
    )

    parser.add_argument(
        "-d",
        "--keep-dollar-math",
        action="store_true",
        help="keep inline math with $...$",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"bluetex {__version__}, Python {vi.major}.{vi.minor}.{vi.micro}",
    )

    return parser
