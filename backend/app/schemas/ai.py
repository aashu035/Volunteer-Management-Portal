"""Pydantic schemas — AI matching recommendations."""

from uuid import UUID

from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    task_id: UUID
    top_n: int = Field(default=5, ge=1, le=20)


class MatchReason(BaseModel):
    factor: str
    score: float
    detail: str


class MatchResult(BaseModel):
    volunteer_id: UUID
    volunteer_name: str
    match_score: float = Field(..., ge=0, le=100)
    match_reasons: list[MatchReason]


class RecommendResponse(BaseModel):
    task_id: UUID
    recommendations: list[MatchResult]
    algorithm: str = "rule_based"
