/**
 * cn() utility — merges Tailwind classes with conflict resolution.
 * Replaces ad-hoc className concatenation.
 */
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
