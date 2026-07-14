"""Dashboard endpoints — KPI data for each role."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.core.permissions import require_role
from app.models.user import User, UserRole
from app.models.event import Event, EventStatus
from app.models.task import Task, TaskStatus
from app.models.attendance import Attendance
from app.schemas.dashboard import AdminDashboardResponse, ChartDataPoint, KpiCard

router = APIRouter()


@router.get("/admin", response_model=AdminDashboardResponse)
async def admin_dashboard(
    current_user: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    """Admin dashboard — global KPIs and charts."""
    # Total volunteers
    vol_count = await db.execute(
        select(func.count()).select_from(User).where(User.role == UserRole.VOLUNTEER)
    )
    total_volunteers = vol_count.scalar_one()

    # Active events
    active_count = await db.execute(
        select(func.count()).select_from(Event).where(
            Event.status.in_([EventStatus.OPEN, EventStatus.IN_PROGRESS])
        )
    )
    active_events = active_count.scalar_one()

    # Hours this month
    now = datetime.now(timezone.utc)
    first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    hours_result = await db.execute(
        select(func.coalesce(func.sum(Attendance.hours_logged), 0))
        .where(Attendance.check_in_time >= first_of_month)
    )
    hours_this_month = float(hours_result.scalar_one())

    # Pending tasks
    pending_count = await db.execute(
        select(func.count()).select_from(Task).where(Task.status == TaskStatus.PENDING)
    )
    pending_tasks = pending_count.scalar_one()

    # Event distribution by status
    event_dist_result = await db.execute(
        select(Event.status, func.count()).group_by(Event.status)
    )
    event_distribution = [
        ChartDataPoint(label=status.value, value=count)
        for status, count in event_dist_result.all()
    ]

    return AdminDashboardResponse(
        total_volunteers=KpiCard(label="Total Volunteers", value=total_volunteers),
        active_events=KpiCard(label="Active Events", value=active_events),
        hours_this_month=KpiCard(label="Hours This Month", value=hours_this_month),
        pending_tasks=KpiCard(label="Pending Tasks", value=pending_tasks),
        volunteer_growth=[],  # Simplified — would need time-series data
        event_distribution=event_distribution,
    )
