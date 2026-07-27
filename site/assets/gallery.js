(() => {
  "use strict";

  const PAGE_SIZE = 180;
  const root = document.querySelector("#app");
  const cards = Array.from(document.querySelectorAll("[data-icon-card]"));
  const search = document.querySelector("#icon-search");
  const clearSearch = document.querySelector("#clear-search");
  const copyMode = document.querySelector("#copy-mode");
  const count = document.querySelector("#visible-count");
  const empty = document.querySelector("#empty-state");
  const loadMore = document.querySelector("#load-more");
  const toast = document.querySelector("#copy-toast");
  const categoryButtons = Array.from(document.querySelectorAll("[data-category]"));

  let activeCategory = "All";
  let visibleLimit = PAGE_SIZE;
  let toastTimer;

  const normalized = (value) =>
    value.toLowerCase().trim().replace(/[\s_]+/g, "-");

  const filteredCards = () => {
    const query = normalized(search.value);
    return cards.filter((card) => {
      const categoryMatches =
        activeCategory === "All" || card.dataset.categoryName === activeCategory;
      const queryMatches =
        !query || normalized(card.dataset.search || "").includes(query);
      return categoryMatches && queryMatches;
    });
  };

  const updateUrl = () => {
    const params = new URLSearchParams();
    if (search.value.trim()) params.set("q", search.value.trim());
    if (activeCategory !== "All") params.set("category", activeCategory);
    const query = params.toString();
    history.replaceState(null, "", query ? `?${query}` : location.pathname);
  };

  const applyFilters = () => {
    const matches = filteredCards();
    const visible = Math.min(visibleLimit, matches.length);
    const matchSet = new Set(matches.slice(0, visible));

    cards.forEach((card) => {
      card.hidden = !matchSet.has(card);
    });

    count.textContent =
      matches.length === cards.length
        ? `Showing ${visible.toLocaleString()} of ${cards.length.toLocaleString()} icons`
        : `${matches.length.toLocaleString()} icon${matches.length === 1 ? "" : "s"} found`;
    empty.hidden = matches.length !== 0;
    loadMore.hidden = visible >= matches.length;
    clearSearch.hidden = !search.value;
    updateUrl();
  };

  const setCategory = (category) => {
    activeCategory = category;
    visibleLimit = PAGE_SIZE;
    categoryButtons.forEach((button) => {
      const active = button.dataset.category === category;
      button.classList.toggle("is-active", active);
      button.classList.toggle("uipr-button-primary", active);
      button.classList.toggle("uipr-button-outline", !active);
      button.setAttribute("aria-pressed", String(active));
    });
    applyFilters();
  };

  const showToast = (message = "Copied to clipboard") => {
    toast.querySelector("span").textContent = message;
    toast.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 1800);
  };

  const copyText = async (value, button) => {
    try {
      await navigator.clipboard.writeText(value);
    } catch {
      const helper = document.createElement("textarea");
      helper.value = value;
      helper.style.position = "fixed";
      helper.style.opacity = "0";
      document.body.appendChild(helper);
      helper.select();
      document.execCommand("copy");
      helper.remove();
    }

    const label = button.querySelector("span");
    const previous = label?.textContent;
    if (label) label.textContent = "Copied";
    showToast();
    setTimeout(() => {
      if (label) label.textContent = previous || "Copy";
    }, 1200);
  };

  search.addEventListener("input", () => {
    visibleLimit = PAGE_SIZE;
    applyFilters();
  });

  clearSearch.addEventListener("click", () => {
    search.value = "";
    search.focus();
    visibleLimit = PAGE_SIZE;
    applyFilters();
  });

  categoryButtons.forEach((button) => {
    button.addEventListener("click", () => setCategory(button.dataset.category));
  });

  copyMode.addEventListener("change", () => {
    localStorage.setItem("6cons-copy-mode", copyMode.value);
  });

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-copy-button], [data-copy-value]");
    if (!button) return;

    const value =
      button.dataset.copyValue ||
      button.dataset[
        `copy${copyMode.value.charAt(0).toUpperCase()}${copyMode.value.slice(1)}`
      ];
    if (value) copyText(value, button);
  });

  loadMore.addEventListener("click", () => {
    visibleLimit += PAGE_SIZE;
    applyFilters();
  });

  document.querySelector("#empty-clear").addEventListener("click", () => {
    search.value = "";
    setCategory("All");
    search.focus();
  });

  document.addEventListener("keydown", (event) => {
    const editing = /input|textarea|select/i.test(document.activeElement?.tagName);
    if (event.key === "/" && !editing) {
      event.preventDefault();
      search.focus();
    }
    if (event.key === "Escape" && document.activeElement === search) {
      search.value = "";
      applyFilters();
      search.blur();
    }
  });

  const themeToggle = document.querySelector("#theme-toggle");
  const setTheme = (theme) => {
    root.dataset.uiprTheme = theme;
    root.dataset.uiprColorMode = theme;
    themeToggle.setAttribute("aria-label", `Switch to ${theme === "dark" ? "light" : "dark"} theme`);
    localStorage.setItem("6cons-theme", theme);
  };

  themeToggle.addEventListener("click", () => {
    setTheme(root.dataset.uiprTheme === "dark" ? "light" : "dark");
  });

  const params = new URLSearchParams(location.search);
  search.value = params.get("q") || "";
  const requestedCategory = params.get("category");
  if (requestedCategory && categoryButtons.some((button) => button.dataset.category === requestedCategory)) {
    activeCategory = requestedCategory;
  }

  copyMode.value = localStorage.getItem("6cons-copy-mode") || "component";
  const preferredTheme =
    localStorage.getItem("6cons-theme") ||
    (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  setTheme(preferredTheme);
  setCategory(activeCategory);
})();
