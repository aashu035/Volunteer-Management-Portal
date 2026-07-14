/**
 * Events Page — list, create, and register for events.
 */
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { eventsApi } from "../api/events";
import { useAuth } from "../context/AuthContext";
import { PageHeader, Button, Card, Badge, LoadingSpinner, EmptyState, Input } from "../components/common";
import { Calendar, MapPin, Users, Plus, X } from "lucide-react";
import { formatDateTime, capitalize } from "../utils/formatters";
import { STATUS_COLORS } from "../utils/constants";
import toast from "react-hot-toast";

export default function EventsPage() {
  const { isCoordinator } = useAuth();
  const queryClient = useQueryClient();
  const [showCreate, setShowCreate] = useState(false);
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ["events", page],
    queryFn: () => eventsApi.list({ page, per_page: 12 }).then((r) => r.data),
  });

  const registerMutation = useMutation({
    mutationFn: (eventId) => eventsApi.register(eventId),
    onSuccess: () => {
      toast.success("Registered for event!");
      queryClient.invalidateQueries(["events"]);
    },
    onError: (err) => toast.error(err.response?.data?.detail || "Registration failed"),
  });

  const createMutation = useMutation({
    mutationFn: (data) => eventsApi.create(data),
    onSuccess: () => {
      toast.success("Event created!");
      queryClient.invalidateQueries(["events"]);
      setShowCreate(false);
    },
    onError: (err) => toast.error(err.response?.data?.detail || "Creation failed"),
  });

  const [newEvent, setNewEvent] = useState({
    title: "", description: "", location: "",
    start_date: "", end_date: "", max_volunteers: 50,
  });

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Events"
        description={`${data?.total || 0} total events`}
        actions={
          isCoordinator && (
            <Button onClick={() => setShowCreate(!showCreate)}>
              {showCreate ? <X className="w-4 h-4 mr-2 inline" /> : <Plus className="w-4 h-4 mr-2 inline" />}
              {showCreate ? "Cancel" : "New Event"}
            </Button>
          )
        }
      />

      {/* Create Form */}
      {showCreate && (
        <Card className="mb-8 animate-slide-up">
          <h3 className="text-lg font-semibold mb-4">Create New Event</h3>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createMutation.mutate({
                ...newEvent,
                start_date: new Date(newEvent.start_date).toISOString(),
                end_date: new Date(newEvent.end_date).toISOString(),
                max_volunteers: parseInt(newEvent.max_volunteers),
                required_skill_ids: [],
              });
            }}
            className="grid grid-cols-1 md:grid-cols-2 gap-4"
          >
            <Input id="evt-title" label="Title" value={newEvent.title} onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })} required />
            <Input id="evt-location" label="Location" value={newEvent.location} onChange={(e) => setNewEvent({ ...newEvent, location: e.target.value })} />
            <Input id="evt-start" label="Start Date" type="datetime-local" value={newEvent.start_date} onChange={(e) => setNewEvent({ ...newEvent, start_date: e.target.value })} required />
            <Input id="evt-end" label="End Date" type="datetime-local" value={newEvent.end_date} onChange={(e) => setNewEvent({ ...newEvent, end_date: e.target.value })} required />
            <Input id="evt-max" label="Max Volunteers" type="number" value={newEvent.max_volunteers} onChange={(e) => setNewEvent({ ...newEvent, max_volunteers: e.target.value })} />
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-surface-700 mb-1.5">Description</label>
              <textarea className="input-field min-h-[80px]" value={newEvent.description} onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })} />
            </div>
            <div className="md:col-span-2 flex justify-end gap-3">
              <Button variant="secondary" type="button" onClick={() => setShowCreate(false)}>Cancel</Button>
              <Button type="submit" loading={createMutation.isPending}>Create Event</Button>
            </div>
          </form>
        </Card>
      )}

      {/* Events Grid */}
      {data?.events?.length === 0 ? (
        <EmptyState icon={Calendar} title="No events yet" description="Create your first event to get started." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data?.events?.map((event, i) => (
            <Card key={event.id} className={`hover:shadow-xl transition-all duration-300 animate-slide-up stagger-${(i % 4) + 1}`}>
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-surface-800 line-clamp-1">{event.title}</h3>
                <Badge variant={STATUS_COLORS[event.status]?.replace("badge-", "") || "neutral"}>
                  {capitalize(event.status)}
                </Badge>
              </div>
              {event.description && (
                <p className="text-sm text-surface-500 mb-4 line-clamp-2">{event.description}</p>
              )}
              <div className="space-y-2 text-sm text-surface-600">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-surface-400" />
                  <span>{formatDateTime(event.start_date)}</span>
                </div>
                {event.location && (
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-surface-400" />
                    <span>{event.location}</span>
                  </div>
                )}
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-surface-400" />
                  <span>{event.registered_count || 0} / {event.max_volunteers} volunteers</span>
                </div>
              </div>
              {event.status === "open" && (
                <Button
                  variant="secondary"
                  size="sm"
                  className="w-full mt-4"
                  onClick={() => registerMutation.mutate(event.id)}
                  loading={registerMutation.isPending}
                >
                  Register
                </Button>
              )}
            </Card>
          ))}
        </div>
      )}

      {/* Pagination */}
      {data?.total > 12 && (
        <div className="flex justify-center gap-3 mt-8">
          <Button variant="secondary" size="sm" disabled={page === 1} onClick={() => setPage((p) => p - 1)}>
            Previous
          </Button>
          <span className="flex items-center text-sm text-surface-500">
            Page {page} of {Math.ceil(data.total / 12)}
          </span>
          <Button variant="secondary" size="sm" disabled={page >= Math.ceil(data.total / 12)} onClick={() => setPage((p) => p + 1)}>
            Next
          </Button>
        </div>
      )}
    </div>
  );
}
