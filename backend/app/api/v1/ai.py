"""AI matching endpoint — volunteer-task recommendations."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.core.permissions import require_role
from app.models.user import User
from app.schemas.ai import RecommendRequest, RecommendResponse
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/recommend", response_model=RecommendResponse)
async def get_recommendations(
    data: RecommendRequest,
    current_user: User = Depends(require_role("admin", "coordinator")),
    db: AsyncSession = Depends(get_db),
):
    """Get AI-powered volunteer recommendations for a task (coordinator+ only)."""
    service = AIService(db)
    return await service.recommend(data)
