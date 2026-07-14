/**
 * Tasks Page — view, create, assign, and complete tasks.
 */
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { eventsApi } from "../../api/events";
import { tasksApi } from "../../api/tasks";
import { useAuth } from "../../context/AuthContext";
import { PageHeader, Button, Card, Badge, LoadingSpinner, EmptyState, Input } from "../../components/common";
import { ListTodo, CheckCircle2 } from "lucide-react";
import { capitalize, formatDateTime } from "../../utils/formatters";
import { STATUS_COLORS } from "../../utils/constants";
import toast from "react-hot-toast";

export default function TasksPage() {
  const { isCoordinator } = useAuth();
  const queryClient = useQueryClient();
  const [selectedEventId, setSelectedEventId] = useState(null);

  const { data: eventsData, isLoading: eventsLoading } = useQuery({
    queryKey: ["events", 1],
    queryFn: () => eventsApi.list({ page: 1, per_page: 100 }).then((r) => r.data),
  });

  const { data: tasks, isLoading: tasksLoading } = useQuery({
    queryKey: ["tasks", selectedEventId],
    queryFn: () => tasksApi.getByEvent(selectedEventId).then((r) => r.data),
    enabled: !!selectedEventId,
  });

  const completeMutation = useMutation({
    mutationFn: (taskId) => tasksApi.complete(taskId),
    onSuccess: () => {
      toast.success("Task completed!");
      queryClient.invalidateQueries(["tasks"]);
    },
  });

  if (eventsLoading) return <LoadingSpinner />;

  return (
    <div className="animate-fade-in">
      <PageHeader title="Tasks" description="Manage tasks across all events." />

      {/* Event selector */}
      <Card className="mb-6">
        <label className="block text-sm font-medium text-surface-700 mb-2">Select Event</label>
        <select
          className="input-field"
          value={selectedEventId || ""}
          onChange={(e) => setSelectedEventId(e.target.value || null)}
        >
          <option value="">Choose an event...</option>
          {eventsData?.events?.map((event) => (
            <option key={event.id} value={event.id}>
              {event.title} ({capitalize(event.status)})
            </option>
          ))}
        </select>
      </Card>

      {!selectedEventId ? (
        <EmptyState icon={ListTodo} title="Select an event" description="Choose an event above to view its tasks." />
      ) : tasksLoading ? (
        <LoadingSpinner />
      ) : tasks?.length === 0 ? (
        <EmptyState icon={ListTodo} title="No tasks yet" description="This event doesn't have any tasks." />
      ) : (
        <div className="space-y-4">
          {tasks?.map((task) => (
            <Card key={task.id} className="flex flex-col sm:flex-row sm:items-center gap-4 hover:shadow-lg transition-shadow">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold text-surface-800">{task.title}</h3>
                  <Badge variant={STATUS_COLORS[task.status]?.replace("badge-", "") || "neutral"}>
                    {capitalize(task.status)}
                  </Badge>
                </div>
                {task.description && <p className="text-sm text-surface-500">{task.description}</p>}
                <div className="flex flex-wrap gap-4 mt-2 text-xs text-surface-400">
                  {task.required_skills?.length > 0 && (
                    <span>Skills: {task.required_skills.join(", ")}</span>
                  )}
                  {task.estimated_hours && <span>Est: {task.estimated_hours}h</span>}
                  {task.deadline && <span>Due: {formatDateTime(task.deadline)}</span>}
                </div>
              </div>
              {task.status !== "completed" && (
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => completeMutation.mutate(task.id)}
                  loading={completeMutation.isPending}
                >
                  <CheckCircle2 className="w-4 h-4 mr-1 inline" />
                  Complete
                </Button>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
