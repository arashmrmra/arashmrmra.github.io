(() => {
  const key = "ordinary-blog-theme";
  const button = document.querySelector("#theme-toggle");
  let saved = null;
  try { saved = localStorage.getItem(key); } catch (_) {}
  if (saved === "light") document.body.classList.add("light");
  if (!button) return;
  button.addEventListener("click", () => {
    document.body.classList.toggle("light");
    try { localStorage.setItem(key, document.body.classList.contains("light") ? "light" : "dark"); } catch (_) {}
  });
})();
