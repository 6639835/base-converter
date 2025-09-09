"""
Tests for the core base conversion functionality.
"""

import os
import sys

# Add project root and src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest

from src.converter import (
    BaseConverter,
    batch_convert,
    quick_binary_to_decimal,
    quick_decimal_to_binary,
    quick_decimal_to_hex,
    quick_hex_to_decimal,
)


class TestBaseConverter:
    """Test cases for BaseConverter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = BaseConverter()

    def test_initialization(self):
        """Test BaseConverter initialization."""
        assert isinstance(self.converter.DIGITS, str)
        assert len(self.converter.DIGITS) == 36
        assert self.converter.DIGITS.startswith("0123456789")
        assert isinstance(self.converter.base_names, dict)
        assert 2 in self.converter.base_names
        assert 16 in self.converter.base_names

    def test_is_valid_number(self):
        """Test number validation for different bases."""
        # Valid cases
        assert self.converter.is_valid_number("1010", 2) == True
        assert self.converter.is_valid_number("777", 8) == True
        assert self.converter.is_valid_number("123", 10) == True
        assert self.converter.is_valid_number("ABC", 16) == True
        assert self.converter.is_valid_number("ZZZ", 36) == True
        assert self.converter.is_valid_number("-123", 10) == True
        assert self.converter.is_valid_number("0xFF", 16) == True
        assert self.converter.is_valid_number("0b1010", 2) == True
        assert self.converter.is_valid_number("0o777", 8) == True

        # Invalid cases
        assert self.converter.is_valid_number("2", 2) == False  # Invalid digit for base
        assert self.converter.is_valid_number("8", 8) == False  # Invalid digit for base
        assert (
            self.converter.is_valid_number("G", 16) == False
        )  # Invalid digit for base
        assert self.converter.is_valid_number("", 10) == False  # Empty string
        assert self.converter.is_valid_number("   ", 10) == False  # Whitespace only
        assert self.converter.is_valid_number("123", 1) == False  # Invalid base
        assert self.converter.is_valid_number("123", 37) == False  # Invalid base

    def test_decimal_to_base(self):
        """Test conversion from decimal to other bases."""
        # Binary conversions
        assert self.converter.decimal_to_base(10, 2) == "1010"
        assert self.converter.decimal_to_base(0, 2) == "0"
        assert self.converter.decimal_to_base(-10, 2) == "-1010"

        # Octal conversions
        assert self.converter.decimal_to_base(64, 8) == "100"
        assert self.converter.decimal_to_base(511, 8) == "777"

        # Hexadecimal conversions
        assert self.converter.decimal_to_base(255, 16) == "FF"
        assert self.converter.decimal_to_base(16, 16) == "10"
        assert self.converter.decimal_to_base(171, 16) == "AB"

        # Other bases
        assert self.converter.decimal_to_base(7, 3) == "21"
        assert self.converter.decimal_to_base(35, 36) == "Z"

        # Edge cases
        with pytest.raises(ValueError):
            self.converter.decimal_to_base(10, 1)  # Invalid base
        with pytest.raises(ValueError):
            self.converter.decimal_to_base(10, 37)  # Invalid base

    def test_base_to_decimal(self):
        """Test conversion from other bases to decimal."""
        # Binary conversions
        assert self.converter.base_to_decimal("1010", 2) == 10
        assert self.converter.base_to_decimal("0", 2) == 0
        assert self.converter.base_to_decimal("-1010", 2) == -10
        assert self.converter.base_to_decimal("0b1010", 2) == 10

        # Octal conversions
        assert self.converter.base_to_decimal("100", 8) == 64
        assert self.converter.base_to_decimal("777", 8) == 511
        assert self.converter.base_to_decimal("0o777", 8) == 511

        # Hexadecimal conversions
        assert self.converter.base_to_decimal("FF", 16) == 255
        assert self.converter.base_to_decimal("10", 16) == 16
        assert self.converter.base_to_decimal("AB", 16) == 171
        assert self.converter.base_to_decimal("0xFF", 16) == 255
        assert self.converter.base_to_decimal("0XFF", 16) == 255  # Different case

        # Other bases
        assert self.converter.base_to_decimal("21", 3) == 7
        assert self.converter.base_to_decimal("Z", 36) == 35

        # Invalid cases
        with pytest.raises(ValueError):
            self.converter.base_to_decimal("2", 2)  # Invalid digit
        with pytest.raises(ValueError):
            self.converter.base_to_decimal("G", 16)  # Invalid digit

    def test_convert_base(self):
        """Test direct base-to-base conversion."""
        # Binary to other bases
        assert self.converter.convert_base("1010", 2, 10) == "10"
        assert self.converter.convert_base("1010", 2, 8) == "12"
        assert self.converter.convert_base("1010", 2, 16) == "A"

        # Decimal to other bases
        assert self.converter.convert_base("255", 10, 2) == "11111111"
        assert self.converter.convert_base("255", 10, 8) == "377"
        assert self.converter.convert_base("255", 10, 16) == "FF"

        # Hex to other bases
        assert self.converter.convert_base("FF", 16, 10) == "255"
        assert self.converter.convert_base("FF", 16, 2) == "11111111"
        assert self.converter.convert_base("FF", 16, 8) == "377"

        # Same base conversion
        assert self.converter.convert_base("123", 10, 10) == "123"
        assert self.converter.convert_base("ABC", 16, 16) == "ABC"

    def test_convenience_methods(self):
        """Test convenience conversion methods."""
        # Binary conversions
        assert self.converter.to_binary("10") == "1010"
        assert self.converter.to_binary("FF", 16) == "11111111"

        # Octal conversions
        assert self.converter.to_octal("255") == "377"
        assert self.converter.to_octal("FF", 16) == "377"

        # Decimal conversions
        assert self.converter.to_decimal("1010", 2) == "10"
        assert self.converter.to_decimal("FF", 16) == "255"

        # Hexadecimal conversions
        assert self.converter.to_hexadecimal("255") == "FF"
        assert self.converter.to_hexadecimal("1010", 2) == "A"

    def test_binary_arithmetic(self):
        """Test arithmetic operations on binary numbers."""
        # Addition
        assert self.converter.binary_arithmetic("1010", "1100", "+") == "10110"

        # Subtraction
        assert self.converter.binary_arithmetic("1100", "1010", "-") == "10"

        # Multiplication
        assert self.converter.binary_arithmetic("101", "11", "*") == "1111"

        # Division
        assert self.converter.binary_arithmetic("1100", "11", "/") == "100"

        # Modulo
        assert self.converter.binary_arithmetic("1101", "11", "%") == "1"

        # Power
        assert self.converter.binary_arithmetic("10", "11", "**") == "1000"

        # Division by zero
        with pytest.raises(ValueError, match="Division by zero"):
            self.converter.binary_arithmetic("1010", "0", "/")

        with pytest.raises(ValueError, match="Division by zero"):
            self.converter.binary_arithmetic("1010", "0", "%")

        # Invalid operation
        with pytest.raises(ValueError, match="Unsupported operation"):
            self.converter.binary_arithmetic("1010", "1100", "^")

    def test_get_conversion_table(self):
        """Test conversion table generation."""
        table = self.converter.get_conversion_table("255", 10)

        assert isinstance(table, dict)
        assert len(table) == 4  # Binary, octal, decimal, hex
        assert table[2] == "11111111"
        assert table[8] == "377"
        assert table[10] == "255"
        assert table[16] == "FF"

    def test_format_number_with_separators(self):
        """Test number formatting with separators."""
        # Default settings (groups of 4 with underscore)
        assert (
            self.converter.format_number_with_separators("11111111", 2) == "1111_1111"
        )
        assert (
            self.converter.format_number_with_separators("123456789", 10)
            == "1_2345_6789"
        )

        # Custom separator and group size
        assert (
            self.converter.format_number_with_separators("11111111", 2, "-", 2)
            == "11-11-11-11"
        )

        # Negative numbers
        assert (
            self.converter.format_number_with_separators("-11111111", 2) == "-1111_1111"
        )

        # Short numbers (no formatting needed)
        assert self.converter.format_number_with_separators("123", 10) == "123"

    def test_get_base_info(self):
        """Test base information retrieval."""
        # Binary info
        info = self.converter.get_base_info(2)
        assert info["base"] == 2
        assert info["name"] == "Binary"
        assert info["digits"] == ["0", "1"]
        assert info["digit_count"] == 2
        assert info["max_digit"] == "1"
        assert "0b" in info["common_prefixes"]

        # Hex info
        info = self.converter.get_base_info(16)
        assert info["base"] == 16
        assert info["name"] == "Hexadecimal"
        assert len(info["digits"]) == 16
        assert info["max_digit"] == "F"
        assert "0x" in info["common_prefixes"]

        # Invalid base
        with pytest.raises(ValueError):
            self.converter.get_base_info(1)
        with pytest.raises(ValueError):
            self.converter.get_base_info(37)

    def test_detect_base(self):
        """Test automatic base detection."""
        # Prefix-based detection
        assert self.converter.detect_base("0b1010") == 2
        assert self.converter.detect_base("0B1010") == 2
        assert self.converter.detect_base("0o777") == 8
        assert self.converter.detect_base("0O777") == 8
        assert self.converter.detect_base("0xFF") == 16
        assert self.converter.detect_base("0XFF") == 16

        # Negative numbers with prefixes
        assert self.converter.detect_base("-0b1010") == 2
        assert self.converter.detect_base("-0xFF") == 16

        # Digit-based inference
        assert self.converter.detect_base("01") == 2
        assert self.converter.detect_base("01234567") == 8
        assert self.converter.detect_base("0123456789") == 10
        assert self.converter.detect_base("0123456789ABCDEF") == 16

        # Ambiguous cases (should suggest common bases)
        assert (
            self.converter.detect_base("123") == 10
        )  # Could be many bases, but 10 is most common
        assert self.converter.detect_base("ABC") == 16  # Contains letters, so hex

    def test_validate_conversion(self):
        """Test conversion validation by round-trip."""
        # Valid conversions
        assert self.converter.validate_conversion("1010", "10", 2, 10) == True
        assert self.converter.validate_conversion("255", "FF", 10, 16) == True
        assert self.converter.validate_conversion("FF", "377", 16, 8) == True

        # Invalid conversions (this shouldn't happen with correct implementation)
        assert self.converter.validate_conversion("1010", "11", 2, 10) == False

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Zero in different bases
        assert self.converter.convert_base("0", 2, 10) == "0"
        assert self.converter.convert_base("0", 10, 16) == "0"
        assert self.converter.convert_base("0", 36, 2) == "0"

        # Large numbers
        large_binary = "1" * 64  # 64-bit binary
        decimal_result = self.converter.base_to_decimal(large_binary, 2)
        back_to_binary = self.converter.decimal_to_base(decimal_result, 2)
        assert back_to_binary == large_binary

        # Maximum base (36)
        assert self.converter.convert_base("ZZ", 36, 10) == "1295"  # 35*36 + 35
        assert self.converter.convert_base("1295", 10, 36) == "ZZ"


class TestUtilityFunctions:
    """Test utility functions."""

    def test_quick_conversions(self):
        """Test quick conversion utility functions."""
        # Binary to decimal
        assert quick_binary_to_decimal("1010") == 10
        assert quick_binary_to_decimal("0") == 0
        assert quick_binary_to_decimal("11111111") == 255

        # Decimal to binary
        assert quick_decimal_to_binary(10) == "1010"
        assert quick_decimal_to_binary(0) == "0"
        assert quick_decimal_to_binary(255) == "11111111"

        # Hex to decimal
        assert quick_hex_to_decimal("FF") == 255
        assert quick_hex_to_decimal("A") == 10
        assert quick_hex_to_decimal("0") == 0

        # Decimal to hex
        assert quick_decimal_to_hex(255) == "FF"
        assert quick_decimal_to_hex(10) == "A"
        assert quick_decimal_to_hex(0) == "0"

    def test_batch_convert(self):
        """Test batch conversion utility."""
        numbers = ["10", "20", "30"]
        results = batch_convert(numbers, 10, 2)
        expected = ["1010", "10100", "11110"]
        assert results == expected

        # Test with invalid numbers (should include error messages)
        numbers_with_error = ["10", "invalid", "20"]
        results = batch_convert(numbers_with_error, 10, 2)
        assert results[0] == "1010"
        assert "Error" in results[1]
        assert results[2] == "10100"

        # Empty list
        assert batch_convert([], 10, 2) == []


class TestIntegration:
    """Integration tests combining multiple features."""

    def test_round_trip_conversions(self):
        """Test round-trip conversions maintain accuracy."""
        converter = BaseConverter()
        test_numbers = ["123", "1010", "777", "FF", "ZZZ"]
        test_bases = [10, 2, 8, 16, 36]

        for i, number in enumerate(test_numbers):
            source_base = test_bases[i]
            for target_base in [2, 8, 10, 16, 36]:
                if source_base != target_base:
                    # Convert to target base and back
                    converted = converter.convert_base(number, source_base, target_base)
                    back_converted = converter.convert_base(
                        converted, target_base, source_base
                    )

                    # Should match original (case-insensitive for hex)
                    assert back_converted.upper() == number.upper()

    def test_arithmetic_consistency(self):
        """Test that arithmetic operations are consistent across bases."""
        converter = BaseConverter()

        # Test the same arithmetic in different bases
        # 5 + 3 = 8 in decimal
        decimal_result = converter.binary_arithmetic(
            converter.decimal_to_base(5, 2), converter.decimal_to_base(3, 2), "+"
        )
        decimal_back = converter.base_to_decimal(decimal_result, 2)
        assert decimal_back == 8

    def test_formatting_combinations(self):
        """Test various formatting option combinations."""
        converter = BaseConverter()
        number = "11111111"

        # Test separator formatting
        formatted = converter.format_number_with_separators(number, 2, "_", 4)
        assert formatted == "1111_1111"

        # Verify the formatted number is still valid
        assert converter.is_valid_number(formatted.replace("_", ""), 2)

    def test_comprehensive_base_coverage(self):
        """Test conversion across all supported bases."""
        converter = BaseConverter()
        decimal_value = 1000

        # Convert decimal 1000 to all bases and back
        for base in range(2, 37):
            converted = converter.decimal_to_base(decimal_value, base)
            back_to_decimal = converter.base_to_decimal(converted, base)
            assert back_to_decimal == decimal_value
