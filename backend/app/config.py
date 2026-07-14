"""Application configuration via Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment-based configuration with validation."""

    # Application
    ENV: str = "development"
    APP_NAME: str = "Volunteer Management Portal"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/volunteer_portal"
    DATABASE_URL_SYNC: str = "postgresql://postgres:postgres@localhost:5432/volunteer_portal"

    # Authentication
    JWT_SECRET: str = "dev-secret-change-in-production-256-bit-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Frontend (CORS)
    FRONTEND_URL: str = "http://localhost:5173"

    # Email (stubbed)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""

    # AI
    OLLAMA_URL: str = ""
    OPENAI_API_KEY: str = ""

    # Rate Limiting
    RATE_LIMIT: str = "100/minute"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
