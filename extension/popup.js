document.addEventListener("DOMContentLoaded", () => {
  const loginSection = document.getElementById("loginSection");
  const actionsSection = document.getElementById("actionsSection");
  const authBadge = document.getElementById("authBadge");
  const statusMessage = document.getElementById("statusMessage");
  const userEmailEl = document.getElementById("userEmail");

  const loginForm = document.getElementById("loginForm");
  const fillBtn = document.getElementById("fillBtn");
  const logBtn = document.getElementById("logBtn");
  const logoutBtn = document.getElementById("logoutBtn");

  function showStatus(text, type = "info") {
    statusMessage.textContent = text;
    statusMessage.className = `status status-${type}`;
  }

  function setAuthenticatedUI(email) {
    loginSection.classList.add("hidden");
    actionsSection.classList.remove("hidden");
    authBadge.textContent = "Signed In";
    authBadge.className = "badge badge-success";
    userEmailEl.textContent = email || "User";
  }

  function setSignedOutUI() {
    actionsSection.classList.add("hidden");
    loginSection.classList.remove("hidden");
    authBadge.textContent = "Signed Out";
    authBadge.className = "badge badge-muted";
    userEmailEl.textContent = "";
  }

  async function init() {
    const res = await chrome.runtime.sendMessage({ type: "GET_AUTH" });
    if (res && res.ok && res.token) {
      setAuthenticatedUI(res.email);
    } else {
      setSignedOutUI();
    }
  }

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    showStatus("Signing in...", "info");
    const res = await chrome.runtime.sendMessage({ type: "LOGIN", email, password });
    if (res && res.ok) {
      setAuthenticatedUI(res.email);
      showStatus("Signed in successfully.", "success");
    } else {
      showStatus((res && res.error) || "Login failed.", "error");
    }
  });

  logoutBtn.addEventListener("click", async () => {
    await chrome.runtime.sendMessage({ type: "LOGOUT" });
    setSignedOutUI();
    showStatus("Signed out.", "info");
  });

  fillBtn.addEventListener("click", async () => {
    showStatus("Fetching profile...", "info");
    const profileRes = await chrome.runtime.sendMessage({ type: "FETCH_PROFILE" });
    if (!profileRes || !profileRes.ok) {
      showStatus((profileRes && profileRes.error) || "Could not load profile.", "error");
      return;
    }

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.id) {
      showStatus("No active tab found.", "error");
      return;
    }

    chrome.tabs.sendMessage(
      tab.id,
      { type: "FILL_FORM", profile: profileRes.profile },
      (fillRes) => {
        if (chrome.runtime.lastError) {
          showStatus("Could not reach page. Reload the tab and try again.", "error");
          return;
        }
        if (fillRes && fillRes.ok) {
          showStatus(`Filled ${fillRes.filledCount} field(s).`, "success");
        } else {
          showStatus((fillRes && fillRes.error) || "Autofill failed.", "error");
        }
      }
    );
  });

  logBtn.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const titleInput = document.getElementById("jobTitle").value.trim();
    const companyInput = document.getElementById("companyName").value.trim();

    const payload = {
      job_title: titleInput || (tab && tab.title) || "Job Application",
      company_name: companyInput || "External Company",
      apply_url: (tab && tab.url) || "",
      status: "applied",
    };

    showStatus("Logging application...", "info");
    const res = await chrome.runtime.sendMessage({ type: "LOG_APPLICATION", payload });
    if (res && res.ok) {
      showStatus("Application logged to tracker!", "success");
    } else {
      showStatus((res && res.error) || "Failed to log application.", "error");
    }
  });

  init();
});
