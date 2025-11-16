"""PyMUD-SS13 Textual TUI Client launcher."""

from __future__ import annotations

import argparse
import sys

from .app import run_app


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PyMUD-SS13 Terminal User Interface Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:\n  python -m tui_client\n  python -m tui_client --host 192.168.1.100\n  python -m tui_client --host example.com --port 8080\n\nControls:\n  F1  - Game view\n  F2  - Inventory view\n  F3  - Map view\n  F4  - Help view\n  F10 - Quit\n\nFor more information, visit the Help view (F4) after logging in.""",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Server host address (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Server port number (default: 5000)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="PyMUD-SS13 TUI Client v1.0.0",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Main entry point for launching the Textual client."""
    parser = build_parser()
    args = parser.parse_args(argv)
    server_url = f"ws://{args.host}:{args.port}/ws"

    print(f"Connecting to PyMUD-SS13 server at {server_url}...")
    print("Press F10 or Ctrl+C to quit at any time.\n")

    try:
        run_app(server_url)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as exc:  # pragma: no cover - defensive guard rail
        print(f"\nError: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
