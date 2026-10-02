"""
Command-line interface for bangla-pdf-decoder.

Usage:
    bangla-pdf-decoder input.txt -o output.txt
    cat input.txt | bangla-pdf-decoder > output.txt
    bangla-pdf-decoder --text "চূড়াĢ Ïভাটার তািলকা"
"""

import argparse
import sys
from .decoder import decode_bangla_pdf_text


def main():
    parser = argparse.ArgumentParser(
        prog="bangla-pdf-decoder",
        description="Decode legacy & hybrid Bengali font encodings from PDF text into clean Unicode UTF-8.",
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        type=str,
        default=None,
        help="Input text file path (defaults to reading from stdin)",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output text file path (defaults to writing to stdout)",
    )
    parser.add_argument(
        "-t", "--text",
        type=str,
        default=None,
        help="Direct text string to decode",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    # Determine input text
    if args.text is not None:
        raw_text = args.text
    elif args.input_file:
        with open(args.input_file, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
    else:
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(1)
        raw_text = sys.stdin.read()

    decoded = decode_bangla_pdf_text(raw_text)

    # Determine output destination
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(decoded)
    else:
        # Ensure utf-8 output even on Windows consoles
        if sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(decoded)


if __name__ == "__main__":
    main()
