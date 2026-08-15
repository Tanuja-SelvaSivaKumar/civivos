const API_BASE_URL = "http://127.0.0.1:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  let data = null;
  try { data = await response.json(); } catch { data = null; }

  if (!response.ok) {
    throw new Error(data?.detail || `Request failed with status ${response.status}`);
  }
  return data;
}

export function createCase(citizenName, complaint) {
  return request('/cases', { method: 'POST', body: JSON.stringify({ citizen_name: citizenName, complaint }) });
}
export function getCase(caseId) { return request(`/cases/${encodeURIComponent(caseId)}`); }
export function getTimeline(caseId) { return request(`/cases/${encodeURIComponent(caseId)}/timeline`); }
export function getFirstAppeal(caseId) { return request(`/cases/${encodeURIComponent(caseId)}/first-appeal`); }
export function approveCase(caseId) { return request(`/cases/${encodeURIComponent(caseId)}/approve`, { method: 'POST' }); }
export function fileCase(caseId) { return request(`/cases/${encodeURIComponent(caseId)}/file`, { method: 'POST' }); }
export function waitForResponse(caseId) { return request(`/cases/${encodeURIComponent(caseId)}/wait`, { method: 'POST' }); }
export function runWatcher() { return request('/watcher/run', { method: 'POST' }); }
