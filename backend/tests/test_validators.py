"""Unit tests for validation utilities."""

from app.utils.validators import (
    validate_date_range,
    validate_email,
    validate_password_strength,
    validate_phone,
)
from datetime import datetime, timezone, timedelta


class TestEmailValidation:
    def test_valid_email(self):
        assert validate_email("user@example.com") is True
        assert validate_email("user.name+tag@domain.co.in") is True

    def test_invalid_email(self):
        assert validate_email("userexample.com") is False
        assert validate_email("@domain.com") is False
        assert validate_email("user@") is False
        assert validate_email("") is False


class TestPhoneValidation:
    def test_valid_phone(self):
        assert validate_phone("+919876543210") is True
        assert validate_phone("9876543210") is True

    def test_invalid_phone(self):
        assert validate_phone("123") is False
        assert validate_phone("abc") is False
        assert validate_phone("") is False


class TestPasswordStrength:
    def test_strong_password(self):
        is_valid, _ = validate_password_strength("Admin@123")
        assert is_valid is True

    def test_short_password(self):
        is_valid, msg = validate_password_strength("Ab1")
        assert is_valid is False
        assert "8 characters" in msg

    def test_no_uppercase(self):
        is_valid, msg = validate_password_strength("admin@123")
        assert is_valid is False
        assert "uppercase" in msg

    def test_no_lowercase(self):
        is_valid, msg = validate_password_strength("ADMIN@123")
        assert is_valid is False
        assert "lowercase" in msg

    def test_no_digit(self):
        is_valid, msg = validate_password_strength("Admin@abc")
        assert is_valid is False
        assert "digit" in msg


class TestDateRangeValidation:
    def test_valid_range(self):
        now = datetime.now(timezone.utc)
        assert validate_date_range(now, now + timedelta(days=1)) is True

    def test_invalid_range(self):
        now = datetime.now(timezone.utc)
        assert validate_date_range(now, now - timedelta(days=1)) is False

    def test_equal_dates(self):
        now = datetime.now(timezone.utc)
        assert validate_date_range(now, now) is False
