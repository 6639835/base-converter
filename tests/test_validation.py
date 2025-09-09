"""
Tests for input validation functionality.
"""

import os
import sys

# Add project root and src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest

from src.validation import (
    InputValidator,
    ValidationError,
    clean_number_input,
    is_valid_base,
    is_valid_number_for_base,
)


class TestInputValidator:
    """Test cases for InputValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = InputValidator()

    def test_initialization(self):
        """Test InputValidator initialization."""
        assert self.validator.max_input_length == 1000
        assert self.validator.min_base == 2
        assert self.validator.max_base == 36
        assert "binary_prefix" in self.validator.patterns
        assert "hex_prefix" in self.validator.patterns

    def test_validate_base(self):
        """Test base validation."""
        # Valid bases
        assert self.validator.validate_base(2) == 2
        assert self.validator.validate_base("10") == 10
        assert self.validator.validate_base(36) == 36
        assert self.validator.validate_base("16") == 16

        # Invalid bases
        with pytest.raises(ValidationError, match="Base must be a valid integer"):
            self.validator.validate_base("invalid")

        with pytest.raises(ValidationError, match="Base must be a valid integer"):
            self.validator.validate_base(None)

        with pytest.raises(ValidationError, match="Base must be between 2 and 36"):
            self.validator.validate_base(1)

        with pytest.raises(ValidationError, match="Base must be between 2 and 36"):
            self.validator.validate_base(37)

        with pytest.raises(ValidationError, match="Base must be between 2 and 36"):
            self.validator.validate_base(-5)

    def test_validate_number_string(self):
        """Test number string validation."""
        # Valid number strings
        assert self.validator.validate_number_string("123") == "123"
        assert self.validator.validate_number_string("  ABC  ") == "ABC"
        assert self.validator.validate_number_string("-123") == "-123"
        assert self.validator.validate_number_string("0xFF") == "0xFF"

        # Invalid number strings
        with pytest.raises(ValidationError, match="Number must be a string"):
            self.validator.validate_number_string(123)

        with pytest.raises(ValidationError, match="Number cannot be empty"):
            self.validator.validate_number_string("")

        with pytest.raises(ValidationError, match="Number cannot be empty"):
            self.validator.validate_number_string("   ")

        with pytest.raises(ValidationError, match="Number too long"):
            self.validator.validate_number_string("1" * 1001)

        with pytest.raises(ValidationError, match="Invalid number format"):
            self.validator.validate_number_string("12@34")

    def test_validate_number_for_base(self):
        """Test number validation for specific bases."""
        # Valid combinations
        result, has_prefix = self.validator.validate_number_for_base("1010", 2)
        assert result == "1010"
        assert has_prefix == False

        result, has_prefix = self.validator.validate_number_for_base("0b1010", 2)
        assert result == "0b1010"
        assert has_prefix == True

        result, has_prefix = self.validator.validate_number_for_base("777", 8)
        assert result == "777"
        assert has_prefix == False

        result, has_prefix = self.validator.validate_number_for_base("0o777", 8)
        assert result == "0o777"
        assert has_prefix == True

        result, has_prefix = self.validator.validate_number_for_base("FF", 16)
        assert result == "FF"
        assert has_prefix == False

        result, has_prefix = self.validator.validate_number_for_base("0xFF", 16)
        assert result == "0xFF"
        assert has_prefix == True

        # Negative numbers
        result, has_prefix = self.validator.validate_number_for_base("-123", 10)
        assert result == "-123"
        assert has_prefix == False

        result, has_prefix = self.validator.validate_number_for_base("-0xFF", 16)
        assert result == "-0xFF"
        assert has_prefix == True

        # Invalid digit for base
        with pytest.raises(ValidationError, match="Invalid digit '2' for base 2"):
            self.validator.validate_number_for_base("1210", 2)

        with pytest.raises(ValidationError, match="Invalid digit '8' for base 8"):
            self.validator.validate_number_for_base("778", 8)

        with pytest.raises(ValidationError, match="Invalid digit 'G' for base 16"):
            self.validator.validate_number_for_base("FFG", 16)

        # Prefix mismatch
        with pytest.raises(
            ValidationError, match="Prefix '0B' indicates base 2, but base 10 specified"
        ):
            self.validator.validate_number_for_base("0b1010", 10)

        with pytest.raises(
            ValidationError,
            match="Prefix '0X' indicates base 16, but base 10 specified",
        ):
            self.validator.validate_number_for_base("0xFF", 10)

        # Empty after prefix removal
        with pytest.raises(
            ValidationError, match="Number cannot be empty after removing prefix"
        ):
            self.validator.validate_number_for_base("0x", 16)

    def test_validate_operation(self):
        """Test arithmetic operation validation."""
        # Valid operations
        assert self.validator.validate_operation("+") == "+"
        assert self.validator.validate_operation("-") == "-"
        assert self.validator.validate_operation("*") == "*"
        assert self.validator.validate_operation("/") == "/"
        assert self.validator.validate_operation("%") == "%"
        assert self.validator.validate_operation("**") == "**"

        # Invalid operations
        with pytest.raises(ValidationError, match="Invalid operation"):
            self.validator.validate_operation("^")

        with pytest.raises(ValidationError, match="Invalid operation"):
            self.validator.validate_operation("&")

        with pytest.raises(ValidationError, match="Invalid operation"):
            self.validator.validate_operation("invalid")

    def test_sanitize_input(self):
        """Test input sanitization."""
        # Normal text
        assert self.validator.sanitize_input("123") == "123"

        # Multiple spaces
        assert self.validator.sanitize_input("  123   456  ") == "123 456"

        # Control characters
        assert self.validator.sanitize_input("123\x00\x1f") == "123"

        # Non-string input
        assert self.validator.sanitize_input(123) == "123"

        # Mixed whitespace and control chars
        assert self.validator.sanitize_input("  \t123\n\r456\x08  ") == "123 456"

    def test_validate_batch_input(self):
        """Test batch input validation."""
        # Valid batch
        numbers = ["123", "456", "789"]
        result = self.validator.validate_batch_input(numbers, 10)
        assert result == numbers

        # Valid batch with various formats
        numbers = ["123", "-456", "0xFF"]
        result = self.validator.validate_batch_input(numbers, 16)
        assert len(result) == 3

        # Invalid input type
        with pytest.raises(ValidationError, match="Numbers must be provided as a list"):
            self.validator.validate_batch_input("not a list", 10)

        # Too many numbers
        large_batch = ["123"] * 101
        with pytest.raises(ValidationError, match="Too many numbers in batch"):
            self.validator.validate_batch_input(large_batch, 10)

        # Some invalid numbers
        numbers = ["123", "invalid", "456", "2"]  # "2" is invalid for base 2
        with pytest.raises(ValidationError, match="Validation errors"):
            self.validator.validate_batch_input(numbers, 2)

    def test_suggest_base(self):
        """Test base suggestion functionality."""
        # Explicit prefixes
        assert self.validator.suggest_base("0b1010") == 2
        assert self.validator.suggest_base("0B1010") == 2
        assert self.validator.suggest_base("0o777") == 8
        assert self.validator.suggest_base("0O777") == 8
        assert self.validator.suggest_base("0xFF") == 16
        assert self.validator.suggest_base("0XFF") == 16

        # Negative numbers with prefixes
        assert self.validator.suggest_base("-0b1010") == 2
        assert self.validator.suggest_base("-0xFF") == 16

        # Digit-based suggestions
        assert self.validator.suggest_base("01") == 2
        assert self.validator.suggest_base("01234567") == 8
        assert self.validator.suggest_base("0123456789") == 10
        assert self.validator.suggest_base("0123456789ABCDEF") == 16

        # Ambiguous cases
        assert self.validator.suggest_base("123") == 10
        assert self.validator.suggest_base("ABC") == 16

        # Mixed case
        assert self.validator.suggest_base("abc") == 16
        assert self.validator.suggest_base("AbC") == 16

        # Invalid input
        assert self.validator.suggest_base("") is None
        assert self.validator.suggest_base("@#$") is None

        # Large base requirements
        assert self.validator.suggest_base("XYZ") == 36

    def test_format_error_message(self):
        """Test error message formatting."""
        error = ValueError("Test error")

        # Without context
        message = self.validator.format_error_message(error)
        assert "ValueError: Test error" in message

        # With context
        message = self.validator.format_error_message(error, "validation")
        assert "ValueError in validation: Test error" in message

        # Different error types
        error = TypeError("Type error")
        message = self.validator.format_error_message(error, "conversion")
        assert "TypeError in conversion: Type error" in message

    def test_get_validation_summary(self):
        """Test validation summary generation."""
        # Valid input
        summary = self.validator.get_validation_summary("123", 10)
        assert summary["original_input"] == "123"
        assert summary["is_valid"] == True
        assert summary["cleaned_number"] == "123"
        assert summary["has_prefix"] == False
        assert summary["is_negative"] == False
        assert summary["suggested_base"] == 10
        assert len(summary["errors"]) == 0

        # Input with prefix
        summary = self.validator.get_validation_summary("0xFF", 16)
        assert summary["is_valid"] == True
        assert summary["has_prefix"] == True
        assert summary["suggested_base"] == 16

        # Negative number
        summary = self.validator.get_validation_summary("-123", 10)
        assert summary["is_valid"] == True
        assert summary["is_negative"] == True

        # Invalid input
        summary = self.validator.get_validation_summary("G", 10)
        assert summary["is_valid"] == False
        assert len(summary["errors"]) > 0
        assert summary["suggested_base"] == 16  # G suggests hex

        # Empty input
        summary = self.validator.get_validation_summary("", 10)
        assert summary["is_valid"] == False
        assert len(summary["errors"]) > 0

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Maximum length input (at limit)
        long_input = "1" * 1000
        result = self.validator.validate_number_string(long_input)
        assert result == long_input

        # Whitespace handling
        result, _ = self.validator.validate_number_for_base("  123  ", 10)
        assert result == "123"

        # Case insensitive handling
        result, _ = self.validator.validate_number_for_base("abc", 16)
        assert result == "abc"

        result, _ = self.validator.validate_number_for_base("ABC", 16)
        assert result == "ABC"

        # All valid digits for base 36
        all_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result, _ = self.validator.validate_number_for_base(all_digits, 36)
        assert result == all_digits

        # Boundary bases
        result, _ = self.validator.validate_number_for_base("01", 2)
        assert result == "01"

        result, _ = self.validator.validate_number_for_base(all_digits, 36)
        assert result == all_digits


class TestUtilityFunctions:
    """Test utility functions."""

    def test_is_valid_base(self):
        """Test is_valid_base utility function."""
        assert is_valid_base(2) == True
        assert is_valid_base("10") == True
        assert is_valid_base(36) == True

        assert is_valid_base(1) == False
        assert is_valid_base(37) == False
        assert is_valid_base("invalid") == False
        assert is_valid_base(None) == False

    def test_is_valid_number_for_base(self):
        """Test is_valid_number_for_base utility function."""
        assert is_valid_number_for_base("123", 10) == True
        assert is_valid_number_for_base("1010", 2) == True
        assert is_valid_number_for_base("FF", 16) == True

        assert is_valid_number_for_base("123", 2) == False
        assert is_valid_number_for_base("G", 16) == False
        assert is_valid_number_for_base("", 10) == False

    def test_clean_number_input(self):
        """Test clean_number_input utility function."""
        assert clean_number_input("123") == "123"
        assert clean_number_input("  123  ") == "123"
        assert clean_number_input("ABC") == "ABC"

        # Invalid input should return sanitized version
        result = clean_number_input("123@#$")
        assert "@#$" not in result  # Should be sanitized


class TestValidationIntegration:
    """Integration tests for validation with other components."""

    def test_validation_with_conversion(self):
        """Test validation integration with conversion logic."""
        validator = InputValidator()

        # Test that validated numbers work with conversion
        test_cases = [("1010", 2), ("777", 8), ("123", 10), ("FF", 16), ("ZZ", 36)]

        for number, base in test_cases:
            # Validation should pass
            validated, _ = validator.validate_number_for_base(number, base)
            assert validated is not None

            # Should work with actual converter
            from src.converter import BaseConverter

            converter = BaseConverter()
            decimal_value = converter.base_to_decimal(validated, base)
            assert isinstance(decimal_value, int)

    def test_error_handling_consistency(self):
        """Test that error handling is consistent across validation."""
        validator = InputValidator()

        # All these should raise ValidationError (not other exceptions)
        invalid_inputs = [
            ("", 10),  # Empty
            ("123", 1),  # Invalid base
            ("G", 10),  # Invalid digit
            ("0xFF", 10),  # Wrong prefix for base
        ]

        for number, base in invalid_inputs:
            with pytest.raises(ValidationError):
                validator.validate_number_for_base(number, base)

    def test_batch_validation_consistency(self):
        """Test batch validation produces consistent results."""
        validator = InputValidator()

        numbers = ["123", "456", "789"]

        # Individual validation
        individual_results = []
        for number in numbers:
            try:
                result, _ = validator.validate_number_for_base(number, 10)
                individual_results.append(result)
            except ValidationError:
                individual_results.append(None)

        # Batch validation
        batch_results = validator.validate_batch_input(numbers, 10)

        # Should be consistent
        assert batch_results == individual_results

    def test_suggestion_accuracy(self):
        """Test that base suggestions are accurate and useful."""
        validator = InputValidator()

        # Test cases where suggestion should be accurate
        test_cases = [
            ("0b1010", 2),  # Explicit binary prefix
            ("0xFF", 16),  # Explicit hex prefix
            ("01234567", 8),  # Only octal digits
            ("789ABC", 16),  # Contains hex letters
        ]

        for number, expected_base in test_cases:
            suggested = validator.suggest_base(number)
            assert suggested == expected_base

            # Suggestion should be valid for the number
            try:
                validator.validate_number_for_base(number, suggested)
            except ValidationError:
                pytest.fail(
                    f"Suggested base {suggested} is not valid for number {number}"
                )

    def test_comprehensive_validation_flow(self):
        """Test complete validation workflow."""
        validator = InputValidator()

        # Simulate complete validation flow for various inputs
        test_inputs = [
            ("123", 10, True),  # Valid decimal
            ("0xFF", 16, True),  # Valid hex with prefix
            ("-1010", 2, True),  # Valid negative binary
            ("G", 10, False),  # Invalid digit
            ("", 10, False),  # Empty input
            ("123", 1, False),  # Invalid base
        ]

        for number, base, should_be_valid in test_inputs:
            summary = validator.get_validation_summary(number, base)

            assert summary["is_valid"] == should_be_valid

            if should_be_valid:
                assert len(summary["errors"]) == 0
                assert summary["cleaned_number"] != ""
            else:
                assert len(summary["errors"]) > 0
