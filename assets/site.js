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

})();
