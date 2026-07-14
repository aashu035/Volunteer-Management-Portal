/**
 * AI matching API module.
 */
import client from "./client";

export const aiApi = {
  recommend: (data) => client.post("/ai/recommend", data),
};
