/* ============================================
   MAIN.JS — Elba Ouma Portfolio
============================================ */

/* ─── Custom Cursor ─────────────────────── */
const cursor = document.getElementById("cursor");
if (cursor) {
  document.addEventListener("mousemove", e => {
    cursor.style.top  = e.clientY + "px";
    cursor.style.left = e.clientX + "px";
  });
  document.querySelectorAll("a, button, .project-card, .skill-block").forEach(el => {
    el.addEventListener("mouseenter", () => cursor.classList.add("expand"));
    el.addEventListener("mouseleave", () => cursor.classList.remove("expand"));
  });
}

/* ─── Hamburger Menu ────────────────────── */
const hamburger = document.getElementById("hamburger");
const navList   = document.querySelector(".navbar ul");
if (hamburger && navList) {
  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("open");
    navList.classList.toggle("open");
  });
  // close on nav link click
  navList.querySelectorAll("a").forEach(a => {
    a.addEventListener("click", () => {
      hamburger.classList.remove("open");
      navList.classList.remove("open");
    });
  });
}

/* ─── Typing Effect (index only) ────────── */
const typingEl = document.getElementById("typing");
if (typingEl) {
  const phrases = ["Backend Engineer.", "Django Developer.", "React Integration.", "Systems Builder."];
  let phraseIdx = 0, charIdx = 0, deleting = false;

  function type() {
    const phrase = phrases[phraseIdx];
    typingEl.textContent = deleting
      ? phrase.slice(0, charIdx--)
      : phrase.slice(0, charIdx++);

    if (!deleting && charIdx === phrase.length + 1) {
      deleting = true;
      setTimeout(type, 1800);
      return;
    }
    if (deleting && charIdx === 0) {
      deleting = false;
      phraseIdx = (phraseIdx + 1) % phrases.length;
      setTimeout(type, 400);
      return;
    }
    setTimeout(type, deleting ? 45 : 85);
  }
  type();
}

/* ─── Scroll Fade-Up ────────────────────── */
const fadeEls = document.querySelectorAll(".fade-up");
if (fadeEls.length) {
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  fadeEls.forEach(el => observer.observe(el));
}

/* ─── Active nav link highlight ─────────── */
const currentPage = location.pathname.split("/").pop() || "index.html";
document.querySelectorAll(".navbar ul li a").forEach(a => {
  const href = a.getAttribute("href");
  if (href === currentPage) a.classList.add("active");
});

/* Theme picker */
const themeButtons = document.querySelectorAll(".theme-swatch");
const savedTheme = localStorage.getItem("portfolio-theme") || "neon";
document.body.dataset.theme = savedTheme;

function markTheme(theme) {
  themeButtons.forEach(button => {
    button.classList.toggle("active", button.dataset.theme === theme);
  });
}

markTheme(savedTheme);

themeButtons.forEach(button => {
  button.addEventListener("click", () => {
    const theme = button.dataset.theme;
    document.body.dataset.theme = theme;
    localStorage.setItem("portfolio-theme", theme);
    markTheme(theme);
  });
});

