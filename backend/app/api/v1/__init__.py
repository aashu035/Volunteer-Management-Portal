"""API v1 router — aggregates all endpoint modules."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.events import router as events_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.ai import router as ai_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.volunteers import router as volunteers_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(volunteers_router, prefix="/volunteers", tags=["Volunteers"])
router.include_router(events_router, prefix="/events", tags=["Events"])
router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
router.include_router(ai_router, prefix="/ai", tags=["AI Matching"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
