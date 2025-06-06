#!/usr/bin/env python3
import argparse
import sys

parser = argparse.ArgumentParser(description="Greet people from a list of names")
parser.add_argument(
    "greeting", nargs="?", default="Hello", help="greeting message (default: Hello)"
)
parser.add_argument("-i", "--input", help="input file with names")
parser.add_argument(
    "--no-exclamation", action="store_true", help="don't add exclamation mark"
)
args = parser.parse_args()

# Determine input source
if args.input:
    file = open(args.input)
elif not sys.stdin.isatty():
    file = sys.stdin
else:
    print("Error: No input file specified and no data piped to stdin", file=sys.stderr)
    sys.exit(1)

# Process names
punctuation = "" if args.no_exclamation else "!"
for line in file:
    if name := line.strip():
        print(f"{args.greeting}, {name}{punctuation}")

if args.input:
    file.close()
