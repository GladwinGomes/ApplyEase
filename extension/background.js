const API_BASE = "http://localhost:8000";

async function getStoredAuth() {
  const data = await chrome.storage.local.get(["authToken", "userEmail"]);
  return {
    token: data.authToken || null,
    email: data.userEmail || null,
  };
}

async function setStoredAuth(token, email) {
  await chrome.storage.local.set({ authToken: token, userEmail: email });
}

async function clearStoredAuth() {
  await chrome.storage.local.remove(["authToken", "userEmail"]);
}

async function apiRequest(endpoint, options = {}) {
  const { token } = await getStoredAuth();
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = `Token ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { detail: text };
  }

  if (!response.ok) {
    throw new Error(data.detail || data.error || `Request failed (${response.status})`);
  }

  return data;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  (async () => {
    try {
      if (message.type === "GET_AUTH") {
        const auth = await getStoredAuth();
        sendResponse({ ok: true, ...auth });
        return;
      }

      if (message.type === "LOGIN") {
        const data = await apiRequest("/accounts/api/login/", {
          method: "POST",
          body: JSON.stringify({
            email: message.email,
            password: message.password,
          }),
        });
        const token = data.token || data.key;
        if (!token) {
          throw new Error("No auth token returned by server.");
        }
        await setStoredAuth(token, message.email);
        sendResponse({ ok: true, token, email: message.email });
        return;
      }

      if (message.type === "LOGOUT") {
        await clearStoredAuth();
        sendResponse({ ok: true });
        return;
      }

      if (message.type === "FETCH_PROFILE") {
        const profile = await apiRequest("/api/profile/", { method: "GET" });
        sendResponse({ ok: true, profile });
        return;
      }

      if (message.type === "LOG_APPLICATION") {
        const payload = message.payload || {};
        const application = await apiRequest("/api/applications/", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        sendResponse({ ok: true, application });
        return;
      }

      sendResponse({ ok: false, error: `Unknown message type: ${message.type}` });
    } catch (err) {
      sendResponse({ ok: false, error: err.message || "Unexpected error" });
    }
  })();

  return true;
});
