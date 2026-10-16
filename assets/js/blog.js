(() => {
  const search = document.querySelector("#post-search");
  const buttons = [...document.querySelectorAll("[data-category-filter]")];
  const cards = [...document.querySelectorAll("[data-post-card]")];
  const empty = document.querySelector("#empty-state");
  if (!cards.length) return;
  let activeCategory = buttons.find(button => button.classList.contains("active"))?.dataset.categoryFilter || buttons[0]?.dataset.categoryFilter || "";
  const apply = () => {
    const query = (search?.value || "").trim().toLocaleLowerCase("fa");
    let shown = 0;
    cards.forEach(card => {
      const category = card.dataset.category || "";
      const haystack = (card.dataset.search || card.textContent).toLocaleLowerCase("fa");
      const visible = (!activeCategory || activeCategory === "همه" || activeCategory === "All" || category === activeCategory) && haystack.includes(query);
      card.hidden = !visible;
      if (visible) shown++;
    });
    if (empty) empty.hidden = shown !== 0;
  };
  buttons.forEach(button => button.addEventListener("click", () => {
    activeCategory = button.dataset.categoryFilter;
    buttons.forEach(item => {
      const active = item === button;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    apply();
  }));
  search?.addEventListener("input", apply);
  apply();
})();
