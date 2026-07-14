/**
 * Dashboard Page — KPI cards + charts.
 */
import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../api/dashboard";
import { useAuth } from "../context/AuthContext";
import { PageHeader, KpiCard, Card, LoadingSpinner } from "../components/common";
import { Users, Calendar, Clock, ListTodo } from "lucide-react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from "chart.js";
import { Doughnut, Bar } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

export default function DashboardPage() {
  const { user, isAdmin } = useAuth();

  const { data, isLoading } = useQuery({
    queryKey: ["adminDashboard"],
    queryFn: () => dashboardApi.getAdminDashboard().then((r) => r.data),
    enabled: isAdmin,
  });

  if (!isAdmin) {
    return (
      <div className="animate-fade-in">
        <PageHeader title={`Welcome, ${user?.full_name}`} description="Here's your volunteer activity overview." />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <h3 className="text-lg font-semibold text-surface-800 mb-2">Your Activity</h3>
            <p className="text-surface-500">Track your volunteer hours, tasks, and upcoming events from the sidebar.</p>
          </Card>
          <Card>
            <h3 className="text-lg font-semibold text-surface-800 mb-2">Quick Actions</h3>
            <p className="text-surface-500">Browse open events and register to contribute. Every hour counts!</p>
          </Card>
        </div>
      </div>
    );
  }

  if (isLoading) return <LoadingSpinner />;

  const chartColors = {
    planning: "#94a3b8",
    open: "#0ea5e9",
    in_progress: "#f59e0b",
    completed: "#10b981",
    cancelled: "#ef4444",
  };

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

      {/* KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <KpiCard label={data?.total_volunteers?.label} value={data?.total_volunteers?.value} icon={Users} className="stagger-1" />
        <KpiCard label={data?.active_events?.label} value={data?.active_events?.value} icon={Calendar} className="stagger-2" />
        <KpiCard label={data?.hours_this_month?.label} value={data?.hours_this_month?.value} icon={Clock} className="stagger-3" />
        <KpiCard label={data?.pending_tasks?.label} value={data?.pending_tasks?.value} icon={ListTodo} className="stagger-4" />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-semibold text-surface-800 mb-4">Event Status Distribution</h3>
          <div className="h-64 flex items-center justify-center">
            {data?.event_distribution?.length > 0 ? (
              <Doughnut data={eventChartData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }} />
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
