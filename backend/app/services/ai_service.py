"""
AI Matching Service — Rule-based volunteer-task matching engine.

Implements the scoring algorithm from SRS-AI-001 to SRS-AI-004:
  - Skill matching (exact 100%, fuzzy 70%)
  - Proficiency bonus (+10% expert, +5% intermediate)
  - Historical performance (+15% for >90% completion, -20% for <50%)
  - Explainable reasoning for each recommendation
"""

from uuid import UUID

from rapidfuzz import fuzz
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ResourceNotFoundError
from app.models.task import Task
from app.models.user import User, UserRole
from app.models.volunteer import VolunteerProfile
from app.models.skill import VolunteerSkill, Skill
from app.schemas.ai import MatchReason, MatchResult, RecommendRequest, RecommendResponse


class AIService:
    """Rule-based AI matching engine with explainable scoring."""

    EXACT_MATCH_SCORE = 100.0
    FUZZY_MATCH_THRESHOLD = 70.0
    EXPERT_BONUS = 10.0
    INTERMEDIATE_BONUS = 5.0
    HIGH_COMPLETION_BONUS = 15.0
    LOW_COMPLETION_PENALTY = -20.0

    def __init__(self, db: AsyncSession):
        self.db = db

    async def recommend(self, request: RecommendRequest) -> RecommendResponse:
        """Generate volunteer recommendations for a task."""
        # Get task
        task_result = await self.db.execute(select(Task).where(Task.id == request.task_id))
        task = task_result.scalar_one_or_none()
        if not task:
            raise ResourceNotFoundError("Task")

        # Get all active volunteers with skills
        vol_result = await self.db.execute(
            select(User)
            .where(User.role == UserRole.VOLUNTEER, User.status == "active")
            .options(selectinload(User.volunteer_profile))
        )
        volunteers = list(vol_result.scalars().all())

        # Score each volunteer
        scored = []
        for volunteer in volunteers:
            if volunteer.volunteer_profile is None:
                continue
            score, reasons = await self._score_volunteer(volunteer, task)
            if score > 0:
                scored.append(MatchResult(
                    volunteer_id=volunteer.id,
                    volunteer_name=volunteer.full_name,
                    match_score=min(score, 100.0),
                    match_reasons=reasons,
                ))

        # Sort by score descending, take top N
        scored.sort(key=lambda x: x.match_score, reverse=True)
        top_matches = scored[:request.top_n]

        return RecommendResponse(
            task_id=request.task_id,
            recommendations=top_matches,
            algorithm="rule_based",
        )

    async def _score_volunteer(self, volunteer: User, task: Task) -> tuple[float, list[MatchReason]]:
        """Score a volunteer against a task with explainable reasons."""
        total_score = 0.0
        reasons = []

        # 1. Skill matching
        required_skills = task.required_skills or []
        if required_skills:
            skill_score, skill_reasons = await self._score_skills(volunteer, required_skills)
            total_score += skill_score
            reasons.extend(skill_reasons)
        else:
            # No skill requirements — give base score
            total_score += 50.0
            reasons.append(MatchReason(
                factor="skills", score=50.0, detail="No specific skills required"
            ))

        # 2. Historical performance
        profile = volunteer.volunteer_profile
        if profile and profile.total_hours > 0:
            perf_score, perf_reason = self._score_performance(profile)
            total_score += perf_score
            reasons.append(perf_reason)

        return total_score, reasons

    async def _score_skills(
        self, volunteer: User, required_skills: list[str]
    ) -> tuple[float, list[MatchReason]]:
        """Score volunteer's skills against task requirements."""
        # Get volunteer's skills
        vol_skills_result = await self.db.execute(
            select(VolunteerSkill, Skill)
            .join(Skill, VolunteerSkill.skill_id == Skill.id)
            .where(VolunteerSkill.volunteer_id == volunteer.volunteer_profile.id)
        )
        vol_skills = vol_skills_result.all()

        if not vol_skills:
            return 0.0, [MatchReason(factor="skills", score=0.0, detail="No skills listed")]

        vol_skill_names = {skill.name.lower(): (vs, skill) for vs, skill in vol_skills}
        total_skill_score = 0.0
        reasons = []

        for req_skill in required_skills:
            req_lower = req_skill.lower()
            best_match_score = 0.0
            best_match_name = ""
            best_proficiency_bonus = 0.0

            for vol_name, (vs, skill) in vol_skill_names.items():
                # Exact match
                if vol_name == req_lower:
                    match_pct = self.EXACT_MATCH_SCORE
                else:
                    # Fuzzy match
                    match_pct = fuzz.ratio(req_lower, vol_name)

                if match_pct >= self.FUZZY_MATCH_THRESHOLD and match_pct > best_match_score:
                    best_match_score = match_pct
                    best_match_name = skill.name
                    # Proficiency bonus
                    if vs.proficiency.value == "expert":
                        best_proficiency_bonus = self.EXPERT_BONUS
                    elif vs.proficiency.value == "intermediate":
                        best_proficiency_bonus = self.INTERMEDIATE_BONUS

            if best_match_score > 0:
                score = (best_match_score / 100.0) * 40.0 + best_proficiency_bonus
                total_skill_score += score
                match_type = "exact" if best_match_score == 100 else "fuzzy"
                reasons.append(MatchReason(
                    factor="skill_match",
                    score=score,
                    detail=f"{match_type.title()} match: '{best_match_name}' → '{req_skill}' ({best_match_score:.0f}%)"
                ))

        avg_score = total_skill_score / len(required_skills) if required_skills else 0
        return avg_score, reasons

    @staticmethod
    def _score_performance(profile: VolunteerProfile) -> tuple[float, MatchReason]:
        """Score based on historical performance (total hours as proxy)."""
        hours = profile.total_hours
        if hours > 50:
            return AIService.HIGH_COMPLETION_BONUS, MatchReason(
                factor="performance",
                score=AIService.HIGH_COMPLETION_BONUS,
                detail=f"High performer: {hours:.0f} hours logged"
            )
        elif hours < 5:
            return AIService.LOW_COMPLETION_PENALTY, MatchReason(
                factor="performance",
                score=AIService.LOW_COMPLETION_PENALTY,
                detail=f"New volunteer: only {hours:.0f} hours logged"
            )
        return 0.0, MatchReason(
            factor="performance", score=0.0, detail=f"{hours:.0f} hours logged"
        )
