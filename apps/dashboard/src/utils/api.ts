// API utilities for connecting to FastAPI backend

const API_BASE = "http://localhost:8200/api";

// API client
async function apiCall(endpoint: string, options: RequestInit = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || "API request failed");
  }

  return response.json();
}

// Companies API
export const companiesAPI = {
  async getCompanies(
    params: { skip?: number; limit?: number; industry?: string } = {},
  ) {
    const searchParams = new URLSearchParams();
    if (params.skip) searchParams.set("skip", params.skip.toString());
    if (params.limit) searchParams.set("limit", params.limit.toString());
    if (params.industry) searchParams.set("industry", params.industry);

    const query = searchParams.toString();
    return apiCall(`/companies/${query ? `?${query}` : ""}`);
  },

  async getCompany(id: number) {
    return apiCall(`/companies/${id}`);
  },
};

// Items API (keeping for reference)
export const itemsAPI = {
  async getItems(
    params: { skip?: number; limit?: number; status?: string } = {},
  ) {
    const searchParams = new URLSearchParams();
    if (params.skip) searchParams.set("skip", params.skip.toString());
    if (params.limit) searchParams.set("limit", params.limit.toString());
    if (params.status) searchParams.set("status", params.status);

    const query = searchParams.toString();
    return apiCall(`/items/${query ? `?${query}` : ""}`);
  },

  async createItem(itemData: {
    title: string;
    content: string;
    status: string;
  }) {
    return apiCall("/items/", {
      method: "POST",
      body: JSON.stringify(itemData),
    });
  },

  async updateItem(
    id: number,
    itemData: { title?: string; content?: string; status?: string },
  ) {
    return apiCall(`/items/${id}`, {
      method: "PUT",
      body: JSON.stringify(itemData),
    });
  },

  async deleteItem(id: number) {
    return apiCall(`/items/${id}`, {
      method: "DELETE",
    });
  },
};

