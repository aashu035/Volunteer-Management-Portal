"""Authentication service — registration, login, token management."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DuplicateEmailError, InvalidCredentialsError
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.models.volunteer import VolunteerProfile
from app.repositories.user_repo import UserRepository
from app.schemas.user import TokenResponse, UserCreate


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, data: UserCreate) -> tuple[User, TokenResponse]:
        """Register a new user and return JWT tokens."""
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise DuplicateEmailError()

        password_hash = await hash_password(data.password)

        user = User(
            email=data.email,
            password_hash=password_hash,
            full_name=data.full_name,
            phone=data.phone,
            role=UserRole.VOLUNTEER,
        )
        user = await self.user_repo.create(user)

        # Create volunteer profile automatically
        profile = VolunteerProfile(user_id=user.id)
        self.db.add(profile)
        await self.db.flush()

        tokens = self._create_tokens(user)
        return user, tokens

    async def login(self, email: str, password: str) -> tuple[User, TokenResponse]:
        """Authenticate user and return JWT tokens."""
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise InvalidCredentialsError()

        is_valid = await verify_password(password, user.password_hash)
        if not is_valid:
            raise InvalidCredentialsError()

        tokens = self._create_tokens(user)
        return user, tokens

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Generate new access token from refresh token."""
        payload = decode_token(refresh_token)
        if payload is None or payload.get("type") != "refresh":
            raise InvalidCredentialsError(detail="Invalid refresh token")

        user = await self.user_repo.get_by_id(payload["sub"])
        if not user:
            raise InvalidCredentialsError(detail="User not found")

        return self._create_tokens(user)

    @staticmethod
    def _create_tokens(user: User) -> TokenResponse:
        token_data = {"sub": str(user.id), "role": user.role.value}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
        )
