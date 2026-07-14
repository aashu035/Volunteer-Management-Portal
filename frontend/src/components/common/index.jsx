/**
 * Common UI components — Button, Input, Badge, Card, Loading, EmptyState
 */
import { cn } from "../../utils/cn";
import { Loader2 } from "lucide-react";

// ===========================
// Button
// ===========================
export function Button({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  disabled = false,
  className,
  ...props
}) {
  const variants = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    danger: "btn-danger",
    ghost: "px-4 py-2 text-surface-600 hover:bg-surface-100 rounded-xl transition-colors",
  };

  const sizes = {
    sm: "!px-3 !py-1.5 text-sm",
    md: "",
    lg: "!px-8 !py-3 text-lg",
  };

  return (
    <button
      className={cn(variants[variant], sizes[size], className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin inline" />}
      {children}
    </button>
  );
}

// ===========================
// Input
// ===========================
export function Input({ label, error, className, id, ...props }) {
  return (
    <div className="space-y-1.5">
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-surface-700">
          {label}
        </label>
      )}
      <input id={id} className={cn("input-field", error && "border-red-400 focus:ring-red-500/50", className)} {...props} />
      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  );
}

// ===========================
// Badge
// ===========================
export function Badge({ children, variant = "neutral", className }) {
  const variants = {
    success: "badge-success",
    warning: "badge-warning",
    danger: "badge-danger",
    info: "badge-info",
    neutral: "badge-neutral",
  };

  return (
    <span className={cn("badge", variants[variant], className)}>
      {children}
    </span>
  );
}

// ===========================
// Card
// ===========================
export function Card({ children, className, ...props }) {
  return (
    <div className={cn("glass-card p-6", className)} {...props}>
      {children}
    </div>
  );
}

// ===========================
// Loading Spinner
// ===========================
export function LoadingSpinner({ size = "lg", className }) {
  const sizes = { sm: "w-4 h-4", md: "w-6 h-6", lg: "w-10 h-10" };
  return (
    <div className={cn("flex items-center justify-center py-12", className)}>
      <Loader2 className={cn(sizes[size], "animate-spin text-primary-500")} />
    </div>
  );
}

// ===========================
// Empty State
// ===========================
export function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center animate-fade-in">
      {Icon && <Icon className="w-16 h-16 text-surface-300 mb-4" />}
      <h3 className="text-lg font-semibold text-surface-700">{title}</h3>
      {description && <p className="text-surface-500 mt-1 max-w-md">{description}</p>}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}

// ===========================
// Page Header
// ===========================
export function PageHeader({ title, description, actions }) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
      <div>
        <h1 className="gradient-text">{title}</h1>
        {description && <p className="text-surface-500 mt-1">{description}</p>}
      </div>
      {actions && <div className="flex gap-3">{actions}</div>}
    </div>
  );
}

// ===========================
// KPI Card
// ===========================
export function KpiCard({ label, value, icon: Icon, change, changeLabel, className }) {
  return (
    <div className={cn("kpi-card animate-slide-up", className)}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-surface-500">{label}</span>
        {Icon && (
          <div className="p-2.5 bg-primary-50 rounded-xl">
            <Icon className="w-5 h-5 text-primary-600" />
          </div>
        )}
      </div>
      <div className="flex items-end gap-2">
        <span className="text-3xl font-bold text-surface-900">{value}</span>
        {change != null && (
          <span className={cn("text-sm font-medium mb-1", change >= 0 ? "text-emerald-600" : "text-red-500")}>
            {change >= 0 ? "↑" : "↓"} {Math.abs(change)}%
          </span>
        )}
      </div>
      {changeLabel && <span className="text-xs text-surface-400">{changeLabel}</span>}
    </div>
  );
}
