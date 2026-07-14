/**
 * Auth API module.
 */
import client from "./client";

export const authApi = {
  register: (data) => client.post("/auth/register", data),
  login: (data) => client.post("/auth/login", data),
  refresh: (refreshToken) => client.post("/auth/refresh", { refresh_token: refreshToken }),
  logout: () => client.post("/auth/logout"),
  getMe: () => client.get("/users/me"),
};
