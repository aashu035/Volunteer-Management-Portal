"""
FastAPI dependencies — database session and auth token extraction.
"""

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidCredentialsError, TokenExpiredError
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate JWT, return the current user."""
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise TokenExpiredError()

    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidCredentialsError(detail="Invalid token payload")

    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise InvalidCredentialsError(detail="User not found")

    return user
