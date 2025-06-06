#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
# ]
# ///

import typer
import sys
from pathlib import Path


def main(
    greeting: str = typer.Argument("Hello", help="greeting message"),
    input_file: Path | None = typer.Option(
        None, "-i", "--input", help="input file with names"
    ),
    no_exclamation: bool = typer.Option(
        False, "--no-exclamation", help="don't add exclamation mark"
    ),
):
    """Greet people from a list of names"""

    # Determine input source
    if input_file:
        file = input_file.open()
    elif not sys.stdin.isatty():
        file = sys.stdin
    else:
        typer.echo(
            "Error: No input file specified and no data piped to stdin", err=True
        )
        raise typer.Exit(1)

    # Process names
    punctuation = "" if no_exclamation else "!"
    for line in file:
        if name := line.strip():
            typer.echo(f"{greeting}, {name}{punctuation}")

    if input_file:
        file.close()


if __name__ == "__main__":
    typer.run(main)
