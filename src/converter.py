"""
Core base conversion functions for the Base Converter utility.
Supports conversion between various number bases including binary, octal, decimal, hexadecimal, and custom bases.
"""

import math
import re
from typing import Dict, List, Optional, Union


class BaseConverter:
    """A comprehensive base converter with support for multiple number systems."""

    # Standard digit characters for bases up to 36
    DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        """Initialize the BaseConverter with supported bases and their names."""
        self.base_names = {
            2: "Binary",
            8: "Octal",
            10: "Decimal",
            16: "Hexadecimal",
            3: "Ternary",
            4: "Quaternary",
            5: "Quinary",
            6: "Senary",
            7: "Septenary",
            9: "Nonary",
            11: "Undecimal",
            12: "Duodecimal",
            13: "Tridecimal",
            14: "Tetradecimal",
            15: "Pentadecimal",
            17: "Heptadecimal",
            18: "Octodecimal",
            19: "Enneadecimal",
            20: "Vigesimal",
            36: "Base36",
        }

    def is_valid_number(self, number: str, base: int) -> bool:
        """
        Validate if a number string is valid for the given base.

        Args:
            number (str): The number string to validate
            base (int): The base to validate against (2-36)

        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(number, str) or not number.strip():
            return False

        if base < 2 or base > 36:
            return False

        # Remove optional prefix and handle negative numbers
        clean_number = number.strip().upper()
        if clean_number.startswith("-"):
            clean_number = clean_number[1:]
        if clean_number.startswith(("0X", "0B", "0O")):
            clean_number = clean_number[2:]

        if not clean_number:
            return False

        valid_digits = self.DIGITS[:base]
        return all(digit in valid_digits for digit in clean_number)

    def decimal_to_base(self, decimal_number: int, target_base: int) -> str:
        """
        Convert a decimal number to any base (2-36).

        Args:
            decimal_number (int): The decimal number to convert
            target_base (int): The target base (2-36)

        Returns:
            str: The number in the target base

        Raises:
            ValueError: If target_base is not between 2 and 36
        """
        if target_base < 2 or target_base > 36:
            raise ValueError(f"Base must be between 2 and 36, got {target_base}")

        if decimal_number == 0:
            return "0"

        is_negative = decimal_number < 0
        decimal_number = abs(decimal_number)

        result = ""
        while decimal_number > 0:
            remainder = decimal_number % target_base
            result = self.DIGITS[remainder] + result
            decimal_number //= target_base

        return ("-" + result) if is_negative else result

    def base_to_decimal(self, number: str, source_base: int) -> int:
        """
        Convert a number from any base (2-36) to decimal.

        Args:
            number (str): The number string to convert
            source_base (int): The source base (2-36)

        Returns:
            int: The decimal representation

        Raises:
            ValueError: If the number is invalid for the source base
        """
        if not self.is_valid_number(number, source_base):
            raise ValueError(f"Invalid number '{number}' for base {source_base}")

        clean_number = number.strip().upper()
        is_negative = clean_number.startswith("-")
        if is_negative:
            clean_number = clean_number[1:]

        # Handle common prefixes
        if clean_number.startswith(("0X", "0B", "0O")):
            clean_number = clean_number[2:]

        decimal_value = 0
        power = 0

        for digit in reversed(clean_number):
            digit_value = self.DIGITS.index(digit)
            decimal_value += digit_value * (source_base**power)
            power += 1

        return -decimal_value if is_negative else decimal_value

    def convert_base(self, number: str, source_base: int, target_base: int) -> str:
        """
        Convert a number from one base to another.

        Args:
            number (str): The number string to convert
            source_base (int): The source base (2-36)
            target_base (int): The target base (2-36)

        Returns:
            str: The converted number in target base
        """
        decimal_value = self.base_to_decimal(number, source_base)
        return self.decimal_to_base(decimal_value, target_base)

    def to_binary(self, number: str, source_base: int = 10) -> str:
        """Convert number to binary (base 2)."""
        return self.convert_base(number, source_base, 2)

    def to_octal(self, number: str, source_base: int = 10) -> str:
        """Convert number to octal (base 8)."""
        return self.convert_base(number, source_base, 8)

    def to_decimal(self, number: str, source_base: int) -> str:
        """Convert number to decimal (base 10)."""
        return str(self.convert_base(number, source_base, 10))

    def to_hexadecimal(self, number: str, source_base: int = 10) -> str:
        """Convert number to hexadecimal (base 16)."""
        return self.convert_base(number, source_base, 16)

    def binary_arithmetic(self, num1: str, num2: str, operation: str) -> str:
        """
        Perform arithmetic operations on binary numbers.

        Args:
            num1 (str): First binary number
            num2 (str): Second binary number
            operation (str): Operation (+, -, *, /, %, **)

        Returns:
            str: Result in binary
        """
        dec1 = self.base_to_decimal(num1, 2)
        dec2 = self.base_to_decimal(num2, 2)

        if operation == "+":
            result = dec1 + dec2
        elif operation == "-":
            result = dec1 - dec2
        elif operation == "*":
            result = dec1 * dec2
        elif operation == "/":
            if dec2 == 0:
                raise ValueError("Division by zero")
            result = dec1 // dec2  # Integer division
        elif operation == "%":
            if dec2 == 0:
                raise ValueError("Division by zero")
            result = dec1 % dec2
        elif operation == "**":
            result = dec1**dec2
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        return self.decimal_to_base(result, 2)

    def get_conversion_table(self, number: str, source_base: int) -> Dict[int, str]:
        """
        Get a conversion table showing the number in multiple common bases.

        Args:
            number (str): The number to convert
            source_base (int): The source base of the number

        Returns:
            Dict[int, str]: Dictionary mapping base to converted value
        """
        common_bases = [2, 8, 10, 16]
        decimal_val = self.base_to_decimal(number, source_base)

        conversion_table = {}
        for base in common_bases:
            conversion_table[base] = self.decimal_to_base(decimal_val, base)

        return conversion_table

    def format_number_with_separators(
        self, number: str, base: int, separator: str = "_", group_size: int = 4
    ) -> str:
        """
        Format a number with digit separators for better readability.

        Args:
            number (str): The number to format
            base (int): The base of the number
            separator (str): The separator character (default: "_")
            group_size (int): Size of digit groups (default: 4)

        Returns:
            str: Formatted number with separators
        """
        if not self.is_valid_number(number, base):
            return number

        clean_number = number.strip().upper()
        is_negative = clean_number.startswith("-")
        if is_negative:
            clean_number = clean_number[1:]

        # Group digits from right to left
        grouped = ""
        for i, digit in enumerate(reversed(clean_number)):
            if i > 0 and i % group_size == 0:
                grouped = separator + grouped
            grouped = digit + grouped

        return ("-" + grouped) if is_negative else grouped

    def get_base_info(self, base: int) -> Dict[str, Union[str, int, List[str]]]:
        """
        Get information about a specific base.

        Args:
            base (int): The base to get information about

        Returns:
            Dict: Information about the base including name, digits, etc.
        """
        if base < 2 or base > 36:
            raise ValueError(f"Base must be between 2 and 36, got {base}")

        return {
            "base": base,
            "name": self.base_names.get(base, f"Base-{base}"),
            "digits": list(self.DIGITS[:base]),
            "digit_count": base,
            "max_digit": self.DIGITS[base - 1],
            "common_prefixes": self._get_common_prefixes(base),
        }

    def _get_common_prefixes(self, base: int) -> List[str]:
        """Get common prefixes for a base."""
        prefix_map = {2: ["0b", "0B"], 8: ["0o", "0O"], 16: ["0x", "0X"]}
        return prefix_map.get(base, [])

    def detect_base(self, number: str) -> Optional[int]:
        """
        Attempt to detect the base of a number from common prefixes.

        Args:
            number (str): The number string to analyze

        Returns:
            Optional[int]: Detected base or None if cannot determine
        """
        clean_number = number.strip().lower()

        if clean_number.startswith("0b"):
            return 2
        elif clean_number.startswith("0o"):
            return 8
        elif clean_number.startswith("0x"):
            return 16
        elif clean_number.startswith("-0b"):
            return 2
        elif clean_number.startswith("-0o"):
            return 8
        elif clean_number.startswith("-0x"):
            return 16

        # Try to infer from digits used
        clean_number = clean_number.lstrip("-")
        unique_digits = set(clean_number.upper())

        # For ambiguous cases, use specific heuristics
        if unique_digits.issubset(set("01")):
            return 2  # Pure binary
        elif unique_digits.issubset(set("01234567")):
            # If it uses all octal digits (0-7) or has leading zero pattern, suggest octal
            if (
                len(unique_digits) >= 4
                or clean_number.startswith("0")
                and len(clean_number) > 1
            ):
                return 8
            # For simple cases like "123", prefer decimal
            else:
                return 10
        elif unique_digits.issubset(set("0123456789")):
            return 10  # Decimal
        elif unique_digits.issubset(set("0123456789ABCDEF")):
            return 16  # Hexadecimal

        return None

    def validate_conversion(
        self, original: str, converted: str, source_base: int, target_base: int
    ) -> bool:
        """
        Validate a conversion by converting back and comparing.

        Args:
            original (str): Original number
            converted (str): Converted number
            source_base (int): Source base
            target_base (int): Target base

        Returns:
            bool: True if conversion is valid
        """
        try:
            back_converted = self.convert_base(converted, target_base, source_base)
            return original.upper().strip() == back_converted.upper().strip()
        except:
            return False


# Utility functions for common conversions
def quick_binary_to_decimal(binary: str) -> int:
    """Quick conversion from binary string to decimal integer."""
    converter = BaseConverter()
    return converter.base_to_decimal(binary, 2)


def quick_decimal_to_binary(decimal: int) -> str:
    """Quick conversion from decimal integer to binary string."""
    converter = BaseConverter()
    return converter.decimal_to_base(decimal, 2)


def quick_hex_to_decimal(hex_str: str) -> int:
    """Quick conversion from hexadecimal string to decimal integer."""
    converter = BaseConverter()
    return converter.base_to_decimal(hex_str, 16)


def quick_decimal_to_hex(decimal: int) -> str:
    """Quick conversion from decimal integer to hexadecimal string."""
    converter = BaseConverter()
    return converter.decimal_to_base(decimal, 16)


def batch_convert(numbers: List[str], source_base: int, target_base: int) -> List[str]:
    """
    Convert multiple numbers from one base to another.

    Args:
        numbers (List[str]): List of numbers to convert
        source_base (int): Source base
        target_base (int): Target base

    Returns:
        List[str]: List of converted numbers
    """
    converter = BaseConverter()
    results = []

    for number in numbers:
        try:
            converted = converter.convert_base(number, source_base, target_base)
            results.append(converted)
        except Exception as e:
            results.append(f"Error: {str(e)}")

    return results
