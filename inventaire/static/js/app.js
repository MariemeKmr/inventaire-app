(function(){
  document.querySelectorAll(".toast").forEach(t => new bootstrap.Toast(t).show());
  document.addEventListener("keydown", (e) => {
    if (e.target.matches("input, textarea")) return;
    if (e.key === "/") { e.preventDefault(); document.getElementById("globalSearch")?.focus(); }
  });
})();
