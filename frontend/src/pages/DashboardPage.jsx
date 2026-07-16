/**
 * Dashboard Page — KPI cards + charts.
 */
import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../api/dashboard";
import { useAuth } from "../context/AuthContext";
import { PageHeader, KpiCard, Card, LoadingSpinner } from "../components/common";
import { Users, Calendar, Clock, ListTodo, Award, CheckCircle } from "lucide-react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from "chart.js";
import { Doughnut, Bar } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const chartColors = {
  planning: "#94a3b8",
  open: "#0ea5e9",
  in_progress: "#f59e0b",
  completed: "#10b981",
  cancelled: "#ef4444",
};

export default function DashboardPage() {
  const { user } = useAuth();
  const role = user?.role; // "admin", "coordinator", "volunteer"

  const { data, isLoading } = useQuery({
    queryKey: ["dashboard", role],
    queryFn: async () => {
      if (role === "admin") return (await dashboardApi.getAdminDashboard()).data;
      if (role === "coordinator") return (await dashboardApi.getCoordinatorDashboard()).data;
      if (role === "volunteer") return (await dashboardApi.getVolunteerDashboard()).data;
      return null;
    },
    enabled: !!role,
  });

  if (isLoading) return <LoadingSpinner />;

  // Admin View
  if (role === "admin") {
    const eventChartData = {
      labels: data?.event_distribution?.map((d) => d.label.replace("_", " ")) || [],
      datasets: [
        {
          data: data?.event_distribution?.map((d) => d.value) || [],
          backgroundColor: data?.event_distribution?.map((d) => chartColors[d.label] || "#64748b") || [],
          borderWidth: 0,
        },
      ],
    };

    return (
      <div className="animate-fade-in">
        <PageHeader title="Admin Dashboard" description="Real-time KPIs and analytics overview." />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KpiCard label={data?.total_volunteers?.label} value={data?.total_volunteers?.value} icon={Users} className="stagger-1" />
          <KpiCard label={data?.active_events?.label} value={data?.active_events?.value} icon={Calendar} className="stagger-2" />
          <KpiCard label={data?.hours_this_month?.label} value={data?.hours_this_month?.value} icon={Clock} className="stagger-3" />
          <KpiCard label={data?.pending_tasks?.label} value={data?.pending_tasks?.value} icon={ListTodo} className="stagger-4" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <h3 className="text-lg font-semibold text-surface-800 mb-4">Event Status Distribution</h3>
            <div className="h-64 flex items-center justify-center">
              {data?.event_distribution?.length > 0 ? (
                <Doughnut data={eventChartData} options={{ responsive: true, maintainAspectRatio: false }} />
              ) : (
                <p className="text-surface-400">No events yet</p>
              )}
            </div>
          </Card>
          <Card>
            <h3 className="text-lg font-semibold text-surface-800 mb-4">Platform Overview</h3>
            <div className="space-y-4 mt-4">
              <div className="flex items-center justify-between p-4 bg-primary-50 rounded-xl">
                <span className="text-sm font-medium text-primary-700">Active Volunteers</span>
                <span className="text-2xl font-bold text-primary-800">{data?.total_volunteers?.value}</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-emerald-50 rounded-xl">
                <span className="text-sm font-medium text-emerald-700">Events Running</span>
                <span className="text-2xl font-bold text-emerald-800">{data?.active_events?.value}</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-amber-50 rounded-xl">
                <span className="text-sm font-medium text-amber-700">Pending Tasks</span>
                <span className="text-2xl font-bold text-amber-800">{data?.pending_tasks?.value}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  // Coordinator View
  if (role === "coordinator") {
    const eventChartData = {
      labels: data?.event_distribution?.map((d) => d.label.replace("_", " ")) || [],
      datasets: [
        {
          data: data?.event_distribution?.map((d) => d.value) || [],
          backgroundColor: data?.event_distribution?.map((d) => chartColors[d.label] || "#64748b") || [],
          borderWidth: 0,
        },
      ],
    };

    return (
      <div className="animate-fade-in">
        <PageHeader title={`Welcome, ${user?.full_name}`} description="Coordinator Dashboard — Track events you manage." />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KpiCard label={data?.my_events?.label} value={data?.my_events?.value} icon={Calendar} className="stagger-1" />
          <KpiCard label={data?.total_volunteers?.label} value={data?.total_volunteers?.value} icon={Users} className="stagger-2" />
          <KpiCard label={data?.pending_tasks?.label} value={data?.pending_tasks?.value} icon={ListTodo} className="stagger-3" />
          <KpiCard label={data?.total_hours_logged?.label} value={data?.total_hours_logged?.value} icon={Clock} className="stagger-4" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <h3 className="text-lg font-semibold text-surface-800 mb-4">My Events Distribution</h3>
            <div className="h-64 flex items-center justify-center">
              {data?.event_distribution?.length > 0 ? (
                <Doughnut data={eventChartData} options={{ responsive: true, maintainAspectRatio: false }} />
              ) : (
                <p className="text-surface-400">No events yet</p>
              )}
            </div>
          </Card>
          <Card>
            <h3 className="text-lg font-semibold text-surface-800 mb-4">Quick Actions</h3>
            <div className="space-y-4">
              <p className="text-surface-500">Manage your events, approve tasks, and coordinate volunteers from the sidebar.</p>
              <div className="flex items-center justify-between p-4 bg-emerald-50 rounded-xl">
                <span className="text-sm font-medium text-emerald-700">Total Hours Logged</span>
                <span className="text-2xl font-bold text-emerald-800">{data?.total_hours_logged?.value}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  // Volunteer View
  if (role === "volunteer") {
    const historyChartData = {
      labels: data?.hours_history?.map((d) => d.label) || [],
      datasets: [
        {
          label: "Hours Logged",
          data: data?.hours_history?.map((d) => d.value) || [],
          backgroundColor: "#0ea5e9",
        },
      ],
    };

    return (
      <div className="animate-fade-in">
        <PageHeader title={`Welcome, ${user?.full_name}`} description="Here's your volunteer activity overview." />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KpiCard label={data?.total_hours?.label} value={data?.total_hours?.value} icon={Clock} className="stagger-1" />
          <KpiCard label={data?.upcoming_events?.label} value={data?.upcoming_events?.value} icon={Calendar} className="stagger-2" />
          <KpiCard label={data?.completed_tasks?.label} value={data?.completed_tasks?.value} icon={CheckCircle} className="stagger-3" />
          <KpiCard label={data?.rank_or_badges?.label} value={data?.rank_or_badges?.change_label || data?.rank_or_badges?.value} icon={Award} className="stagger-4" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <h3 className="text-lg font-semibold text-surface-800 mb-4">Hours Over Time</h3>
            <div className="h-64 flex items-center justify-center">
              {data?.hours_history?.length > 0 ? (
                <Bar data={historyChartData} options={{ responsive: true, maintainAspectRatio: false }} />
              ) : (
                <p className="text-surface-400">No data available</p>
              )}
            </div>
          </Card>
          <Card>
            <h3 className="text-lg font-semibold text-surface-800 mb-2">Ready to contribute?</h3>
            <p className="text-surface-500 mb-4">Browse open events and register to contribute. Every hour counts!</p>
            <div className="p-4 bg-primary-50 rounded-xl">
              <span className="block text-sm font-medium text-primary-700 mb-1">Upcoming Shifts</span>
              <span className="text-2xl font-bold text-primary-800">{data?.upcoming_events?.value}</span>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return null;
}
