#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = ["typer[all]"]
# ///
import typer
from pathlib import Path
from typing import Annotated
from enum import Enum


class Format(str, Enum):
    json = "json"
    csv = "csv"
    text = "text"


app = typer.Typer(help="🚀 File processing toolkit")


@app.command()
def analyze(
    file: Annotated[Path, typer.Argument(help="File to analyze", exists=True)],
    format: Annotated[
        Format, typer.Option("--format", "-f", help="Output format")
    ] = Format.text,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Show detailed output")
    ] = False,
    limit: Annotated[int, typer.Option(min=1, max=100, help="Limit results")] = 10,
):
    """📊 Analyze file content and show statistics"""
    content = file.read_text()
    lines = len(content.splitlines())
    words = len(content.split())
    chars = len(content)

    if format == Format.json:
        import json

        data = {"file": str(file), "lines": lines, "words": words, "chars": chars}
        if verbose:
            data["top_words"] = content.lower().split()[:limit]
        typer.echo(json.dumps(data, indent=2))
    elif format == Format.csv:
        typer.echo("metric,value")
        typer.echo(f"lines,{lines}")
        typer.echo(f"words,{words}")
        typer.echo(f"chars,{chars}")
    else:
        typer.echo(f"📁 File: {file.name}")
        typer.echo(f"📝 Lines: {lines}")
        typer.echo(f"🔤 Words: {words}")
        typer.echo(f"📊 Characters: {chars}")
        if verbose:
            typer.echo(
                f"📋 First {limit} words: {' '.join(content.lower().split()[:limit])}"
            )


@app.command()
def transform(
    file: Annotated[Path, typer.Argument(help="Input file", exists=True)],
    output: Annotated[Path, typer.Option("--output", "-o", help="Output file")] = None,
    uppercase: Annotated[
        bool, typer.Option("--upper", help="Convert to uppercase")
    ] = False,
    reverse: Annotated[bool, typer.Option("--reverse", help="Reverse lines")] = False,
    confirm: Annotated[
        bool, typer.Option("--yes", "-y", help="Skip confirmation")
    ] = False,
):
    """🔄 Transform file content with various operations"""
    content = file.read_text()
    lines = content.splitlines()

    if uppercase:
        lines = [line.upper() for line in lines]
    if reverse:
        lines = lines[::-1]

    result = "\n".join(lines)
    output_file = output or file.with_suffix(f".transformed{file.suffix}")

    if not confirm:
        typer.confirm(f"Write to {output_file}?", abort=True)

    output_file.write_text(result)
    typer.secho(
        f"✅ Transformed content written to {output_file}", fg=typer.colors.GREEN
    )


if __name__ == "__main__":
    app()
