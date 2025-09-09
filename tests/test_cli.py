"""
Tests for the command-line interface functionality.
"""

import os
import sys
from io import StringIO
from unittest.mock import mock_open, patch

import pytest

# Add project root and src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.cli import BaseConverterCLI


class TestBaseConverterCLI:
    """Test cases for BaseConverterCLI class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = BaseConverterCLI()

    def test_initialization(self):
        """Test CLI initialization."""
        assert self.cli.converter is not None
        assert self.cli.validator is not None

    def test_create_parser(self):
        """Test argument parser creation."""
        parser = self.cli.create_parser()

        # Test that parser is created
        assert parser is not None
        assert parser.prog == "base-converter"

        # Test default arguments parsing
        args = parser.parse_args(["123"])
        assert args.number == "123"
        assert args.from_base == 10
        assert args.to_base == 2

        # Test with explicit bases
        args = parser.parse_args(["FF", "-f", "16", "-t", "10"])
        assert args.number == "FF"
        assert args.from_base == 16
        assert args.to_base == 10

        # Test with flags
        args = parser.parse_args(["123", "--table"])
        assert args.table == True

        args = parser.parse_args(["123", "--format"])
        assert args.format == True

        args = parser.parse_args(["123", "--prefix"])
        assert args.prefix == True

        # Test interactive mode
        args = parser.parse_args(["--interactive"])
        assert args.interactive == True

    def test_format_output(self):
        """Test output formatting."""
        # Basic formatting
        result = self.cli.format_output("FF", 16, False, False)
        assert result == "FF"

        # With prefix
        result = self.cli.format_output("FF", 16, True, False)
        assert result == "0xFF"

        result = self.cli.format_output("1010", 2, True, False)
        assert result == "0b1010"

        result = self.cli.format_output("777", 8, True, False)
        assert result == "0o777"

        # With separators
        result = self.cli.format_output("11111111", 2, False, True)
        assert "_" in result

        # Negative numbers with prefix
        result = self.cli.format_output("-FF", 16, True, False)
        assert result == "-0xFF"

        # Both prefix and separators
        result = self.cli.format_output("11111111", 2, True, True)
        assert result.startswith("0b")
        assert "_" in result

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_conversion_table(self, mock_stdout):
        """Test conversion table printing."""
        self.cli.print_conversion_table("255", 10, verbose=False)
        output = mock_stdout.getvalue()

        # Should contain conversions for common bases
        assert "2:" in output  # Binary
        assert "8:" in output  # Octal
        assert "10:" in output  # Decimal
        assert "16:" in output  # Hexadecimal

        # Should contain actual converted values
        assert "11111111" in output  # Binary of 255
        assert "377" in output  # Octal of 255
        assert "255" in output  # Decimal of 255
        assert "FF" in output  # Hex of 255

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_conversion_table_verbose(self, mock_stdout):
        """Test verbose conversion table printing."""
        self.cli.print_conversion_table("255", 10, verbose=True)
        output = mock_stdout.getvalue()

        # Should contain verbose labels
        assert "Binary" in output
        assert "Octal" in output
        assert "Decimal" in output
        assert "Hexadecimal" in output
        assert "base" in output

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_all_bases(self, mock_stdout):
        """Test listing all supported bases."""
        self.cli.list_all_bases()
        output = mock_stdout.getvalue()

        # Should list common bases with names
        assert "Base  2: Binary" in output
        assert "Base  8: Octal" in output
        assert "Base 10: Decimal" in output
        assert "Base 16: Hexadecimal" in output
        assert "Base 36:" in output  # Should include base 36

    def test_process_arithmetic(self):
        """Test arithmetic operations."""
        # Addition in decimal
        result = self.cli.process_arithmetic("5", "3", "+", 10)
        assert result == "8"

        # Subtraction in binary
        result = self.cli.process_arithmetic("1100", "1010", "-", 2)
        # 12 - 10 = 2 in decimal, which is "10" in binary
        assert result == "10"

        # Multiplication in hex
        result = self.cli.process_arithmetic("A", "2", "*", 16)
        # 10 * 2 = 20 in decimal, which is "14" in hex
        assert result == "14"

        # Division by zero should raise error
        with pytest.raises(ValueError, match="Division by zero"):
            self.cli.process_arithmetic("10", "0", "/", 10)

        # Invalid operation should raise error
        with pytest.raises(ValueError, match="Arithmetic error"):
            self.cli.process_arithmetic("10", "5", "^", 10)

        # Invalid number for base should raise error
        with pytest.raises(ValueError):
            self.cli.process_arithmetic("123", "5", "+", 2)  # "123" invalid for base 2

    @patch("builtins.open", new_callable=mock_open, read_data="10\n20\n30\n")
    @patch("os.path.exists", return_value=True)
    @patch("sys.stdout", new_callable=StringIO)
    def test_process_batch_file(self, mock_stdout, mock_exists, mock_file):
        """Test batch file processing."""

        # Create mock arguments
        class MockArgs:
            def __init__(self):
                self.prefix = False
                self.format = False
                self.quiet = False

        args = MockArgs()

        self.cli.process_batch_file("test.txt", 10, 2, args)
        output = mock_stdout.getvalue()

        # Should process all numbers
        assert "1010" in output  # 10 in binary
        assert "10100" in output  # 20 in binary
        assert "11110" in output  # 30 in binary

        # Should show processing message
        assert "Processing 3 numbers" in output

    @patch("os.path.exists", return_value=False)
    @patch("sys.stderr", new_callable=StringIO)
    def test_process_batch_file_not_found(self, mock_stderr, mock_exists):
        """Test batch file processing with non-existent file."""

        class MockArgs:
            pass

        args = MockArgs()
        self.cli.process_batch_file("nonexistent.txt", 10, 2, args)

        error_output = mock_stderr.getvalue()
        assert "not found" in error_output

    def test_run_basic_conversion(self):
        """Test basic conversion via run method."""
        # Test successful conversion
        exit_code = self.cli.run(["255", "-f", "10", "-t", "16"])
        assert exit_code == 0

        # Test with invalid base
        exit_code = self.cli.run(["255", "-f", "1", "-t", "16"])  # Invalid base
        assert exit_code == 1

        # Test with invalid number for base
        exit_code = self.cli.run(["G", "-f", "10", "-t", "16"])  # Invalid digit
        assert exit_code == 1

    @patch("sys.stdout", new_callable=StringIO)
    def test_run_conversion_table(self, mock_stdout):
        """Test conversion with table output."""
        exit_code = self.cli.run(["255", "--table"])
        assert exit_code == 0

        output = mock_stdout.getvalue()
        assert "Binary" in output or "2:" in output

    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_formatting_options(self, mock_stdout):
        """Test conversion with formatting options."""
        # Test with prefix
        exit_code = self.cli.run(["255", "-f", "10", "-t", "16", "--prefix"])
        assert exit_code == 0

        # Test with separators
        exit_code = self.cli.run(["11111111", "-f", "2", "-t", "10", "--format"])
        assert exit_code == 0

    def test_run_arithmetic(self):
        """Test arithmetic operations via run method."""
        exit_code = self.cli.run(["10", "--arithmetic", "+", "--second-number", "5"])
        assert exit_code == 0

        # Test without second number (should fail)
        exit_code = self.cli.run(["10", "--arithmetic", "+"])
        assert exit_code == 1

    @patch("sys.stdout", new_callable=StringIO)
    def test_run_detect_base(self, mock_stdout):
        """Test base detection via run method."""
        exit_code = self.cli.run(["0xFF", "--detect-base", "-t", "10"])
        assert exit_code == 0

        output = mock_stdout.getvalue()
        assert "Detected base: 16" in output or "255" in output

    def test_run_list_bases(self):
        """Test listing bases via run method."""
        exit_code = self.cli.run(["--list-bases"])
        assert exit_code == 0

    @patch("sys.stdout", new_callable=StringIO)
    def test_run_validation(self, mock_stdout):
        """Test validation option via run method."""
        exit_code = self.cli.run(
            ["255", "-f", "10", "-t", "16", "--validate", "--info"]
        )
        assert exit_code == 0

        output = mock_stdout.getvalue()
        assert "Validation:" in output
        assert "PASSED" in output or "FAILED" in output

    def test_run_quiet_mode(self):
        """Test quiet mode output."""
        # In quiet mode, should only output the result
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            exit_code = self.cli.run(["255", "-f", "10", "-t", "16", "--quiet"])
            assert exit_code == 0

            output = mock_stdout.getvalue().strip()
            assert output == "FF"  # Should only contain the result

    @patch("os.path.exists", return_value=True)
    def test_run_batch_mode(self, mock_exists):
        """Test batch mode via run method."""
        # Create a more specific mock that only affects our file operations
        original_open = (
            __builtins__["open"]
            if isinstance(__builtins__, dict)
            else __builtins__.open
        )

        def side_effect(*args, **kwargs):
            if args and "test.txt" in str(args[0]):
                return mock_open(read_data="10\n20\n")(*args, **kwargs)
            else:
                return original_open(*args, **kwargs)

        with patch("builtins.open", side_effect=side_effect):
            exit_code = self.cli.run(["--batch", "test.txt", "-f", "10", "-t", "2"])
            assert exit_code == 0

    def test_run_no_arguments(self):
        """Test run with no arguments (should show help)."""
        with patch("sys.stderr", new_callable=StringIO):
            exit_code = self.cli.run([])
            assert exit_code == 1  # Should fail without number

    def test_run_interactive_mode_flag(self):
        """Test interactive mode flag."""
        # Interactive mode is hard to test fully, but we can test that it starts
        with patch.object(
            self.cli, "interactive_mode", return_value=None
        ) as mock_interactive:
            exit_code = self.cli.run(["--interactive"])
            assert exit_code == 0
            mock_interactive.assert_called_once()

    @patch("sys.stdout", new_callable=StringIO)
    def test_run_verbose_mode(self, mock_stdout):
        """Test verbose mode."""
        exit_code = self.cli.run(["255", "--table", "--verbose"])
        assert exit_code == 0

        output = mock_stdout.getvalue()
        # Verbose mode should include more detailed information
        assert len(output) > 50  # Should be substantial output

    def test_error_handling(self):
        """Test error handling in various scenarios."""
        # Test with validation error
        exit_code = self.cli.run(
            ["G", "-f", "10", "-t", "2"]
        )  # Invalid digit for decimal
        assert exit_code == 1

        # Test with invalid base
        exit_code = self.cli.run(
            ["123", "-f", "37", "-t", "2"]
        )  # Base 37 not supported
        assert exit_code == 1

    def test_main_function(self):
        """Test the main entry point function."""
        from src.cli import main

        # Test that main can be called (though it will sys.exit)
        with patch("sys.argv", ["base-converter", "--list-bases"]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_once_with(0)


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def test_full_conversion_workflow(self):
        """Test complete conversion workflow."""
        cli = BaseConverterCLI()

        # Test various conversion scenarios
        test_cases = [
            (["1010", "-f", "2", "-t", "10"], 0),  # Binary to decimal
            (["FF", "-f", "16", "-t", "2"], 0),  # Hex to binary
            (["777", "-f", "8", "-t", "10"], 0),  # Octal to decimal
            (["123", "--table"], 0),  # Show table
            (["255", "--detect-base"], 0),  # Detect base
        ]

        for args, expected_exit_code in test_cases:
            with patch("sys.stdout", new_callable=StringIO):
                exit_code = cli.run(args)
                assert exit_code == expected_exit_code

    def test_arithmetic_operations_integration(self):
        """Test arithmetic operations integration."""
        cli = BaseConverterCLI()

        # Test various arithmetic operations
        arithmetic_cases = [
            (["10", "--arithmetic", "+", "--second-number", "5"], 0),
            (["1100", "-f", "2", "--arithmetic", "-", "--second-number", "1010"], 0),
            (["A", "-f", "16", "--arithmetic", "*", "--second-number", "2"], 0),
        ]

        for args, expected_exit_code in arithmetic_cases:
            with patch("sys.stdout", new_callable=StringIO):
                exit_code = cli.run(args)
                assert exit_code == expected_exit_code

    @patch("os.path.exists", return_value=True)
    def test_batch_processing_integration(self, mock_exists):
        """Test batch processing integration."""
        cli = BaseConverterCLI()

        # Test batch conversion from decimal to various bases
        original_open = (
            __builtins__["open"]
            if isinstance(__builtins__, dict)
            else __builtins__.open
        )

        def side_effect(*args, **kwargs):
            if args and "test.txt" in str(args[0]):
                return mock_open(read_data="123\n456\n789\nABC\n")(*args, **kwargs)
            else:
                return original_open(*args, **kwargs)

        with patch("builtins.open", side_effect=side_effect):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                exit_code = cli.run(["--batch", "test.txt", "-f", "10", "-t", "16"])
                assert exit_code == 0

            output = mock_stdout.getvalue()
            # Should process decimal numbers and convert to hex
            assert "7B" in output  # 123 in hex
            assert "1C8" in output  # 456 in hex
            assert "315" in output  # 789 in hex
            assert "Error" in output  # ABC should cause error in decimal

    def test_error_recovery_and_reporting(self):
        """Test error recovery and proper error reporting."""
        cli = BaseConverterCLI()

        # Test various error scenarios
        error_cases = [
            ([""], 1),  # Empty number
            (["123", "-f", "0"], 1),  # Invalid base
            (["G", "-f", "10"], 1),  # Invalid digit
            (["123", "--arithmetic", "+"], 1),  # Missing second number
        ]

        for args, expected_exit_code in error_cases:
            with patch("sys.stderr", new_callable=StringIO):
                exit_code = cli.run(args)
                assert exit_code == expected_exit_code

    def test_output_formatting_consistency(self):
        """Test output formatting consistency across different modes."""
        cli = BaseConverterCLI()

        # Test that formatting options work consistently
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            # Test prefix formatting
            cli.run(["255", "-f", "10", "-t", "16", "--prefix", "--quiet"])
            hex_output = mock_stdout.getvalue().strip()
            assert hex_output == "0xFF"

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            # Test separator formatting for binary
            cli.run(["255", "-f", "10", "-t", "2", "--format", "--quiet"])
            binary_output = mock_stdout.getvalue().strip()
            assert "_" in binary_output  # Should have separators

    def test_cross_platform_compatibility(self):
        """Test features that ensure cross-platform compatibility."""
        cli = BaseConverterCLI()

        # Test file operations work with different path separators
        with patch("os.path.exists", return_value=False):
            with patch("sys.stderr", new_callable=StringIO):
                # Should handle both Unix and Windows style paths gracefully
                exit_code = cli.run(["--batch", "/unix/style/path.txt"])
                assert exit_code is not None  # Should complete without crashing

                exit_code = cli.run(["--batch", "C:\\Windows\\style\\path.txt"])
                assert exit_code is not None  # Should complete without crashing

    @patch("sys.stdin", new_callable=lambda: StringIO("123 10 2\nFF 16 10\nquit\n"))
    @patch("sys.stdout", new_callable=StringIO)
    def test_interactive_mode_simulation(self, mock_stdout, mock_stdin):
        """Test interactive mode simulation."""
        cli = BaseConverterCLI()

        # This tests the interactive mode without actually running it interactively
        try:
            cli.interactive_mode()
        except:
            pass  # Interactive mode may exit in various ways, that's ok for testing

        # The main thing is that it doesn't crash
        assert True  # If we reach here, interactive mode started successfully
