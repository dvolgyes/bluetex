"""Click-based CLI for bluetex.

This module provides a modern Click-based command-line interface for bluetex,
replacing the legacy argparse-based CLI with better user experience and logging.
"""

import sys
from pathlib import Path
from sys import version_info as vi

import click
from loguru import logger

from ..__about__ import __version__
from ..main import clean


@click.command()
@click.argument("infiles", nargs=-1, required=True, type=click.Path(exists=True))
@click.option(
    "-e",
    "--encoding",
    default=None,
    help="Encoding to use for reading and writing files",
)
@click.option(
    "-i",
    "--in-place",
    is_flag=True,
    help="Modify all files in place",
)
@click.option(
    "-c",
    "--keep-comments",
    is_flag=True,
    help="Keep comments",
)
@click.option(
    "-d",
    "--keep-dollar",
    is_flag=True,
    help="Keep inline math with $...$",
)
@click.option(
    "--logfile",
    type=click.Path(),
    help="Log file path for output",
)
@click.option(
    "--loglevel",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default="INFO",
    help="Log level",
)
@click.version_option(
    version=f"bluetex {__version__}, Python {vi.major}.{vi.minor}.{vi.micro}"
)
def main(
    infiles: tuple[str, ...],
    encoding: str | None,
    in_place: bool,
    keep_comments: bool,
    keep_dollar: bool,
    logfile: str | None,
    loglevel: str,
) -> None:
    """Clean up LaTeX files.

    Processes one or more LaTeX files, applying various formatting improvements
    and modernizations. Files can be processed in-place or output to stdout.

    Args:
        infiles: Tuple of input file path strings to process
        encoding: Character encoding for reading/writing files
        in_place: If True, modify files in place; otherwise output to stdout
        keep_comments: If True, preserve comments in output
        keep_dollar: If True, preserve $...$ math delimiters
        logfile: Optional path string for log file output
        loglevel: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Convert string paths to Path objects
    infile_paths = [Path(f) for f in infiles]
    logfile_path = Path(logfile) if logfile else None

    # Configure logging - remove default handler and add custom ones
    logger.remove()  # Remove default handler

    # Add stderr handler with specified level
    logger.add(sys.stderr, level=loglevel.upper())

    # Add file handler if specified
    if logfile_path:
        logger.add(logfile_path, level=loglevel.upper())

    logger.debug(
        f"Processing {len(infile_paths)} files with encoding={encoding}, in_place={in_place}"
    )

    stdout_parts: list[str] = []
    return_code = 0

    for infile in infile_paths:
        logger.debug(f"Processing file: {infile}")

        try:
            with infile.open(encoding=encoding) as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file {infile}: {e}")
            return_code = 1
            continue

        try:
            cleaned_content = clean(content, keep_comments, keep_dollar)
        except Exception as e:
            logger.error(f"Error cleaning file {infile}: {e}")
            return_code = 1
            continue

        if in_place:
            # Check if content changed - return code 1 indicates changes were made
            if content != cleaned_content:
                return_code = 1

            try:
                with infile.open("w", encoding=encoding) as f:
                    f.write(cleaned_content)
                logger.info(f"Updated file: {infile}")
            except Exception as e:
                logger.error(f"Error writing file {infile}: {e}")
                return_code = 1
        else:
            stdout_parts.append(cleaned_content)

    if not in_place:
        # Write to stdout without trailing newline for consistency with original behavior
        print("\n".join(stdout_parts), end="")

    sys.exit(return_code)


if __name__ == "__main__":
    main()  # pragma: no cover
