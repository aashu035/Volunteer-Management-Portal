/**
 * Notifications Page — view and manage notifications.
 */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import client from "../../api/client";
import { useAuth } from "../../context/AuthContext";
import { PageHeader, Button, Card, Badge, LoadingSpinner, EmptyState } from "../../components/common";
import { Bell, Check, Trash2 } from "lucide-react";
import { formatRelative, capitalize } from "../../utils/formatters";
import { cn } from "../../utils/cn";
import toast from "react-hot-toast";

export default function NotificationsPage() {
  const queryClient = useQueryClient();

  const { data: notifications, isLoading } = useQuery({
    queryKey: ["notifications"],
    queryFn: () => client.get("/notifications").then((r) => r.data),
  });

  const markReadMutation = useMutation({
    mutationFn: (id) => client.put(`/notifications/${id}/read`),
    onSuccess: () => queryClient.invalidateQueries(["notifications"]),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => client.delete(`/notifications/${id}`),
    onSuccess: () => {
      toast.success("Notification deleted");
      queryClient.invalidateQueries(["notifications"]);
    },
  });

  if (isLoading) return <LoadingSpinner />;

  const unreadCount = notifications?.filter((n) => !n.is_read)?.length || 0;

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Notifications"
        description={`${unreadCount} unread notification${unreadCount !== 1 ? "s" : ""}`}
      />

      {notifications?.length === 0 ? (
        <EmptyState
          icon={Bell}
          title="All caught up!"
          description="You don't have any notifications yet."
        />
      ) : (
        <div className="space-y-3">
          {notifications?.map((notif) => (
            <Card
              key={notif.id}
              className={cn(
                "flex items-start gap-4 transition-all duration-200",
                !notif.is_read && "border-l-4 border-l-primary-500 bg-primary-50/30"
              )}
            >
              <div className={cn(
                "w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0",
                notif.is_read ? "bg-surface-100" : "bg-primary-100"
              )}>
                <Bell className={cn("w-5 h-5", notif.is_read ? "text-surface-400" : "text-primary-600")} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h4 className="font-semibold text-surface-800">{notif.title}</h4>
                  <Badge variant={notif.is_read ? "neutral" : "info"}>
                    {capitalize(notif.type?.replace(/_/g, " "))}
                  </Badge>
                </div>
                {notif.message && <p className="text-sm text-surface-500 mt-1">{notif.message}</p>}
                <span className="text-xs text-surface-400 mt-1 block">{formatRelative(notif.created_at)}</span>
              </div>
              <div className="flex gap-1 flex-shrink-0">
                {!notif.is_read && (
                  <button
                    onClick={() => markReadMutation.mutate(notif.id)}
                    className="p-2 hover:bg-surface-100 rounded-lg transition-colors"
                    title="Mark as read"
                  >
                    <Check className="w-4 h-4 text-emerald-500" />
                  </button>
                )}
                <button
                  onClick={() => deleteMutation.mutate(notif.id)}
                  className="p-2 hover:bg-red-50 rounded-lg transition-colors"
                  title="Delete"
                >
                  <Trash2 className="w-4 h-4 text-red-400" />
                </button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
