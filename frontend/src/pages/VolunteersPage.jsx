/**
 * Volunteers Page — list and search volunteers (admin/coordinator only).
 */
import { useQuery } from "@tanstack/react-query";
import client from "../api/client";
import { PageHeader, Card, Badge, LoadingSpinner, EmptyState } from "../components/common";
import { Users, MapPin, Clock } from "lucide-react";
import { formatHours } from "../utils/formatters";

export default function VolunteersPage() {
  const { data: volunteers, isLoading } = useQuery({
    queryKey: ["volunteers"],
    queryFn: () => client.get("/volunteers").then((r) => r.data),
  });

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="animate-fade-in">
      <PageHeader title="Volunteers" description={`${volunteers?.length || 0} registered volunteers`} />

      {volunteers?.length === 0 ? (
        <EmptyState icon={Users} title="No volunteers yet" description="Volunteers will appear here after registration." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {volunteers?.map((vol, i) => (
            <Card key={vol.id} className={`hover:shadow-xl transition-all duration-300 animate-slide-up stagger-${(i % 4) + 1}`}>
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-primary-400 to-accent-400 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-md">
                  {vol.bio?.charAt(0)?.toUpperCase() || "V"}
                </div>
                <div>
                  <h3 className="font-semibold text-surface-800">Volunteer</h3>
                  {vol.location && (
                    <div className="flex items-center gap-1 text-xs text-surface-400">
                      <MapPin className="w-3 h-3" />
                      {vol.location}
                    </div>
                  )}
                </div>
              </div>

              {vol.bio && <p className="text-sm text-surface-500 mb-3 line-clamp-2">{vol.bio}</p>}

              <div className="flex items-center justify-between pt-3 border-t border-surface-100">
                <div className="flex items-center gap-1.5 text-sm text-surface-600">
                  <Clock className="w-4 h-4 text-primary-500" />
                  <span className="font-medium">{formatHours(vol.total_hours)}</span>
                </div>
                {vol.badges?.length > 0 && (
                  <div className="flex gap-1">
                    {vol.badges.slice(0, 3).map((badge, j) => (
                      <Badge key={j} variant="info">{badge}</Badge>
                    ))}
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
