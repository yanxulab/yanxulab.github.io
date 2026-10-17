/* Small, progressively enhanced interactions. The content is rendered at build time. */
(() => {
  "use strict";

  for (const demo of document.querySelectorAll("[data-temperature-demo]")) {
    const slider = demo.querySelector("input[type='range']");
    const output = demo.querySelector("output");
    const rows = [...demo.querySelectorAll(".probability-row")];
    const logits = [2.0, 1.2, 0.4, -0.1];
    function update() {
      const temperature = Number(slider.value);
      const peak = Math.max(...logits);
      const weights = logits.map((value) => Math.exp((value - peak) / temperature));
      const total = weights.reduce((sum, value) => sum + value, 0);
      const labels = [];
      rows.forEach((row, index) => {
        const percent = ((weights[index] / total) * 100).toFixed(1);
        row.querySelector(".bar-fill").style.width = `${percent}%`;
        row.querySelector(".probability-value").textContent = `${percent}%`;
        labels.push(`${row.querySelector(".token-label").textContent} ${percent}%`);
      });
      output.value = temperature.toFixed(1);
      slider.setAttribute("aria-valuetext", `${temperature.toFixed(1)}; ${labels.join(", ")}`);
      demo.querySelector(".probability-bars").setAttribute("aria-label", `Illustrative next-token probabilities at temperature ${temperature.toFixed(1)}: ${labels.join(", ")}.`);
    }
    slider.disabled = false;
    slider.addEventListener("input", update);
    update();
  }

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  for (const media of document.querySelectorAll("[data-work-media]")) {
    const video = media.querySelector("[data-work-video]");
    const panels = [...media.querySelectorAll("[data-media-panel]")];
    const choices = [...media.querySelectorAll("[data-media-choice]")];
    const note = media.querySelector(".media-note");
    let selected = "preview";
    let visible = false;
    let userPaused = false;
    let internalPause = false;

    function stop() {
      if (!video.paused) {
        internalPause = true;
        video.pause();
      }
    }
    function shouldPlay() {
      return selected === "preview" && visible && !document.hidden &&
        !reducedMotion.matches && !navigator.connection?.saveData && !userPaused;
    }
    function sync() {
      if (!shouldPlay()) return stop();
      video.play().then(() => { if (!shouldPlay()) stop(); }).catch(() => {});
    }
    function choose(value) {
      selected = value;
      for (const panel of panels) panel.hidden = panel.dataset.mediaPanel !== value;
      for (const choice of choices) choice.setAttribute("aria-pressed", String(choice.dataset.mediaChoice === value));
      note.hidden = value !== "preview";
      sync();
    }

    video.muted = true;
    video.addEventListener("play", () => { userPaused = false; });
    video.addEventListener("pause", () => {
      if (internalPause) internalPause = false;
      else userPaused = true;
    });
    video.addEventListener("error", () => {
      choose("method");
      media.querySelector('[data-media-choice="preview"]').disabled = true;
    });
    for (const choice of choices) {
      choice.addEventListener("click", () => choose(choice.dataset.mediaChoice));
    }
    media.querySelector(".media-switch").hidden = false;
    choose("preview");
    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting && entry.intersectionRatio >= 0.35;
        sync();
      }, {threshold: [0, 0.35]});
      observer.observe(media);
    }
    reducedMotion.addEventListener("change", sync);
    document.addEventListener("visibilitychange", sync);
  }

})();
