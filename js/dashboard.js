/* ============================================
   DASHBOARD.JS — Custom Inbox Interactivity
   ============================================ */

const API_BASE = '/api/contact/';

const loginGate = document.getElementById("loginGate");
const dashboardWrap = document.getElementById("dashboardWrap");
const loginForm = document.getElementById("loginForm");
const adminKeyInput = document.getElementById("adminKey");
const loginError = document.getElementById("loginError");
const inboxGrid = document.getElementById("inboxGrid");
const logoutBtn = document.getElementById("logoutBtn");
const forgotBtn = document.getElementById("forgotBtn");

// ── Check if logged in already ────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  const storedKey = sessionStorage.getItem("inbox_key");
  if (storedKey) {
    loadInbox(storedKey);
  }
});

// ── Handle Login Form Submission ─────────────────────────────
if (loginForm) {
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const key = adminKeyInput.value.trim();
    if (!key) return;

    loadInbox(key);
  });
}
// ── Handle Forgot Key Recovery ──────────────────────────────
if (forgotBtn) {
  forgotBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    
    const confirmSend = confirm(
      "Forgot key? Click OK to send your access key to the registered administrator email address."
    );
    if (!confirmSend) return;

    forgotBtn.textContent = "Notifying...";
    forgotBtn.style.pointerEvents = "none";

    try {
      const res = await fetch(`${API_BASE}?action=forgot`);
      const data = await res.json();
      
      if (res.ok && data.success) {
        alert("A password recovery alert has been sent to the administrator email address. Please check your inbox to confirm and allow.");
      } else {
        alert(data.error || "Failed to trigger email notification. Please try again later.");
      }
    } catch (err) {
      console.error(err);
      alert("Error reaching recovery server. Is Django running?");
    } finally {
      forgotBtn.textContent = "Forgot Key? Recovery Notify →";
      forgotBtn.style.pointerEvents = "auto";
    }
  });
}

// ── Load Messages ────────────────────────────────────────────
async function loadInbox(key) {
  showLoginError(""); // Reset error
  
  try {
    const res = await fetch(`${API_BASE}?key=${key}`);
    const data = await res.json();

    if (res.ok && data.success) {
      sessionStorage.setItem("inbox_key", key);
      
      // Toggle Views
      loginGate.style.display = "none";
      dashboardWrap.style.display = "block";
      
      renderMessages(data.messages, key);
    } else {
      sessionStorage.removeItem("inbox_key");
      showLoginError(data.error || "Authentication failed. Invalid key.");
    }
  } catch (err) {
    console.error(err);
    showLoginError("Error connecting to server. Make sure backend is running.");
  }
}

// ── Render Messages List ─────────────────────────────────────
function renderMessages(messages, key) {
  if (!inboxGrid) return;
  inboxGrid.innerHTML = "";

  if (messages.length === 0) {
    inboxGrid.innerHTML = `
      <div class="empty-state">
        <p>No messages received yet. Your inbox is empty.</p>
      </div>
    `;
    return;
  }

  messages.forEach((msg, idx) => {
    // Format index (e.g. 001, 002)
    const cardNum = String(idx + 1).padStart(3, '0');
    
    const card = document.createElement("div");
    card.className = "message-card fade-up";
    card.innerHTML = `
      <div class="project-num">${cardNum}</div>
      <div class="message-header">
        <div class="message-sender">
          <h3>${escapeHtml(msg.name)}</h3>
          <span><a href="mailto:${escapeHtml(msg.email)}">${escapeHtml(msg.email)}</a></span>
        </div>
        <div class="message-date">${escapeHtml(msg.created_at)}</div>
      </div>
      <div class="message-body">${escapeHtml(msg.message)}</div>
      <div class="message-actions">
        <button class="btn outline small btn-delete" data-id="${msg.id}">Delete Message</button>
      </div>
    `;

    // Bind delete button listener
    const deleteBtn = card.querySelector(".btn-delete");
    deleteBtn.addEventListener("click", async () => {
      if (confirm("Are you sure you want to delete this message?")) {
        deleteBtn.textContent = "Deleting...";
        deleteBtn.disabled = true;
        await deleteMessage(msg.id, key);
      }
    });

    inboxGrid.appendChild(card);
  });
}

// ── Delete Message ───────────────────────────────────────────
async function deleteMessage(id, key) {
  try {
    const res = await fetch(`${API_BASE}?id=${id}&key=${key}`, {
      method: "DELETE"
    });
    
    if (res.ok) {
      // Reload inbox to reflect deletion
      loadInbox(key);
    } else {
      alert("Failed to delete message. Try again.");
    }
  } catch (err) {
    console.error(err);
    alert("Connection error. Could not delete message.");
  }
}

// ── Handle Log Out ───────────────────────────────────────────
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    sessionStorage.removeItem("inbox_key");
    adminKeyInput.value = "";
    loginGate.style.display = "block";
    dashboardWrap.style.display = "none";
  });
}

// ── Helper: Show Login Error ─────────────────────────────────
function showLoginError(msg) {
  if (!loginError) return;
  if (msg) {
    loginError.textContent = msg;
    loginError.style.color = "#f87171";
    loginError.classList.add("show");
  } else {
    loginError.textContent = "";
    loginError.classList.remove("show");
  }
}

// ── Helper: Escape HTML to prevent XSS ───────────────────────
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
