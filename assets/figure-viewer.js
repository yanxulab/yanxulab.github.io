/* Enhance figure links while preserving their original-image fallback. */
(() => {
  "use strict";

  const figures = [...document.querySelectorAll("a.work-image")];
  if (!figures.length || typeof HTMLDialogElement === "undefined" ||
      typeof HTMLDialogElement.prototype.showModal !== "function") return;

  const viewer = document.createElement("dialog");
  viewer.className = "figure-viewer";
  viewer.setAttribute("aria-labelledby", "figure-viewer-title");
  viewer.innerHTML = `
    <div class="figure-viewer-toolbar">
      <h2 id="figure-viewer-title"></h2>
      <div class="figure-viewer-controls">
        <button class="figure-viewer-zoom" type="button" aria-pressed="false">Zoom In</button>
        <a class="figure-viewer-original" target="_blank" rel="noopener">Open Original ↗</a>
        <button class="figure-viewer-close" type="button" aria-label="Close figure">×</button>
      </div>
    </div>
    <div class="figure-viewport" tabindex="0" role="region" aria-label="Figure preview; scroll to inspect when zoomed">
      <img class="figure-full-image" alt="">
    </div>`;
  document.body.append(viewer);

  const title = viewer.querySelector("h2");
  const image = viewer.querySelector("img");
  const viewport = viewer.querySelector(".figure-viewport");
  const zoom = viewer.querySelector(".figure-viewer-zoom");
  const original = viewer.querySelector(".figure-viewer-original");
  const close = viewer.querySelector(".figure-viewer-close");
  let trigger = null;

  function resetZoom() {
    viewer.removeAttribute("data-zoomed");
    zoom.setAttribute("aria-pressed", "false");
    zoom.textContent = "Zoom In";
    viewport.scrollTo(0, 0);
  }

  for (const figure of figures) {
    figure.setAttribute("aria-haspopup", "dialog");
    figure.addEventListener("click", (event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = figure;
      const thumbnail = figure.querySelector("img");
      title.textContent = figure.closest(".work-row").querySelector("h3").textContent;
      image.alt = thumbnail.alt;
      image.src = figure.href;
      original.href = figure.href;
      resetZoom();
      viewer.showModal();
      document.documentElement.classList.add("figure-preview-open");
      close.focus();
    });
  }

  zoom.addEventListener("click", () => {
    const zoomed = viewer.toggleAttribute("data-zoomed");
    zoom.setAttribute("aria-pressed", String(zoomed));
    zoom.textContent = zoomed ? "Fit to View" : "Zoom In";
    viewport.scrollTo(0, 0);
  });
  close.addEventListener("click", () => viewer.close());
  viewer.addEventListener("click", (event) => {
    const bounds = viewer.getBoundingClientRect();
    if (event.target === viewer && (event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom)) viewer.close();
  });
  viewer.addEventListener("close", () => {
    document.documentElement.classList.remove("figure-preview-open");
    resetZoom();
    image.removeAttribute("src");
    if (trigger?.isConnected) trigger.focus({preventScroll: true});
  });
})();
