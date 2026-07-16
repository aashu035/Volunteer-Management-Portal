"""Pydantic schemas — Dashboard KPIs and chart data."""

from pydantic import BaseModel


class KpiCard(BaseModel):
    label: str
    value: int | float
    change: float | None = None
    change_label: str | None = None


class ChartDataPoint(BaseModel):
    label: str
    value: float


class AdminDashboardResponse(BaseModel):
    total_volunteers: KpiCard
    active_events: KpiCard
    hours_this_month: KpiCard
    pending_tasks: KpiCard
    volunteer_growth: list[ChartDataPoint]
    event_distribution: list[ChartDataPoint]


class CoordinatorDashboardResponse(BaseModel):
    my_events: KpiCard
    total_volunteers: KpiCard
    pending_tasks: KpiCard
    total_hours_logged: KpiCard
    event_distribution: list[ChartDataPoint]


class VolunteerDashboardResponse(BaseModel):
    total_hours: KpiCard
    upcoming_events: KpiCard
    completed_tasks: KpiCard
    rank_or_badges: KpiCard
    hours_history: list[ChartDataPoint]
