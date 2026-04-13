import argparse
import sys

import py_prettier_xethhung12 as project
from j_vault_http_client_xethhung12 import client


def _add_input_args(parser: argparse.ArgumentParser) -> None:
    """Add input source arguments to an input subparser."""
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--stdin",
        action="store_true",
        default=False,
        help="Read from stdin (default if no input option specified).",
    )
    group.add_argument(
        "-f",
        "--file",
        type=str,
        default=None,
        help="Input file path.",
    )
    group.add_argument(
        "--from-clip",
        action="store_true",
        help="Read from clipboard.",
    )


def _add_output_args(parser: argparse.ArgumentParser) -> None:
    """Add output destination arguments to an output subparser."""
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--stdout",
        action="store_true",
        default=True,
        help="Output to stdout (default).",
    )
    group.add_argument(
        "--to-clip",
        action="store_true",
        help="Copy output to clipboard.",
    )
    group.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="py-prettier-xethhung12",
        description="Format XML, HTML, or JSON from stdin and print to stdout.",
    )
    subparsers = parser.add_subparsers(dest="parser", required=True, help="Input format")

    # ── json ──────────────────────────────────────────────────────────────────
    json_parser = subparsers.add_parser("json", help="Input is JSON")
    _add_input_args(json_parser)
    json_subs = json_parser.add_subparsers(dest="output_format", required=True, help="Output format")
    _add_output_args(json_subs.add_parser("prettify", help="Prettify JSON"))

    json_xml_sub = json_subs.add_parser("xml", help="Convert JSON to XML")
    json_xml_sub.add_argument(
        "--root",
        type=str,
        default="root",
        metavar="ELEMENT",
        help="Root element name when JSON has multiple top-level keys (default: 'root').",
    )
    json_xml_sub.add_argument(
        "--attr-prefix",
        type=str,
        default="@",
        metavar="PREFIX",
        help="Key prefix that marks XML attributes (default: '@').",
    )
    json_xml_sub.add_argument(
        "--mode",
        choices=["default", "auto"],
        default="default",
        help="Attribute mapping mode. 'default': keys prefixed with --attr-prefix become attributes. "
             "'auto': primitive values become attributes, objects/arrays become subnodes.",
    )
    _add_output_args(json_xml_sub)

    # ── xml ───────────────────────────────────────────────────────────────────
    xml_parser = subparsers.add_parser("xml", help="Input is XML")
    _add_input_args(xml_parser)
    xml_subs = xml_parser.add_subparsers(dest="output_format", required=True, help="Output format")
    _add_output_args(xml_subs.add_parser("prettify", help="Prettify XML"))

    xml_json_sub = xml_subs.add_parser("json", help="Convert XML to JSON")
    xml_json_sub.add_argument(
        "--attr-prefix",
        type=str,
        default="@",
        metavar="PREFIX",
        help="Prefix for XML attribute keys (default: '@'). Pass '' for plain field names.",
    )
    xml_json_sub.add_argument(
        "--skip-root",
        action="store_true",
        default=False,
        help="Skip the root element and return its children directly.",
    )
    _add_output_args(xml_json_sub)

    # ── html ──────────────────────────────────────────────────────────────────
    html_parser = subparsers.add_parser("html", help="Input is HTML")
    _add_input_args(html_parser)
    html_subs = html_parser.add_subparsers(dest="output_format", required=True, help="Output format")
    _add_output_args(html_subs.add_parser("prettify", help="Prettify HTML"))

    return parser


def main():
    client.load_to_env()

    args = build_parser().parse_args()

    # Read input
    if args.from_clip:
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
        if args.parser == "xml" and args.output_format == "json":
            result = project.xml_to_json(text, attr_prefix=args.attr_prefix, skip_root=args.skip_root)
        elif args.parser == "json" and args.output_format == "xml":
            result = project.json_to_xml(text, root=args.root, attr_prefix=args.attr_prefix, mode=args.mode)
        else:
            result = project.format_text(text, args.parser)

        # Write output
        if args.to_clip:
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
            # Use sys.stdout.buffer to write UTF-8 encoded bytes directly
            # This prevents 'charmap' codec errors on Windows with Unicode characters
            sys.stdout.buffer.write(result.encode("utf-8"))
            if not result.endswith("\n"):
                sys.stdout.buffer.write(b"\n")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
