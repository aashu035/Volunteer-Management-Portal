"""
RBAC permissions — decorators and dependency functions for role-based access control.
"""

from functools import wraps

from fastapi import Depends, HTTPException, status

from app.core.exceptions import InsufficientPermissionsError
from app.dependencies import get_current_user


def require_role(*allowed_roles: str):
    """
    FastAPI dependency factory — restricts endpoint access to specific roles.

    Usage:
        @router.post("/events", dependencies=[Depends(require_role("admin", "coordinator"))])
    """
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise InsufficientPermissionsError(
                detail=f"Role '{current_user.role}' is not authorized. Required: {', '.join(allowed_roles)}"
            )
        return current_user

    return role_checker


def require_admin():
    """Shortcut dependency — requires admin role."""
    return require_role("admin")


def require_coordinator():
    """Shortcut dependency — requires coordinator or admin role."""
    return require_role("admin", "coordinator")
