// src/api/client.js

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

/**
 * Enhanced generic fetch wrapper.
 */
async function apiClient(endpoint, customConfig = {}) {
  const token = localStorage.getItem("auth_token");
  const headers = { 
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const config = {
    method: "GET",
    ...customConfig,
    headers: {
      ...headers,
      ...customConfig.headers,
    },
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    if (!response.ok) {
      const errorText = await response.text();
      let errorMessage = response.statusText;
      try {
        const errorJson = JSON.parse(errorText);
        errorMessage = errorJson.detail || errorMessage;
      } catch (e) {}
      throw new Error(`API Error ${response.status}: ${errorMessage}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    throw error;
  }
}

// ─── API Methods ─────────────────────────────────────────────────────────────

export async function fetchJobs(params = {}) {
  const query = new URLSearchParams();
  if (params.query) query.append("query", params.query);
  if (params.location) query.append("location", params.location);
  if (params.job_types && params.job_types.length) query.append("job_types", params.job_types.join(","));
  if (params.remote_only !== undefined) query.append("remote_only", params.remote_only ? "true" : "false");
  // etc for other params
  
  return apiClient(`/jobs/search?${query.toString()}`);
}

export async function fetchSalaryInsights(role, location = "") {
  const query = new URLSearchParams();
  query.append("role", role);
  if (location) query.append("location", location);
  
  return apiClient(`/insights/salary?${query.toString()}`);
}

export async function fetchSkillDemand(limit = 10) {
  return apiClient(`/insights/skills/demand?limit=${limit}`);
}

export async function fetchCompanies(limit = 20) {
  return apiClient(`/insights/companies?limit=${limit}`);
}

// ─── Authentication ──────────────────────────────────────────────────────────

export async function login(email, password) {
  const data = await apiClient("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  if (data.accessToken) {
    localStorage.setItem("auth_token", data.accessToken);
  }
  return data;
}

export async function register(email, password, firstName, lastName) {
  return apiClient("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password, firstName, lastName }),
  });
}

