#!/usr/bin/env python3
import sys

# Get greeting from command line argument, default to "Hello"
greeting = sys.argv[1] if len(sys.argv) > 1 else "Hello"

# Read names from standard input and greet each person
for line in sys.stdin:
    if name := line.strip():
        print(f"{greeting}, {name}!")
