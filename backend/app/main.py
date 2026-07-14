"""
Amaanitvam Foundation — Volunteer Management Portal
FastAPI Application Entry Point

Critical production fixes applied:
1. Async lifespan (not deprecated @app.on_event)
2. Health check endpoint for Render/Railway
3. Conditional Swagger UI (hidden in production)
4. CORS configuration
"""

import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1 import router as api_v1_router
from app.config import settings
from app.core.logging import setup_logging
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern lifespan handler (replaces deprecated @app.on_event).
    Initializes database engine on startup, disposes on shutdown.
    """
    setup_logging()
    # Startup: engine is created lazily by SQLAlchemy, but we can verify connectivity
    yield
    # Shutdown: dispose the engine connection pool
    await engine.dispose()


# Conditional docs visibility — hidden in production (Critical Fix #5)
is_dev = os.getenv("ENV", "development") != "production"

app = FastAPI(
    title="Volunteer Management Portal API",
    description="AI-powered volunteer management for the Amaanitvam Foundation",
    version="1.0.0",
    docs_url="/docs" if is_dev else None,
    redoc_url="/redoc" if is_dev else None,
    openapi_url="/openapi.json" if is_dev else None,
    lifespan=lifespan,
)

# ===========================
# Middleware
# ===========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
        "https://volunteer-management-portal.vercel.app",
        "https://volunteer-management-portal-git-main-harivanshi.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
from app.core.rate_limit import limiter  # noqa: E402

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ===========================
# Health Check (Critical Fix #3)
# ===========================


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint required by Render/Railway for deployment verification."""
    return {
        "status": "ok",
        "service": "volunteer-management-portal",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ===========================
# API Routes
# ===========================

app.include_router(api_v1_router, prefix="/api/v1")
