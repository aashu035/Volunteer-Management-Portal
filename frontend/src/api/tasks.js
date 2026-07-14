/**
 * Tasks API module.
 */
import client from "./client";

export const tasksApi = {
  getByEvent: (eventId) => client.get(`/tasks/event/${eventId}`),
  get: (id) => client.get(`/tasks/${id}`),
  create: (eventId, data) => client.post(`/tasks/event/${eventId}`, data),
  update: (id, data) => client.put(`/tasks/${id}`, data),
  assign: (id, volunteerId) => client.post(`/tasks/${id}/assign`, { volunteer_id: volunteerId }),
  complete: (id, actualHours) => client.post(`/tasks/${id}/complete`, null, { params: { actual_hours: actualHours } }),
};
