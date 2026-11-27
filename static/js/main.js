/**
 * ApplyEase main frontend utilities
 */

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function getCsrfToken() {
  const inputToken = document.querySelector("[name=csrfmiddlewaretoken]");
  if (inputToken) {
    return inputToken.value;
  }
  return getCookie("csrftoken");
}

async function apiFetch(url, options = {}) {
  const method = (options.method || "GET").toUpperCase();
  const headers = new Headers(options.headers || {});

  if (!["GET", "HEAD", "OPTIONS", "TRACE"].includes(method)) {
    const csrfToken = getCsrfToken();
    if (csrfToken && !headers.has("X-CSRFToken")) {
      headers.set("X-CSRFToken", csrfToken);
    }
  }

  if (options.body && !(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(url, {
    credentials: "same-origin",
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errorText}`);
  }

  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }
  return response.text();
}

function showToast(message, type = "info") {
  const container = document.querySelector("main") || document.body;
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type} alert-dismissible fade show container mt-3`;
  alertDiv.role = "alert";
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  container.prepend(alertDiv);
}
