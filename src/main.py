#!/usr/bin/env python3
"""
Main entry point for the Base Converter application.
Can launch either GUI or CLI based on arguments.
"""

import argparse
import sys
from typing import List, Optional


def parse_launcher_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse arguments to determine which interface to launch."""
    parser = argparse.ArgumentParser(
        prog="base-converter",
        description="Base Converter - Choose interface",
        add_help=False,  # We'll handle help differently
    )

    parser.add_argument(
        "--gui", action="store_true", help="Launch graphical user interface"
    )

    parser.add_argument(
        "--cli",
        action="store_true",
        help="Use command-line interface (default if number provided)",
    )

    parser.add_argument("--help", "-h", action="store_true", help="Show help message")

    # Parse known args to handle cases where CLI args are passed
    known_args, remaining = parser.parse_known_args(args)

    # If no interface specified but there are remaining args or a number, use CLI
    if not known_args.gui and not known_args.cli:
        if remaining or (
            args
            and any(
                arg.lstrip("-").replace(".", "").isdigit()
                or any(c in arg for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                for arg in args[:1]
                if not arg.startswith("-")
            )
        ):
            known_args.cli = True
        else:
            known_args.gui = True

    known_args.remaining = remaining
    return known_args


def show_main_help():
    """Show help for the main launcher."""
    help_text = """
Base Converter v1.0 - A comprehensive cross-platform base conversion utility

USAGE:
  base-converter [--gui|--cli] [CLI_OPTIONS...]
  base-converter NUMBER [OPTIONS...]  # Uses CLI interface
  base-converter --gui                # Uses GUI interface

INTERFACES:
  --gui     Launch graphical user interface (default if no number provided)
  --cli     Use command-line interface (default if number provided)

GUI MODE:
  Launches an intuitive graphical interface with:
  - Visual number input and base selection
  - Real-time conversion with validation
  - Conversion history and tables
  - Arithmetic calculator
  - Batch processing tools
  - Export functionality

CLI MODE:
  Command-line interface for scripting and quick conversions:
  - Single conversions: base-converter 1010 -f 2 -t 10
  - Interactive mode: base-converter --interactive
  - Batch processing: base-converter --batch numbers.txt
  - Arithmetic: base-converter 1010 1011 --arithmetic +

EXAMPLES:
  base-converter --gui                    # Launch GUI
  base-converter 1010 -f 2 -t 10         # CLI: Binary to decimal
  base-converter FF --from 16 --to 2     # CLI: Hex to binary  
  base-converter 255 --table             # CLI: Show conversion table
  base-converter --interactive           # CLI: Interactive mode

For detailed CLI help: base-converter --cli --help
For GUI help: Use the Help menu in the GUI application

Visit: https://github.com/6639835/base-converter
"""
    print(help_text)


def main(args: Optional[List[str]] = None):
    """Main entry point that launches the appropriate interface."""
    if args is None:
        args = sys.argv[1:]

    try:
        launcher_args = parse_launcher_args(args)

        if launcher_args.help:
            show_main_help()
            return 0

        if launcher_args.gui:
            # Launch GUI
            try:
                from src import gui

                gui_main = gui.main

                gui_main()
                return 0
            except ImportError as e:
                print(f"Error: Could not import GUI module: {e}")
                print("GUI may not be available on this system.")
                return 1
            except Exception as e:
                print(f"GUI Error: {e}")
                return 1

        elif launcher_args.cli:
            # Launch CLI with remaining arguments
            try:
                from src import cli

                cli_main = cli.main

                sys.argv = ["base-converter"] + launcher_args.remaining
                return cli_main()
            except ImportError as e:
                print(f"Error: Could not import CLI module: {e}")
                return 1
            except Exception as e:
                print(f"CLI Error: {e}")
                return 1

        else:
            # Default fallback
            show_main_help()
            return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
