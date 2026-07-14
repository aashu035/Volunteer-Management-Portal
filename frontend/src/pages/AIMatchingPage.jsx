/**
 * AI Matching Page — get volunteer recommendations for tasks.
 */
import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { eventsApi } from "../api/events";
import { tasksApi } from "../api/tasks";
import { aiApi } from "../api/ai";
import { PageHeader, Button, Card, Badge, LoadingSpinner, EmptyState } from "../components/common";
import { BrainCircuit, Sparkles, Target, Zap } from "lucide-react";
import { capitalize } from "../utils/formatters";
import toast from "react-hot-toast";

export default function AIMatchingPage() {
  const [selectedEventId, setSelectedEventId] = useState(null);
  const [selectedTaskId, setSelectedTaskId] = useState(null);

  const { data: eventsData } = useQuery({
    queryKey: ["events", 1],
    queryFn: () => eventsApi.list({ page: 1, per_page: 100 }).then((r) => r.data),
  });

  const { data: tasks } = useQuery({
    queryKey: ["tasks", selectedEventId],
    queryFn: () => tasksApi.getByEvent(selectedEventId).then((r) => r.data),
    enabled: !!selectedEventId,
  });

  const recommendMutation = useMutation({
    mutationFn: (taskId) => aiApi.recommend({ task_id: taskId, top_n: 5 }),
    onError: (err) => toast.error(err.response?.data?.detail || "Recommendation failed"),
  });

  const handleRecommend = () => {
    if (!selectedTaskId) {
      toast.error("Select a task first");
      return;
    }
    recommendMutation.mutate(selectedTaskId);
  };

  const recommendations = recommendMutation.data?.data?.recommendations || [];

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="AI Matching Engine"
        description="Get intelligent volunteer recommendations for tasks."
      />

      {/* Selection */}
      <Card className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          <div>
            <label className="block text-sm font-medium text-surface-700 mb-1.5">Event</label>
            <select
              className="input-field"
              value={selectedEventId || ""}
              onChange={(e) => { setSelectedEventId(e.target.value || null); setSelectedTaskId(null); }}
            >
              <option value="">Choose event...</option>
              {eventsData?.events?.map((e) => (
                <option key={e.id} value={e.id}>{e.title}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-surface-700 mb-1.5">Task</label>
            <select
              className="input-field"
              value={selectedTaskId || ""}
              onChange={(e) => setSelectedTaskId(e.target.value || null)}
              disabled={!selectedEventId}
            >
              <option value="">Choose task...</option>
              {tasks?.map((t) => (
                <option key={t.id} value={t.id}>{t.title}</option>
              ))}
            </select>
          </div>
          <Button onClick={handleRecommend} loading={recommendMutation.isPending}>
            <Sparkles className="w-4 h-4 mr-2 inline" />
            Get Recommendations
          </Button>
        </div>
      </Card>

      {/* Results */}
      {recommendMutation.isPending && <LoadingSpinner />}

      {recommendations.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-surface-800 flex items-center gap-2">
            <BrainCircuit className="w-5 h-5 text-primary-500" />
            Top Matches ({recommendations.length})
          </h2>
          {recommendations.map((match, i) => (
            <Card key={match.volunteer_id} className="animate-slide-up">
              <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                <div className="flex items-center gap-3 flex-1">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary-400 to-accent-400 rounded-full flex items-center justify-center text-white font-bold shadow-md">
                    #{i + 1}
                  </div>
                  <div>
                    <h3 className="font-semibold text-surface-800">{match.volunteer_name}</h3>
                    <div className="flex items-center gap-2 mt-1">
                      <Target className="w-4 h-4 text-primary-500" />
                      <span className="text-sm font-medium text-primary-600">
                        {match.match_score.toFixed(1)}% match
                      </span>
                    </div>
                  </div>
                </div>

                {/* Match progress bar */}
                <div className="w-full sm:w-48">
                  <div className="h-2.5 bg-surface-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full transition-all duration-700"
                      style={{ width: `${Math.min(match.match_score, 100)}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Reasons */}
              {match.match_reasons?.length > 0 && (
                <div className="mt-4 pt-4 border-t border-surface-100">
                  <p className="text-xs font-medium text-surface-400 mb-2 uppercase tracking-wide">Match Reasons</p>
                  <div className="flex flex-wrap gap-2">
                    {match.match_reasons.map((reason, j) => (
                      <div key={j} className="flex items-center gap-1.5 px-3 py-1.5 bg-surface-50 rounded-lg text-xs text-surface-600">
                        <Zap className="w-3 h-3 text-amber-500" />
                        {reason.detail}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}

      {recommendMutation.isSuccess && recommendations.length === 0 && (
        <EmptyState
          icon={BrainCircuit}
          title="No matches found"
          description="No volunteers match the task requirements. Try tasks with broader skill requirements."
        />
      )}
    </div>
  );
}
