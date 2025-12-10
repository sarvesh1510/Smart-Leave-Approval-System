document.addEventListener("DOMContentLoaded", () => {
  console.log("Smart Leave Assistant — UI ready ✨");

  // Animate toasts if present (some simple fade/slide)
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach(t => {
    t.style.opacity = 0;
    setTimeout(() => { t.style.transition = 'opacity .4s'; t.style.opacity = 1; }, 50);
  });

  // small accessibility: focus first input on login/register pages
  const firstInput = document.querySelector('form input, form textarea, form select');
  if (firstInput) firstInput.focus();

  // if Chart.js exists, ensure default font color for dark theme
  if (window.Chart) {
    Chart.defaults.font.family = "'Inter', -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial";
    Chart.defaults.color = '#cbd5e1';
  }
});
