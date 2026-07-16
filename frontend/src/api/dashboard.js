/**
 * Dashboard API module.
 */
import client from "./client";

export const dashboardApi = {
  getAdminDashboard: () => client.get("/dashboard/admin"),
  getCoordinatorDashboard: () => client.get("/dashboard/coordinator"),
  getVolunteerDashboard: () => client.get("/dashboard/volunteer"),
};
