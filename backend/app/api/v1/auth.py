"""Auth endpoints — register, login, refresh."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import MessageResponse, TokenRefreshRequest, TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

from app.core.rate_limit import limiter

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
@limiter.limit("5/minute")
async def register(request: Request, data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new volunteer account."""
    auth_service = AuthService(db)
    _, tokens = await auth_service.register(data)
    return tokens


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login with email and password."""
    auth_service = AuthService(db)
    _, tokens = await auth_service.login(data.email, data.password)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    """Refresh access token using a valid refresh token."""
    auth_service = AuthService(db)
    return await auth_service.refresh_token(data.refresh_token)


@router.post("/logout", response_model=MessageResponse)
async def logout():
    """Logout (client-side token removal). Token blacklisting requires Redis (future)."""
    return MessageResponse(message="Successfully logged out")
