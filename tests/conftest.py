"""
Pytest configuration and shared fixtures.
"""

import os
import sys

import pytest

# Add project root and src to Python path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def sample_numbers():
    """Fixture providing sample numbers for testing."""
    return {
        "binary": ["1010", "1111", "0", "10101010"],
        "octal": ["777", "123", "0", "1234"],
        "decimal": ["255", "123", "0", "1000"],
        "hexadecimal": ["FF", "ABC", "0", "DEADBEEF"],
        "base36": ["ZZ", "HELLO", "0", "WORLD"],
    }


@pytest.fixture
def conversion_test_cases():
    """Fixture providing test cases for conversion testing."""
    return [
        # (number, from_base, to_base, expected_result)
        ("1010", 2, 10, "10"),
        ("FF", 16, 10, "255"),
        ("777", 8, 10, "511"),
        ("255", 10, 2, "11111111"),
        ("255", 10, 8, "377"),
        ("255", 10, 16, "FF"),
        ("0", 10, 2, "0"),
        ("0", 2, 16, "0"),
        ("ABC", 16, 2, "101010111100"),
        ("ZZ", 36, 10, "1295"),
    ]


@pytest.fixture
def invalid_test_cases():
    """Fixture providing invalid input test cases."""
    return [
        # (number, base, expected_error_type)
        ("2", 2, "ValidationError"),  # Invalid digit for base
        ("G", 16, "ValidationError"),  # Invalid digit for base
        ("123", 1, "ValidationError"),  # Invalid base (too low)
        ("123", 37, "ValidationError"),  # Invalid base (too high)
        ("", 10, "ValidationError"),  # Empty input
        ("   ", 10, "ValidationError"),  # Whitespace only
    ]


@pytest.fixture
def arithmetic_test_cases():
    """Fixture providing arithmetic test cases."""
    return [
        # (num1, num2, operation, base, expected_result)
        ("1010", "1100", "+", 2, "10110"),  # Binary addition
        ("FF", "A", "+", 16, "109"),  # Hex addition
        ("100", "50", "-", 10, "50"),  # Decimal subtraction
        ("11", "10", "*", 2, "110"),  # Binary multiplication
        ("100", "10", "/", 10, "10"),  # Decimal division
        ("1101", "11", "%", 2, "1"),  # Binary modulo
        ("10", "11", "**", 2, "1000"),  # Binary power
    ]


@pytest.fixture
def formatting_test_cases():
    """Fixture providing formatting test cases."""
    return [
        # (number, base, add_prefix, add_separators, expected_contains)
        ("FF", 16, True, False, "0x"),
        ("1010", 2, True, False, "0b"),
        ("777", 8, True, False, "0o"),
        ("11111111", 2, False, True, "_"),
        ("-FF", 16, True, False, "-0x"),
        ("1010", 2, True, True, ["0b", "_"]),  # Should contain both
    ]


class TestDataProvider:
    """Class to provide common test data and utilities."""

    @staticmethod
    def get_all_bases():
        """Return list of all supported bases."""
        return list(range(2, 37))

    @staticmethod
    def get_common_bases():
        """Return list of commonly used bases."""
        return [2, 8, 10, 16, 36]

    @staticmethod
    def get_test_numbers_for_base(base):
        """Get appropriate test numbers for a given base."""
        if base == 2:
            return ["0", "1", "10", "1010", "1111"]
        elif base == 8:
            return ["0", "7", "77", "123", "777"]
        elif base == 10:
            return ["0", "9", "99", "123", "999"]
        elif base == 16:
            return ["0", "F", "FF", "ABC", "FFF"]
        elif base == 36:
            return ["0", "Z", "ZZ", "ABC", "ZZZ"]
        else:
            # Generate appropriate test numbers for other bases
            digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base]
            return [
                "0",
                digits[-1],  # Max single digit
                digits[-1] + digits[-1],  # Max double digit
                digits[1] + digits[2] + digits[3] if len(digits) > 3 else digits[1],
            ]


@pytest.fixture
def test_data_provider():
    """Fixture providing the TestDataProvider class."""
    return TestDataProvider


# Custom pytest markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "cli: marks tests as CLI-specific")
    config.addinivalue_line("markers", "gui: marks tests as GUI-specific")
    config.addinivalue_line("markers", "validation: marks tests as validation-specific")
    config.addinivalue_line("markers", "converter: marks tests as converter-specific")
