/* ============================================
   FORMS.JS — Contact form handler
============================================ */

const BACKEND_URL = 'http://localhost:8000';

const contactForm = document.getElementById("contactForm");
const formSuccess = document.getElementById("formSuccess");

if (contactForm) {
  contactForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const name    = document.getElementById("name").value.trim();
    const email   = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();
    const btn     = contactForm.querySelector("button[type='submit']");

    // Client-side validation
    let valid = true;
    [['name', name], ['email', email], ['message', message]].forEach(([id, val]) => {
      const field = document.getElementById(id);
      if (!val) {
        field.style.borderBottomColor = "#f87171";
        field.addEventListener("input", () => {
          field.style.borderBottomColor = "";
        }, { once: true });
        valid = false;
      }
    });

    if (!valid) return;

    // Send to Django
    btn.textContent = "Sending...";
    btn.disabled = true;

    try {
      const res = await fetch(`${BACKEND_URL}/api/contact/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, message })
      });

      const data = await res.json();

      if (res.ok && data.success) {
        contactForm.reset();
        showMessage("Message sent! I'll be in touch soon.", "#4ade80");
      } else {
        const errMsg = data.error
          || Object.values(data.errors || {}).join(" ")
          || "Something went wrong. Try again.";
        showMessage(errMsg, "#f87171");
      }
    } catch (err) {
      showMessage("Could not reach server. Is Django running?", "#f87171");
    } finally {
      btn.textContent = "Send Message →";
      btn.disabled = false;
    }
  });
}

function showMessage(text, color) {
  if (!formSuccess) return;
  formSuccess.textContent = text;
  formSuccess.style.color = color;
  formSuccess.classList.add("show");
  setTimeout(() => formSuccess.classList.remove("show"), 5000);
}
