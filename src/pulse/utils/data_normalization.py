"""
Utility functions for normalizing data from CSV files
"""

import re


def parse_currency_to_float(value: str) -> int:
    """
    Parse currency strings like '$1B', '$2.5M', '$3T' to integer values in USD.

    Returns the value in actual USD (not millions/billions) rounded to whole dollars.
    Examples:
        '$1B' -> 1000000000
        '$2.5M' -> 2500000
        '$3T' -> 3000000000000
        'N/A' -> 0
        '$2K' -> 2000

    Args:
        value: String value to parse

    Returns:
        Integer value in USD (0 if unparseable)
    """
    if not value or value.upper() in ["N/A", "NA", "", "NULL"]:
        return 0

    # Remove currency symbols and spaces, but keep the value part before any parentheses
    clean_value = re.sub(r"[\$,\s]", "", value.upper())
    # Remove anything in parentheses (like "(Salesforce)", "(Adobe)")
    clean_value = re.sub(r"\([^)]*\)", "", clean_value)

    # Extract number and suffix
    match = re.match(r"^(\d+\.?\d*)([KMBTQ]?)$", clean_value)
    if not match:
        # Try to parse as plain number
        try:
            return round(float(re.sub(r"[^\d.]", "", value)))
        except (ValueError, TypeError):
            return 0

    number_str, suffix = match.groups()
    try:
        number = float(number_str)
    except (ValueError, TypeError):
        return 0

    # Apply multiplier based on suffix
    multipliers = {
        "K": 1_000,
        "M": 1_000_000,
        "B": 1_000_000_000,
        "T": 1_000_000_000_000,
        "Q": 1_000_000_000_000_000,  # Quadrillion (just in case)
        "": 1,  # No suffix
    }

    multiplier = multipliers.get(suffix, 1)
    result = number * multiplier

    # Round to whole number to avoid floating point precision issues
    # For large financial numbers, fractional cents are not meaningful
    return round(result)


def parse_employee_count(value: str) -> int | None:
    """
    Parse employee count strings like '221,000', '75,000' to integers.

    Args:
        value: String value to parse

    Returns:
        Integer employee count or None if unparseable
    """
    if not value or value.upper() in ["N/A", "NA", "", "NULL"]:
        return None

    # Remove commas and spaces
    clean_value = re.sub(r"[,\s]", "", value)

    try:
        return int(clean_value)
    except (ValueError, TypeError):
        return None


def format_currency_display(value: int) -> str:
    """
    Format a numeric currency value for display.

    Args:
        value: Integer value in USD

    Returns:
        Formatted string like '$1.2B', '$500M', etc.
    """
    if value == 0:
        return "N/A"

    abs_value = abs(value)

    if abs_value >= 1_000_000_000_000:  # Trillions
        formatted = f"${value / 1_000_000_000_000:.1f}T"
    elif abs_value >= 1_000_000_000:  # Billions
        formatted = f"${value / 1_000_000_000:.1f}B"
    elif abs_value >= 1_000_000:  # Millions
        formatted = f"${value / 1_000_000:.1f}M"
    elif abs_value >= 1_000:  # Thousands
        formatted = f"${value / 1_000:.1f}K"
    else:
        formatted = f"${value:.0f}"

    # Clean up .0 endings
    return formatted.replace(".0T", "T").replace(".0B", "B").replace(".0M", "M").replace(".0K", "K")


def format_employee_count_display(value: int | None) -> str:
    """
    Format employee count for display.

    Args:
        value: Integer employee count

    Returns:
        Formatted string like '221K', '75K', etc.
    """
    if value is None:
        return "N/A"

    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M".replace(".0M", "M")
    elif value >= 1_000:
        return f"{value / 1_000:.0f}K"
    else:
        return str(value)
