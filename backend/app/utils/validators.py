"""Validation utilities."""

import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Basic phone number validation (10-15 digits, optional + prefix)."""
    pattern = r"^\+?[0-9]{10,15}$"
    return bool(re.match(pattern, phone))


def validate_date_range(start: datetime, end: datetime) -> bool:
    """Validate that end date is after start date."""
    return end > start


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets minimum strength requirements.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    return True, ""
