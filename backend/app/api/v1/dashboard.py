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
from app.models.event import EventRegistration
from app.schemas.dashboard import (
    AdminDashboardResponse,
    CoordinatorDashboardResponse,
    VolunteerDashboardResponse,
    ChartDataPoint,
    KpiCard,
)

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


@router.get("/coordinator", response_model=CoordinatorDashboardResponse)
async def coordinator_dashboard(
    current_user: User = Depends(require_role("coordinator")),
    db: AsyncSession = Depends(get_db),
):
    """Coordinator dashboard — KPIs for events managed by the coordinator."""
    # My active events
    active_count = await db.execute(
        select(func.count()).select_from(Event).where(
            Event.coordinator_id == current_user.id,
            Event.status.in_([EventStatus.OPEN, EventStatus.IN_PROGRESS])
        )
    )
    my_events = active_count.scalar_one()

    # Total unique volunteers in my events
    vol_count = await db.execute(
        select(func.count(func.distinct(EventRegistration.volunteer_id)))
        .select_from(EventRegistration)
        .join(Event, Event.id == EventRegistration.event_id)
        .where(Event.coordinator_id == current_user.id)
    )
    total_volunteers = vol_count.scalar_one()

    # Pending tasks for my events
    pending_count = await db.execute(
        select(func.count()).select_from(Task)
        .join(Event, Event.id == Task.event_id)
        .where(Event.coordinator_id == current_user.id, Task.status == TaskStatus.PENDING)
    )
    pending_tasks = pending_count.scalar_one()

    # Total hours logged for my events
    hours_result = await db.execute(
        select(func.coalesce(func.sum(Attendance.hours_logged), 0))
        .join(Event, Event.id == Attendance.event_id)
        .where(Event.coordinator_id == current_user.id)
    )
    total_hours_logged = float(hours_result.scalar_one())

    # Event distribution for my events
    event_dist_result = await db.execute(
        select(Event.status, func.count())
        .where(Event.coordinator_id == current_user.id)
        .group_by(Event.status)
    )
    event_distribution = [
        ChartDataPoint(label=status.value, value=count)
        for status, count in event_dist_result.all()
    ]

    return CoordinatorDashboardResponse(
        my_events=KpiCard(label="Active Events", value=my_events),
        total_volunteers=KpiCard(label="Volunteers Engaged", value=total_volunteers),
        pending_tasks=KpiCard(label="Pending Tasks", value=pending_tasks),
        total_hours_logged=KpiCard(label="Total Hours", value=total_hours_logged),
        event_distribution=event_distribution,
    )


@router.get("/volunteer", response_model=VolunteerDashboardResponse)
async def volunteer_dashboard(
    current_user: User = Depends(require_role("volunteer")),
    db: AsyncSession = Depends(get_db),
):
    """Volunteer dashboard — personal KPIs and activity."""
    # Total hours logged
    hours_result = await db.execute(
        select(func.coalesce(func.sum(Attendance.hours_logged), 0))
        .where(Attendance.volunteer_id == current_user.id)
    )
    total_hours = float(hours_result.scalar_one())

    # Upcoming events registered for
    now = datetime.now(timezone.utc)
    upcoming_count = await db.execute(
        select(func.count()).select_from(EventRegistration)
        .join(Event, Event.id == EventRegistration.event_id)
        .where(
            EventRegistration.volunteer_id == current_user.id,
            Event.start_date > now,
            Event.status.in_([EventStatus.OPEN, EventStatus.IN_PROGRESS])
        )
    )
    upcoming_events = upcoming_count.scalar_one()

    # Completed tasks assigned to them
    completed_tasks_count = await db.execute(
        select(func.count()).select_from(Task).where(
            Task.assigned_to == current_user.id,
            Task.status == TaskStatus.COMPLETED
        )
    )
    completed_tasks = completed_tasks_count.scalar_one()

    # Dummy data for history (simplified)
    hours_history = [
        ChartDataPoint(label="Jan", value=5),
        ChartDataPoint(label="Feb", value=12),
        ChartDataPoint(label="Mar", value=8),
        ChartDataPoint(label="Apr", value=15),
        ChartDataPoint(label="May", value=total_hours),
    ]

    return VolunteerDashboardResponse(
        total_hours=KpiCard(label="Total Hours", value=total_hours),
        upcoming_events=KpiCard(label="Upcoming Shifts", value=upcoming_events),
        completed_tasks=KpiCard(label="Tasks Completed", value=completed_tasks),
        rank_or_badges=KpiCard(label="Current Rank", value=0, change_label="Bronze"),
        hours_history=hours_history,
    )
