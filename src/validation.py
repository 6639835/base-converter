"""
Input validation and error handling utilities for the Base Converter.
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union, cast


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class InputValidator:
    """Handles input validation for base conversion operations."""

    def __init__(self):
        """Initialize the validator with patterns and limits."""
        self.max_input_length = 1000  # Prevent extremely long inputs
        self.min_base = 2
        self.max_base = 36

        # Regex patterns for different input formats
        self.patterns = {
            "binary_prefix": re.compile(r"^-?0[bB][01]+$"),
            "octal_prefix": re.compile(r"^-?0[oO][0-7]+$"),
            "hex_prefix": re.compile(r"^-?0[xX][0-9a-fA-F]+$"),
            "decimal": re.compile(r"^-?[0-9]+$"),
            "basic_number": re.compile(r"^-?[0-9a-zA-Z]+$"),
        }

    def validate_base(self, base: Union[str, int]) -> int:
        """
        Validate and convert base to integer.

        Args:
            base: Base value to validate (string or integer)

        Returns:
            int: Validated base

        Raises:
            ValidationError: If base is invalid
        """
        try:
            base_int = int(base)
        except (ValueError, TypeError):
            raise ValidationError(f"Base must be a valid integer, got '{base}'")

        if base_int < self.min_base or base_int > self.max_base:
            raise ValidationError(
                f"Base must be between {self.min_base} and {self.max_base}, got {base_int}"
            )

        return base_int

    def validate_number_string(self, number: str) -> str:
        """
        Validate and clean number string input.

        Args:
            number: Number string to validate

        Returns:
            str: Cleaned number string

        Raises:
            ValidationError: If number string is invalid
        """
        if not isinstance(number, str):
            raise ValidationError(
                f"Number must be a string, got {type(number).__name__}"
            )

        if not number or not number.strip():
            raise ValidationError("Number cannot be empty")

        cleaned = number.strip()

        if len(cleaned) > self.max_input_length:
            raise ValidationError(
                f"Number too long (max {self.max_input_length} characters)"
            )

        # Check for basic number format
        if not self.patterns["basic_number"].match(cleaned):
            raise ValidationError(f"Invalid number format: '{number}'")

        return cleaned

    def validate_number_for_base(self, number: str, base: int) -> Tuple[str, bool]:
        """
        Validate that a number string is valid for the given base.

        Args:
            number: Number string to validate
            base: Base to validate against

        Returns:
            Tuple[str, bool]: (cleaned_number, has_prefix)

        Raises:
            ValidationError: If number is not valid for the base
        """
        cleaned_number = self.validate_number_string(number)
        base = self.validate_base(base)

        # Handle negative numbers
        is_negative = cleaned_number.startswith("-")
        if is_negative:
            cleaned_number = cleaned_number[1:]

        # Check for and handle prefixes
        has_prefix = False
        original_cleaned = cleaned_number

        if cleaned_number.upper().startswith(("0B", "0O", "0X")):
            prefix = cleaned_number[:2].upper()
            cleaned_number = cleaned_number[2:]
            has_prefix = True

            # Validate prefix matches expected base
            expected_bases = {"0B": 2, "0O": 8, "0X": 16}
            expected_base = expected_bases.get(prefix)
            if expected_base and expected_base != base:
                raise ValidationError(
                    f"Prefix '{prefix}' indicates base {expected_base}, but base {base} specified"
                )

        if not cleaned_number:
            raise ValidationError("Number cannot be empty after removing prefix")

        # Validate each digit is valid for the base
        valid_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base]
        for i, digit in enumerate(cleaned_number.upper()):
            if digit not in valid_digits:
                raise ValidationError(
                    f"Invalid digit '{digit}' for base {base} at position {i}"
                )

        # Return the original cleaned number (with prefix if present)
        result = original_cleaned
        if is_negative:
            result = "-" + result

        return result, has_prefix

    def validate_operation(self, operation: str) -> str:
        """
        Validate arithmetic operation.

        Args:
            operation: Operation string to validate

        Returns:
            str: Validated operation

        Raises:
            ValidationError: If operation is invalid
        """
        valid_operations = ["+", "-", "*", "/", "%", "**"]

        if operation not in valid_operations:
            raise ValidationError(
                f"Invalid operation '{operation}'. Valid operations: {', '.join(valid_operations)}"
            )

        return operation

    def sanitize_input(self, text: str) -> str:
        """
        Sanitize input text by removing potentially harmful characters.

        Args:
            text: Text to sanitize

        Returns:
            str: Sanitized text
        """
        if not isinstance(text, str):
            return str(text)

        # Remove control characters and excessive whitespace
        sanitized = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)
        sanitized = re.sub(r"\s+", " ", sanitized).strip()

        # For number inputs, keep only valid number characters
        # This includes digits, letters (for higher bases), minus sign, and common prefixes
        sanitized = re.sub(r"[^-+0-9A-Za-z\s]", "", sanitized)
        sanitized = sanitized.strip()

        return sanitized

    def validate_batch_input(self, numbers: List[str], base: int) -> List[str]:
        """
        Validate a batch of number strings for a given base.

        Args:
            numbers: List of number strings
            base: Base to validate against

        Returns:
            List[str]: List of validated numbers

        Raises:
            ValidationError: If any number is invalid
        """
        if not isinstance(numbers, list):
            raise ValidationError("Numbers must be provided as a list")

        if len(numbers) > 100:  # Reasonable limit for batch processing
            raise ValidationError("Too many numbers in batch (max 100)")

        validated_numbers = []
        errors = []

        for i, number in enumerate(numbers):
            try:
                validated, _ = self.validate_number_for_base(number, base)
                validated_numbers.append(validated)
            except ValidationError as e:
                errors.append(f"Number {i+1}: {str(e)}")

        if errors:
            raise ValidationError("Validation errors:\n" + "\n".join(errors))

        return validated_numbers

    def suggest_base(self, number: str) -> Optional[int]:
        """
        Suggest the most likely base for a number based on its format and digits.

        Args:
            number: Number string to analyze

        Returns:
            Optional[int]: Suggested base or None if cannot determine
        """
        try:
            cleaned = self.validate_number_string(number)
        except ValidationError:
            return None

        # Check for explicit prefixes
        cleaned_upper = cleaned.upper()
        if cleaned_upper.startswith(("0B", "-0B")):
            return 2
        elif cleaned_upper.startswith(("0O", "-0O")):
            return 8
        elif cleaned_upper.startswith(("0X", "-0X")):
            return 16

        # Analyze digits to suggest base
        number_part = cleaned.lstrip("-").upper()
        unique_digits = set(number_part)

        # Find minimum base that can represent all digits
        max_digit_value = 0
        digit_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for digit in unique_digits:
            if digit in digit_chars:
                max_digit_value = max(max_digit_value, digit_chars.index(digit))

        suggested_base = max_digit_value + 1

        # Common base suggestions with heuristics
        if suggested_base <= 2 and unique_digits.issubset(set("01")):
            return 2  # Pure binary
        elif suggested_base <= 8 and unique_digits.issubset(set("01234567")):
            # If it uses many octal digits or has leading zero pattern, suggest octal
            if len(unique_digits) >= 4 or (
                number_part.startswith("0") and len(number_part) > 1
            ):
                return 8
            # For simple cases like "123", prefer decimal
            else:
                return 10
        elif suggested_base <= 10:
            return 10  # Default to decimal for most cases
        elif suggested_base <= 16:
            return 16
        else:
            # For bases above 16, consider common cases
            # Single letters should default to hex if they're close to hex range
            if len(unique_digits) == 1 and suggested_base <= 20:
                return 16  # Single letters like G, H, I etc. suggest hex context
            # Otherwise return the calculated base but cap at reasonable limits
            return min(suggested_base, 36)

    def format_error_message(self, error: Exception, context: str = "") -> str:
        """
        Format error messages in a user-friendly way.

        Args:
            error: Exception to format
            context: Additional context for the error

        Returns:
            str: Formatted error message
        """
        error_type = type(error).__name__
        error_msg = str(error)

        if context:
            return f"{error_type} in {context}: {error_msg}"
        else:
            return f"{error_type}: {error_msg}"

    def get_validation_summary(self, number: str, base: int) -> Dict[str, Any]:
        """
        Get a summary of validation information for a number and base.

        Args:
            number: Number string
            base: Base to validate for

        Returns:
            dict: Validation summary
        """
        summary: Dict[str, Any] = {
            "original_input": number,
            "is_valid": False,
            "cleaned_number": "",
            "has_prefix": False,
            "is_negative": False,
            "suggested_base": None,
            "errors": [],
        }

        try:
            # Basic validation
            cleaned = self.validate_number_string(number)
            summary["cleaned_number"] = cleaned
            summary["is_negative"] = cleaned.startswith("-")

            # Base-specific validation
            validated_number, has_prefix = self.validate_number_for_base(number, base)
            summary["has_prefix"] = has_prefix
            summary["is_valid"] = True

        except ValidationError as e:
            cast(List[str], summary["errors"]).append(str(e))

        # Get base suggestion regardless of validation result
        try:
            summary["suggested_base"] = self.suggest_base(number)
        except:
            pass

        return summary


# Utility functions for quick validation
def is_valid_base(base: Union[str, int]) -> bool:
    """Quick check if a base value is valid."""
    try:
        validator = InputValidator()
        validator.validate_base(base)
        return True
    except ValidationError:
        return False


def is_valid_number_for_base(number: str, base: int) -> bool:
    """Quick check if a number is valid for a given base."""
    try:
        validator = InputValidator()
        validator.validate_number_for_base(number, base)
        return True
    except ValidationError:
        return False


def clean_number_input(number: str) -> str:
    """Clean and sanitize a number input string."""
    validator = InputValidator()
    try:
        return validator.validate_number_string(number)
    except ValidationError:
        return validator.sanitize_input(number)
