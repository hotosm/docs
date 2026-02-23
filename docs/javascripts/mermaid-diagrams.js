(() => {
  const MERMAID_URL =
    "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  const SVG_PAN_ZOOM_URL =
    "https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.2/dist/svg-pan-zoom.min.js";

  let renderInFlight = null;
  let mermaidApi = null;
  let panZoomReady = null;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[src="${src}"]`);
      if (existing) {
        if (existing.dataset.loaded === "true") {
          resolve();
          return;
        }
        existing.addEventListener("load", () => resolve(), { once: true });
        existing.addEventListener("error", reject, { once: true });
        return;
      }
      const script = document.createElement("script");
      script.src = src;
      script.async = true;
      script.addEventListener(
        "load",
        () => {
          script.dataset.loaded = "true";
          resolve();
        },
        { once: true },
      );
      script.addEventListener("error", reject, { once: true });
      document.head.appendChild(script);
    });
  }

  async function ensureMermaid() {
    if (mermaidApi) {
      return mermaidApi;
    }
    const module = await import(MERMAID_URL);
    mermaidApi = module.default;
    mermaidApi.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      flowchart: {
        htmlLabels: true,
        useMaxWidth: false,
        nodeSpacing: 40,
        rankSpacing: 70,
      },
      theme: "default",
    });
    window.mermaid = mermaidApi;
    return mermaidApi;
  }

  async function ensurePanZoom() {
    if (window.svgPanZoom) {
      return window.svgPanZoom;
    }
    if (!panZoomReady) {
      panZoomReady = loadScript(SVG_PAN_ZOOM_URL).then(() => window.svgPanZoom);
    }
    return panZoomReady;
  }

  async function renderMermaidBlocks() {
    const sourceBlocks = document.querySelectorAll(
      "pre.mermaid-source, div.mermaid-source",
    );
    if (!sourceBlocks.length) {
      return;
    }

    const mermaid = await ensureMermaid();
    const svgPanZoom = await ensurePanZoom();

    for (const block of sourceBlocks) {
      const code = block.querySelector("code");
      if (!code) {
        continue;
      }

      const source = code.textContent || "";
      const id =
        "mermaid-diagram-" +
        Math.random().toString(36).slice(2, 10) +
        Date.now().toString(36);
      const viewport = document.createElement("div");
      viewport.className = "mermaid-viewport";

      const diagram = document.createElement("div");
      diagram.className = "mermaid-diagram";
      viewport.appendChild(diagram);
      block.replaceWith(viewport);

      try {
        const { svg } = await mermaid.render(id, source);
        diagram.innerHTML = svg;
        const svgElement = diagram.querySelector("svg");
        if (svgElement) {
          for (const image of svgElement.querySelectorAll("image")) {
            image.setAttribute("preserveAspectRatio", "xMidYMid meet");
          }
          const viewBox = svgElement.getAttribute("viewBox");
          if (viewBox) {
            const parts = viewBox.split(/\s+/).map((value) => Number(value));
            if (parts.length === 4) {
              const width = parts[2];
              const height = parts[3];
              if (width > 0 && height > 0) {
                viewport.style.aspectRatio = `${width} / ${height}`;
              }
            }
          }
        }
        if (svgElement && svgPanZoom) {
          const panZoom = svgPanZoom(svgElement, {
            zoomEnabled: true,
            controlIconsEnabled: true,
            fit: true,
            center: true,
            minZoom: 0.3,
            maxZoom: 8,
          });
          panZoom.resize();
          panZoom.fit();
          panZoom.center();
        }
      } catch (error) {
        diagram.innerHTML = `<pre>${String(error)}</pre>`;
      }
    }
  }

  async function renderAll() {
    if (renderInFlight) {
      await renderInFlight;
      return;
    }
    renderInFlight = renderMermaidBlocks().finally(() => {
      renderInFlight = null;
    });
    await renderInFlight;
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(() => {
      void renderAll();
    });
  } else {
    document.addEventListener("DOMContentLoaded", () => {
      void renderAll();
    });
  }
})();
