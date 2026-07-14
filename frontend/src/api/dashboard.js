/**
 * Dashboard API module.
 */
import client from "./client";

export const dashboardApi = {
  getAdminDashboard: () => client.get("/dashboard/admin"),
};
