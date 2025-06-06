#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def analyze_command(args):
    """Analyze file content and show statistics"""
    file = Path(args.file)
    if not file.exists():
        print(f"Error: File {file} does not exist", file=sys.stderr)
        sys.exit(1)

    content = file.read_text()
    lines = len(content.splitlines())
    words = len(content.split())
    chars = len(content)

    if args.format == "json":
        data = {"file": str(file), "lines": lines, "words": words, "chars": chars}
        if args.verbose:
            data["top_words"] = content.lower().split()[: args.limit]
        print(json.dumps(data, indent=2))
    elif args.format == "csv":
        print("metric,value")
        print(f"lines,{lines}")
        print(f"words,{words}")
        print(f"chars,{chars}")
    else:
        print(f"File: {file.name}")
        print(f"Lines: {lines}")
        print(f"Words: {words}")
        print(f"Characters: {chars}")
        if args.verbose:
            print(
                f"First {args.limit} words: {' '.join(content.lower().split()[: args.limit])}"
            )


def transform_command(args):
    """Transform file content with various operations"""
    file = Path(args.file)
    if not file.exists():
        print(f"Error: File {file} does not exist", file=sys.stderr)
        sys.exit(1)

    content = file.read_text()
    lines = content.splitlines()

    if args.uppercase:
        lines = [line.upper() for line in lines]
    if args.reverse:
        lines = lines[::-1]

    result = "\n".join(lines)
    output_file = (
        Path(args.output)
        if args.output
        else file.with_suffix(f".transformed{file.suffix}")
    )

    if not args.yes:
        response = input(f"Write to {output_file}? [y/N]: ")
        if response.lower() not in ["y", "yes"]:
            print("Aborted")
            sys.exit(1)

    output_file.write_text(result)
    print(f"Transformed content written to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="File processing toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze subcommand
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze file content and show statistics"
    )
    analyze_parser.add_argument("file", help="File to analyze")
    analyze_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv", "text"],
        default="text",
        help="Output format",
    )
    analyze_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    analyze_parser.add_argument(
        "--limit", type=int, default=10, help="Limit results (default: 10)"
    )

    # Transform subcommand
    transform_parser = subparsers.add_parser(
        "transform", help="Transform file content with various operations"
    )
    transform_parser.add_argument("file", help="Input file")
    transform_parser.add_argument("--output", "-o", help="Output file")
    transform_parser.add_argument(
        "--upper", dest="uppercase", action="store_true", help="Convert to uppercase"
    )
    transform_parser.add_argument(
        "--reverse", action="store_true", help="Reverse lines"
    )
    transform_parser.add_argument(
        "--yes", "-y", action="store_true", help="Skip confirmation"
    )

    args = parser.parse_args()

    if args.command == "analyze":
        # Validate limit range
        if not (1 <= args.limit <= 100):
            print("Error: limit must be between 1 and 100", file=sys.stderr)
            sys.exit(1)
        analyze_command(args)
    elif args.command == "transform":
        transform_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
