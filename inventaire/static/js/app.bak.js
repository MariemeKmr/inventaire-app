/* --- toasts + raccourci recherche --- */
(function(){
  document.querySelectorAll(".toast").forEach(t => new bootstrap.Toast(t).show());
  document.addEventListener("keydown", (e) => {
    if (e.target.matches("input, textarea")) return;
    if (e.key === "/") { e.preventDefault(); document.getElementById("globalSearch")?.focus(); }
  });
})();

/* --- thème clair/sombre --- */
(function(){
  const root = document.documentElement;
  const key  = "theme";
  const btn  = document.getElementById("themeToggle");
  function apply(theme){
    if(!theme){
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      theme = prefersDark ? "dark" : "light";
    }
    root.setAttribute("data-theme", theme);
    root.setAttribute("data-bs-theme", theme);
    if(btn){
      const i = btn.querySelector("i");
      if(i) i.className = theme === "dark" ? "fa-solid fa-sun" : "fa-solid fa-moon";
      btn.setAttribute("title", theme === "dark" ? "Mode clair" : "Mode sombre");
    }
  }
  apply(localStorage.getItem(key));
  btn?.addEventListener("click", () => {
    const next = (root.getAttribute("data-theme") === "dark") ? "light" : "dark";
    localStorage.setItem(key, next); apply(next);
  });
})();

/* --- sidebar: étendre au survol (pousse le contenu) --- */
(function(){
  const sb = document.querySelector(".app-sidebar");
  if(!sb) return;
  const on = () => document.body.classList.add("sb-expanded");
  const off = () => document.body.classList.remove("sb-expanded");
  sb.addEventListener("mouseenter", on);
  sb.addEventListener("mouseleave", off);
})();
