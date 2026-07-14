/**
 * Events API module.
 */
import client from "./client";

export const eventsApi = {
  list: (params) => client.get("/events", { params }),
  get: (id) => client.get(`/events/${id}`),
  create: (data) => client.post("/events", data),
  update: (id, data) => client.put(`/events/${id}`, data),
  delete: (id) => client.delete(`/events/${id}`),
  register: (id) => client.post(`/events/${id}/register`),
};
