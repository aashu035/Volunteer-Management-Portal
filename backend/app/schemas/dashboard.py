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
