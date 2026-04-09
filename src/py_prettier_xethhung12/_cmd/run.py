import argparse
import sys

import py_prettier_xethhung12 as project
from j_vault_http_client_xethhung12 import client


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="py-prettier-xethhung12",
        description="Format XML, HTML, or JSON from stdin and print to stdout.",
    )
    subparsers = parser.add_subparsers(dest="parser", required=True, help="Parser to use")

    # JSON subcommand
    subparsers.add_parser("json", help="Format JSON")

    # XML subcommand
    subparsers.add_parser("xml", help="Format XML")

    # HTML subcommand
    subparsers.add_parser("html", help="Format HTML")

    # Add common arguments to all subcommands
    for subparser in subparsers.choices.values():
        # Input options group
        input_group = subparser.add_mutually_exclusive_group()
        input_group.add_argument(
            "--stdin",
            action="store_true",
            default=False,
            help="Read from stdin (default if no input option specified).",
        )
        input_group.add_argument(
            "-f",
            "--file",
            type=str,
            default=None,
            help="Input file path.",
        )
        input_group.add_argument(
            "--from-clip",
            action="store_true",
            help="Read from clipboard.",
        )
        
        # Output options group
        output_group = subparser.add_mutually_exclusive_group()
        output_group.add_argument(
            "--stdout",
            action="store_true",
            default=True,
            help="Output to stdout (default).",
        )
        output_group.add_argument(
            "--clip",
            action="store_true",
            help="Copy output to clipboard.",
        )
        output_group.add_argument(
            "-o",
            "--output",
            type=str,
            default=None,
            help="Output file path. If specified, writes to this file instead of stdout.",
        )

    return parser


def main():
    client.load_to_env()

    args = build_parser().parse_args()

    # Read input from various sources
    if args.from_clip:
        # Read from clipboard
        try:
            import pyperclip
            text = pyperclip.paste()
            if not text:
                print("Error: Clipboard is empty.", file=sys.stderr)
                sys.exit(1)
        except ImportError:
            print(
                "Error: 'pyperclip' is not installed. Install it with: pip install pyperclip",
                file=sys.stderr,
            )
            sys.exit(1)
        except Exception as exc:
            print(f"Error reading from clipboard: {exc}", file=sys.stderr)
            sys.exit(1)
    elif args.file:
        # Read from file
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        except Exception as exc:
            print(f"Error reading file: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        # Default: read from stdin
        text = sys.stdin.read()

    try:
        result = project.format_text(text, args.parser)
        
        # Handle output based on user options
        if args.clip:
            # Output to clipboard
            try:
                import pyperclip
                pyperclip.copy(result)
                print("Output copied to clipboard.", file=sys.stderr)
            except ImportError:
                print(
                    "Error: 'pyperclip' is not installed. Install it with: pip install pyperclip",
                    file=sys.stderr,
                )
                sys.exit(1)
            except Exception as exc:
                print(f"Error copying to clipboard: {exc}", file=sys.stderr)
                sys.exit(1)
        elif args.output:
            # Output to file
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result)
                    if not result.endswith("\n"):
                        f.write("\n")
                print(f"Output written to '{args.output}'.", file=sys.stderr)
            except Exception as exc:
                print(f"Error writing to file: {exc}", file=sys.stderr)
                sys.exit(1)
        else:
            # Default: output to stdout
            # Use sys.stdout.buffer to write UTF-8 encoded bytes directly
            # This prevents 'charmap' codec errors on Windows with Unicode characters
            sys.stdout.buffer.write(result.encode("utf-8"))
            if not result.endswith("\n"):
                sys.stdout.buffer.write(b"\n")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
