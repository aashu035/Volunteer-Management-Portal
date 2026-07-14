/**
 * Application constants.
 */

export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const ROLES = {
  ADMIN: "admin",
  COORDINATOR: "coordinator",
  VOLUNTEER: "volunteer",
};

export const EVENT_STATUS = {
  PLANNING: "planning",
  OPEN: "open",
  IN_PROGRESS: "in_progress",
  COMPLETED: "completed",
  CANCELLED: "cancelled",
};

export const TASK_STATUS = {
  PENDING: "pending",
  IN_PROGRESS: "in_progress",
  COMPLETED: "completed",
  BLOCKED: "blocked",
};

export const STATUS_COLORS = {
  planning: "badge-neutral",
  open: "badge-info",
  in_progress: "badge-warning",
  completed: "badge-success",
  cancelled: "badge-danger",
  pending: "badge-neutral",
  blocked: "badge-danger",
  active: "badge-success",
  inactive: "badge-neutral",
};
