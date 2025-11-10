#!/usr/bin/env python3
"""
PyMUD-SS13 Textual TUI Client Launcher

Launch the terminal user interface for PyMUD-SS13.

Usage:
    python tui_client.py [options]

Options:
    --host HOST     Server host (default: localhost)
    --port PORT     Server port (default: 5000)
    --help          Show this help message
"""

import sys
import argparse
from tui_client.app import run_app


def main():
    """Main entry point for the TUI client."""
    parser = argparse.ArgumentParser(
        description="PyMUD-SS13 Terminal User Interface Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tui_client.py
  python tui_client.py --host 192.168.1.100
  python tui_client.py --host example.com --port 8080

Controls:
  F1  - Game view
  F2  - Inventory view
  F3  - Map view
  F4  - Help view
  F10 - Quit

For more information, visit the Help view (F4) after logging in.
        """
    )

    parser.add_argument(
        "--host",
        default="localhost",
        help="Server host address (default: localhost)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Server port number (default: 5000)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="PyMUD-SS13 TUI Client v1.0.0"
    )

    args = parser.parse_args()

    # Construct WebSocket URL
    server_url = f"ws://{args.host}:{args.port}/ws"

    print(f"Connecting to PyMUD-SS13 server at {server_url}...")
    print("Press F10 or Ctrl+C to quit at any time.")
    print()

    try:
        run_app(server_url)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
