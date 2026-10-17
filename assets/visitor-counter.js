/* Production-only cumulative visitor count; the welcome text is the fallback. */
(() => {
  "use strict";

  const welcome = document.querySelector("[data-visitor-welcome]");
  if (!welcome || !["yanxu.io", "www.yanxu.io"].includes(location.hostname)) return;

  const callback = `yanxuVisitorCount_${Date.now()}_${Math.floor(Math.random() * 1e6)}`;
  const request = document.createElement("script");
  let settled = false;
  const timeout = window.setTimeout(() => finish(), 8000);

  function finish(data) {
    if (settled) return;
    settled = true;
    window.clearTimeout(timeout);
    const count = Number(data?.site_uv);
    if (Number.isSafeInteger(count) && count > 0) {
      const number = new Intl.NumberFormat("en-US").format(count);
      welcome.textContent = `Welcome — ${number} ${count === 1 ? "visitor" : "visitors"} and counting.`;
      welcome.title = "Approximate cumulative visitor count since tracking was enabled.";
    }
    request.remove();
    // A late JSONP response after timeout can safely call this no-op.
    window[callback] = () => {};
  }

  window[callback] = finish;
  request.async = true;
  request.referrerPolicy = "origin";
  request.src = `https://busuanzi.ibruce.info/busuanzi?jsonpCallback=${callback}`;
  request.addEventListener("error", () => finish(), {once: true});
  document.head.append(request);
})();
