/**
 * Formatting utilities for dates, numbers, and text.
 */
import { format, formatDistanceToNow, parseISO } from "date-fns";

export function formatDate(dateStr) {
  if (!dateStr) return "—";
  const date = typeof dateStr === "string" ? parseISO(dateStr) : dateStr;
  return format(date, "MMM d, yyyy");
}

export function formatDateTime(dateStr) {
  if (!dateStr) return "—";
  const date = typeof dateStr === "string" ? parseISO(dateStr) : dateStr;
  return format(date, "MMM d, yyyy · h:mm a");
}

export function formatRelative(dateStr) {
  if (!dateStr) return "—";
  const date = typeof dateStr === "string" ? parseISO(dateStr) : dateStr;
  return formatDistanceToNow(date, { addSuffix: true });
}

export function formatHours(hours) {
  if (hours == null) return "—";
  return `${Number(hours).toFixed(1)}h`;
}

export function capitalize(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, " ");
}

export function truncate(str, length = 60) {
  if (!str || str.length <= length) return str || "";
  return str.slice(0, length) + "…";
}
