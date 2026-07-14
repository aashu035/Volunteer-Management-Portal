/**
 * App Layout — sidebar navigation + main content area.
 */
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { cn } from "../../utils/cn";
import {
  LayoutDashboard,
  Calendar,
  ListTodo,
  Users,
  Bell,
  BrainCircuit,
  LogOut,
  Menu,
  X,
  Sparkles,
} from "lucide-react";
import { useState } from "react";

const navItems = [
  { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard, roles: ["admin", "coordinator", "volunteer"] },
  { path: "/events", label: "Events", icon: Calendar, roles: ["admin", "coordinator", "volunteer"] },
  { path: "/tasks", label: "Tasks", icon: ListTodo, roles: ["admin", "coordinator", "volunteer"] },
  { path: "/volunteers", label: "Volunteers", icon: Users, roles: ["admin", "coordinator"] },
  { path: "/ai-matching", label: "AI Matching", icon: BrainCircuit, roles: ["admin", "coordinator"] },
  { path: "/notifications", label: "Notifications", icon: Bell, roles: ["admin", "coordinator", "volunteer"] },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const filteredNav = navItems.filter((item) => item.roles.includes(user?.role));

  return (
    <div className="flex h-screen bg-surface-50">
      {/* Sidebar */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-surface-100 flex flex-col transition-transform duration-300 lg:relative lg:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-6 py-5 border-b border-surface-100">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl flex items-center justify-center shadow-md">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-base font-bold gradient-text">Amaanitvam</h2>
            <p className="text-xs text-surface-400">Volunteer Portal</p>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="ml-auto lg:hidden p-1 hover:bg-surface-100 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-4 space-y-1 custom-scrollbar overflow-y-auto">
          {filteredNav.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                cn("nav-item", isActive && "nav-item-active")
              }
            >
              <item.icon className="w-5 h-5" />
              {item.label}
            </NavLink>
          ))}
        </nav>

        {/* User info + logout */}
        <div className="border-t border-surface-100 px-4 py-4">
          <div className="flex items-center gap-3 px-4 py-2">
            <div className="w-9 h-9 bg-gradient-to-br from-primary-400 to-accent-400 rounded-full flex items-center justify-center text-white font-semibold text-sm shadow-sm">
              {user?.full_name?.charAt(0)?.toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-surface-800 truncate">{user?.full_name}</p>
              <p className="text-xs text-surface-400 capitalize">{user?.role}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="nav-item w-full mt-2 text-red-500 hover:bg-red-50 hover:text-red-600"
          >
            <LogOut className="w-5 h-5" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/30 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        {/* Top bar (mobile) */}
        <div className="sticky top-0 z-30 bg-white/80 backdrop-blur-xl border-b border-surface-100 px-4 py-3 flex items-center gap-3 lg:hidden">
          <button onClick={() => setSidebarOpen(true)} className="p-2 hover:bg-surface-100 rounded-lg">
            <Menu className="w-5 h-5" />
          </button>
          <span className="font-semibold gradient-text">Amaanitvam Portal</span>
        </div>

        <div className="page-container">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
