#!/usr/bin/env python3
"""
Command-line interface for the Base Converter utility.
Provides comprehensive base conversion functionality via command line.
"""

import argparse
import os
import sys
from typing import Dict, List, Optional

from src.converter import BaseConverter, batch_convert
from src.validation import InputValidator, ValidationError


class BaseConverterCLI:
    """Command-line interface for base conversion operations."""

    def __init__(self):
        """Initialize the CLI with converter and validator instances."""
        self.converter = BaseConverter()
        self.validator = InputValidator()

    def create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            prog="base-converter",
            description="A comprehensive cross-platform base converter utility",
            epilog="Examples:\n"
            "  base-converter 1010 -f 2 -t 10  # Convert binary to decimal\n"
            "  base-converter FF -f 16 -t 2    # Convert hex to binary\n"
            "  base-converter 255 --table      # Show conversion table\n"
            "  base-converter --interactive     # Start interactive mode",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Main number argument
        parser.add_argument(
            "number",
            nargs="?",
            help="Number to convert (required unless using --interactive or --batch)",
        )

        # Base arguments
        parser.add_argument(
            "-f",
            "--from-base",
            type=int,
            default=10,
            metavar="BASE",
            help="Source base (2-36, default: 10)",
        )

        parser.add_argument(
            "-t",
            "--to-base",
            type=int,
            default=2,
            metavar="BASE",
            help="Target base (2-36, default: 2)",
        )

        # Output options
        parser.add_argument(
            "--table",
            action="store_true",
            help="Show conversion table for common bases (2, 8, 10, 16)",
        )

        parser.add_argument(
            "--format", action="store_true", help="Format output with digit separators"
        )

        parser.add_argument(
            "--prefix",
            action="store_true",
            help="Add standard prefix to output (0b, 0o, 0x)",
        )

        parser.add_argument(
            "--info",
            action="store_true",
            help="Show detailed information about the conversion",
        )

        # Operation modes
        parser.add_argument(
            "-i", "--interactive", action="store_true", help="Start interactive mode"
        )

        parser.add_argument(
            "--batch", metavar="FILE", help="Process numbers from file (one per line)"
        )

        parser.add_argument(
            "--arithmetic",
            metavar="OPERATION",
            choices=["+", "-", "*", "/", "%", "**"],
            help="Perform arithmetic operation on two numbers",
        )

        parser.add_argument(
            "--second-number",
            metavar="NUMBER",
            help="Second number for arithmetic operations",
        )

        # Utility options
        parser.add_argument(
            "--detect-base",
            action="store_true",
            help="Try to detect the base of the input number",
        )

        parser.add_argument(
            "--validate",
            action="store_true",
            help="Validate the conversion by converting back",
        )

        parser.add_argument(
            "--list-bases",
            action="store_true",
            help="List all supported bases with their names",
        )

        # Output control
        parser.add_argument(
            "-v", "--verbose", action="store_true", help="Enable verbose output"
        )

        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="Suppress all output except the result",
        )

        parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

        return parser

    def format_output(
        self,
        result: str,
        base: int,
        add_prefix: bool = False,
        add_separators: bool = False,
    ) -> str:
        """Format the output result with optional prefix and separators."""
        if add_separators:
            result = self.converter.format_number_with_separators(result, base)

        if add_prefix:
            prefixes = {2: "0b", 8: "0o", 16: "0x"}
            prefix = prefixes.get(base, "")
            if prefix and not result.startswith(prefix):
                is_negative = result.startswith("-")
                if is_negative:
                    result = "-" + prefix + result[1:]
                else:
                    result = prefix + result

        return result

    def print_conversion_table(
        self, number: str, source_base: int, verbose: bool = False
    ):
        """Print a conversion table showing the number in multiple bases."""
        try:
            table = self.converter.get_conversion_table(number, source_base)

            if verbose:
                print(f"\nConversion table for '{number}' (base {source_base}):")
                print("-" * 50)

            base_names = {2: "Binary", 8: "Octal", 10: "Decimal", 16: "Hexadecimal"}

            for base in [2, 8, 10, 16]:
                name = base_names[base]
                value = table[base]
                if verbose:
                    print(f"{name:>12} (base {base:>2}): {value}")
                else:
                    print(f"{base}: {value}")

        except Exception as e:
            print(f"Error generating conversion table: {e}", file=sys.stderr)

    def print_base_info(self, base: int):
        """Print information about a specific base."""
        try:
            info = self.converter.get_base_info(base)
            print(f"Base {base} ({info['name']}):")
            print(f"  Digits: {', '.join(info['digits'])}")
            print(f"  Digit count: {info['digit_count']}")
            print(f"  Maximum digit: {info['max_digit']}")
            if info["common_prefixes"]:
                print(f"  Common prefixes: {', '.join(info['common_prefixes'])}")
        except Exception as e:
            print(f"Error getting base info: {e}", file=sys.stderr)

    def list_all_bases(self):
        """List all supported bases with their names."""
        print("Supported bases:")
        print("-" * 30)
        for base in range(2, 37):
            try:
                info = self.converter.get_base_info(base)
                print(f"Base {base:>2}: {info['name']}")
            except:
                print(f"Base {base:>2}: Base-{base}")

    def process_arithmetic(
        self, num1: str, num2: str, operation: str, base: int
    ) -> str:
        """Process arithmetic operation on two numbers."""
        try:
            # Validate inputs
            self.validator.validate_number_for_base(num1, base)
            self.validator.validate_number_for_base(num2, base)
            self.validator.validate_operation(operation)

            # Perform operation based on base
            if base == 2:
                result = self.converter.binary_arithmetic(num1, num2, operation)
            else:
                # Convert to decimal, perform operation, convert back
                dec1 = self.converter.base_to_decimal(num1, base)
                dec2 = self.converter.base_to_decimal(num2, base)

                if operation == "+":
                    dec_result = dec1 + dec2
                elif operation == "-":
                    dec_result = dec1 - dec2
                elif operation == "*":
                    dec_result = dec1 * dec2
                elif operation == "/":
                    if dec2 == 0:
                        raise ValueError("Division by zero")
                    dec_result = dec1 // dec2
                elif operation == "%":
                    if dec2 == 0:
                        raise ValueError("Division by zero")
                    dec_result = dec1 % dec2
                elif operation == "**":
                    dec_result = dec1**dec2
                else:
                    raise ValueError(f"Unsupported operation: {operation}")

                result = self.converter.decimal_to_base(dec_result, base)

            return result

        except Exception as e:
            raise ValueError(f"Arithmetic error: {e}")

    def process_batch_file(
        self, filename: str, from_base: int, to_base: int, args
    ) -> None:
        """Process numbers from a batch file."""
        try:
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' not found", file=sys.stderr)
                return

            with open(filename, "r") as file:
                lines = [line.strip() for line in file.readlines() if line.strip()]

            if not lines:
                print("Error: Batch file is empty", file=sys.stderr)
                return

            print(f"Processing {len(lines)} numbers from '{filename}'...")
            print("-" * 50)

            for i, number in enumerate(lines, 1):
                try:
                    # Validate and convert
                    validated_number, _ = self.validator.validate_number_for_base(
                        number, from_base
                    )
                    result = self.converter.convert_base(
                        validated_number, from_base, to_base
                    )

                    # Format output
                    formatted_result = self.format_output(
                        result, to_base, args.prefix, args.format
                    )

                    if not args.quiet:
                        print(f"{i:>3}. {number} -> {formatted_result}")
                    else:
                        print(formatted_result)

                except Exception as e:
                    if not args.quiet:
                        print(f"{i:>3}. {number} -> Error: {e}")

        except Exception as e:
            print(f"Error processing batch file: {e}", file=sys.stderr)

    def interactive_mode(self):
        """Start interactive mode for continuous conversions."""
        print("Base Converter - Interactive Mode")
        print("Type 'help' for commands, 'quit' to exit")
        print("-" * 40)

        while True:
            try:
                command = input("\n> ").strip()

                if not command:
                    continue

                if command.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break

                if command.lower() == "help":
                    self.print_interactive_help()
                    continue

                if command.lower().startswith("list"):
                    self.list_all_bases()
                    continue

                # Parse interactive command
                parts = command.split()
                if len(parts) < 3:
                    print("Usage: <number> <from_base> <to_base>")
                    print("Example: 1010 2 10")
                    continue

                number, from_base_str, to_base_str = parts[0], parts[1], parts[2]

                try:
                    from_base = int(from_base_str)
                    to_base = int(to_base_str)
                except ValueError:
                    print("Error: Bases must be integers")
                    continue

                # Perform conversion
                validated_number, _ = self.validator.validate_number_for_base(
                    number, from_base
                )
                result = self.converter.convert_base(
                    validated_number, from_base, to_base
                )

                print(f"{number} (base {from_base}) = {result} (base {to_base})")

                # Show additional info if requested
                if len(parts) > 3 and "table" in parts[3:]:
                    self.print_conversion_table(number, from_base, verbose=True)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def print_interactive_help(self):
        """Print help for interactive mode."""
        print("\nInteractive Mode Commands:")
        print("  <number> <from_base> <to_base>  - Convert number between bases")
        print("  <number> <from_base> <to_base> table  - Show conversion table")
        print("  list                            - List all supported bases")
        print("  help                           - Show this help")
        print("  quit, exit, q                  - Exit interactive mode")
        print("\nExamples:")
        print("  1010 2 10      - Convert binary 1010 to decimal")
        print("  FF 16 2        - Convert hex FF to binary")
        print("  255 10 16      - Convert decimal 255 to hex")

    def run(self, args=None):
        """Main entry point for the CLI."""
        parser = self.create_parser()
        args = parser.parse_args(args)

        try:
            # Handle special modes first
            if args.list_bases:
                self.list_all_bases()
                return 0

            if args.interactive:
                self.interactive_mode()
                return 0

            if args.batch:
                self.process_batch_file(args.batch, args.from_base, args.to_base, args)
                return 0

            # Require number for other operations
            if not args.number:
                print(
                    "Error: Number is required unless using --interactive, --batch, or --list-bases",
                    file=sys.stderr,
                )
                parser.print_help()
                return 1

            # Validate bases
            from_base = self.validator.validate_base(args.from_base)
            to_base = self.validator.validate_base(args.to_base)

            # Handle base detection
            if args.detect_base:
                detected = self.converter.detect_base(args.number)
                if detected:
                    print(f"Detected base: {detected}")
                    from_base = detected
                else:
                    print("Could not detect base automatically")

            # Validate number for source base
            validated_number, has_prefix = self.validator.validate_number_for_base(
                args.number, from_base
            )

            # Handle arithmetic operations
            if args.arithmetic:
                if not args.second_number:
                    print(
                        "Error: --second-number is required for arithmetic operations",
                        file=sys.stderr,
                    )
                    return 1

                result = self.process_arithmetic(
                    validated_number, args.second_number, args.arithmetic, from_base
                )

                if not args.quiet:
                    print(
                        f"{args.number} {args.arithmetic} {args.second_number} = {result} (base {from_base})"
                    )
                else:
                    print(result)
                return 0

            # Perform conversion
            result = self.converter.convert_base(validated_number, from_base, to_base)

            # Format output
            formatted_result = self.format_output(
                result, to_base, args.prefix, args.format
            )

            # Display results
            if args.table:
                self.print_conversion_table(args.number, from_base, args.verbose)
            elif args.info:
                print(f"Input: {args.number} (base {from_base})")
                print(f"Output: {formatted_result} (base {to_base})")
                if has_prefix:
                    print("Note: Input had base prefix")
                if args.validate:
                    is_valid = self.converter.validate_conversion(
                        args.number, result, from_base, to_base
                    )
                    print(f"Validation: {'PASSED' if is_valid else 'FAILED'}")
            elif not args.quiet:
                print(
                    f"{args.number} (base {from_base}) = {formatted_result} (base {to_base})"
                )
            else:
                print(formatted_result)

            return 0

        except ValidationError as e:
            print(f"Validation error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            if args and args.verbose:
                import traceback

                traceback.print_exc()
            else:
                print(f"Error: {e}", file=sys.stderr)
            return 1


def main():
    """Entry point for the base-converter command."""
    cli = BaseConverterCLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
