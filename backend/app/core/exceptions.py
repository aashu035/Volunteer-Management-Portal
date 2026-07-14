"""
Custom exception classes with structured error codes.

Error codes follow the SRS error code scheme:
  AUTH001-004, VAL001-003, RES001-002, SRV001
"""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception with error code."""

    def __init__(self, status_code: int, detail: str, error_code: str = "SRV001"):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


# ===========================
# Authentication Errors
# ===========================


class InvalidCredentialsError(AppException):
    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH001",
        )


class TokenExpiredError(AppException):
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH002",
        )


class InsufficientPermissionsError(AppException):
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTH003",
        )


class DuplicateEmailError(AppException):
    def __init__(self, detail: str = "Email already registered"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="AUTH004",
        )


# ===========================
# Validation Errors
# ===========================


class ValidationError(AppException):
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="VAL001",
        )


class InvalidDateRangeError(AppException):
    def __init__(self, detail: str = "End date must be after start date"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="VAL002",
        )


# ===========================
# Resource Errors
# ===========================


class ResourceNotFoundError(AppException):
    def __init__(self, resource: str = "Resource", detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail or f"{resource} not found",
            error_code="RES001",
        )


class ResourceAlreadyExistsError(AppException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="RES002",
        )


# ===========================
# Event-Specific Errors
# ===========================


class EventFullError(AppException):
    def __init__(self, detail: str = "Event has reached maximum capacity"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="EVT001",
        )
