// Experimental docs assistant widget. Backend: chat/ in this repo.
(() => {
  const API_URL =
    window.HOT_CHAT_API_URL ||
    (["localhost", "127.0.0.1"].includes(location.hostname)
      ? "http://localhost:8000"
      : "https://docs-chat.k8s-prod.hotosm.org");
  const STORE_KEY = "hot-docs-chat";
  const PLAN_HINT =
    /\b(how (can|could|do|should) (i|we)|i need to|we need to|we want to|i want to)\b.*\b(map|collect|survey|record|digiti[sz]e)\b/i;

  // Survives Material's instant navigation; sessionStorage survives reloads.
  const state = load() || {
    open: false,
    messages: [], // {role, content, sources?, plan?, grounded?}
    planAnswers: null,
    planning: null, // answers in progress
  };
  let root,
    log,
    input,
    sendBtn,
    stopBtn,
    busy = false,
    controller = null;

  function load() {
    try {
      return JSON.parse(sessionStorage.getItem(STORE_KEY));
    } catch {
      return null;
    }
  }
  function save() {
    try {
      sessionStorage.setItem(STORE_KEY, JSON.stringify(state));
    } catch {
      /* storage unavailable */
    }
  }

  const el = (tag, attrs = {}, ...children) => {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") node.className = v;
      else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
      else node.setAttribute(k, v);
    }
    for (const c of children.flat()) {
      if (c != null)
        node.append(c instanceof Node ? c : document.createTextNode(c));
    }
    return node;
  };

  // Escape model output before rendering Markdown
  function escapeHtml(s) {
    return s.replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  }
  function inline(s, sources) {
    return s
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<em>$2</em>")
      .replace(
        /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
        '<a href="$2" target="_blank" rel="noopener">$1</a>',
      )
      .replace(
        /(^|[\s(])(https?:\/\/[^\s)<]+[^\s)<.,;:!?])/g,
        '$1<a href="$2" target="_blank" rel="noopener">$2</a>',
      )
      .replace(/\[(\d{1,2})\]/g, (m, n) => {
        const src = sources && sources[Number(n) - 1];
        return src
          ? `<sup class="hdc-cite"><a href="${escapeHtml(src.url)}" target="_blank" rel="noopener" title="${escapeHtml(src.title)}">${n}</a></sup>`
          : m;
      });
  }
  function renderMarkdown(text, sources) {
    const out = [];
    const blocks = escapeHtml(text).split(/```/);
    blocks.forEach((block, i) => {
      if (i % 2) {
        out.push(`<pre><code>${block.replace(/^\w*\n/, "")}</code></pre>`);
        return;
      }
      let list = null;
      for (const raw of block.split("\n")) {
        const line = raw.trimEnd();
        const li = line.match(/^\s*(?:[-*]|\d+[.)])\s+(.*)/);
        if (li) {
          const type = /^\s*\d/.test(line) ? "ol" : "ul";
          if (list !== type) {
            if (list) out.push(`</${list}>`);
            out.push(`<${type}>`);
            list = type;
          }
          out.push(`<li>${inline(li[1], sources)}</li>`);
          continue;
        }
        if (list) {
          out.push(`</${list}>`);
          list = null;
        }
        if (!line.trim()) continue;
        const h = line.match(/^#{1,6}\s+(.*)/);
        out.push(
          h
            ? `<p><strong>${inline(h[1], sources)}</strong></p>`
            : `<p>${inline(line, sources)}</p>`,
        );
      }
      if (list) out.push(`</${list}>`);
    });
    return out.join("");
  }

  // --- Rendering -----------------------------------------------------------

  function build() {
    log = el("div", { class: "hdc-log", role: "log", "aria-live": "polite" });
    input = el("textarea", {
      class: "hdc-input",
      rows: "1",
      placeholder: "Ask about HOT's mapping tools…",
      "aria-label": "Your question",
      onkeydown: (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          send();
        }
      },
      oninput: () => {
        input.style.height = "auto";
        input.style.height = Math.min(input.scrollHeight, 120) + "px";
      },
    });
    sendBtn = el(
      "button",
      {
        class: "hdc-send",
        type: "button",
        "aria-label": "Send",
        onclick: () => send(),
      },
      "➤",
    );
    stopBtn = el(
      "button",
      {
        class: "hdc-stop",
        type: "button",
        hidden: "",
        onclick: () => controller && controller.abort(),
      },
      "Stop",
    );

    const panel = el(
      "section",
      { class: "hdc-panel", role: "dialog", "aria-label": "HOTOSM Assistant" },
      el(
        "header",
        { class: "hdc-header" },
        el(
          "span",
          { class: "hdc-title" },
          "HOTOSM Assistant",
          el("span", { class: "hdc-badge" }, "Experimental"),
        ),
        el(
          "button",
          {
            class: "hdc-icon",
            type: "button",
            title: "New chat",
            "aria-label": "New chat",
            onclick: reset,
          },
          "↺",
        ),
        el(
          "button",
          {
            class: "hdc-icon",
            type: "button",
            title: "Close",
            "aria-label": "Close",
            onclick: () => toggle(false),
          },
          "✕",
        ),
      ),
      el(
        "p",
        { class: "hdc-disclaimer" },
        "Runs on a small self-hosted AI model, so answers can be slow and may be wrong. Always check the linked sources.",
      ),
      log,
      el("div", { class: "hdc-composer" }, input, stopBtn, sendBtn),
    );
    const launcher = el(
      "button",
      {
        class: "hdc-launcher",
        type: "button",
        "aria-label": "Open docs assistant",
        onclick: () => toggle(),
      },
      el("span", { "aria-hidden": "true" }, "💬"),
      " Ask the docs",
      el("span", { class: "hdc-badge" }, "Beta"),
    );
    root = el("div", { class: "hdc-root" }, panel, launcher);
    root.addEventListener(
      "keydown",
      (e) => e.key === "Escape" && toggle(false),
    );
    renderAll();
  }

  function toggle(force) {
    state.open = force ?? !state.open;
    root.classList.toggle("hdc-open", state.open);
    save();
    if (state.open) setTimeout(() => input.focus(), 50);
  }

  function reset() {
    if (controller) controller.abort();
    Object.assign(state, { messages: [], planAnswers: null, planning: null });
    save();
    renderAll();
  }

  function scroll() {
    log.scrollTop = log.scrollHeight;
  }

  function renderAll() {
    log.replaceChildren();
    root.classList.toggle("hdc-open", state.open);
    if (!state.messages.length && !state.planning) {
      log.append(
        el(
          "div",
          { class: "hdc-msg hdc-assistant" },
          el(
            "div",
            { class: "hdc-bubble" },
            el(
              "p",
              {},
              "Hi! I can answer questions using HOT's tool documentation, or help you work out which tools you need for a mapping project.",
            ),
            el(
              "div",
              { class: "hdc-actions" },
              el(
                "button",
                {
                  class: "hdc-chip hdc-primary",
                  type: "button",
                  onclick: () => startPlan(),
                },
                "🗺️ Plan a mapping project",
              ),
              ...[
                "How do I collect data with ChatMap?",
                "What's the difference between Tasking Manager and Field-TM?",
              ].map((q) =>
                el(
                  "button",
                  { class: "hdc-chip", type: "button", onclick: () => send(q) },
                  q,
                ),
              ),
            ),
          ),
        ),
      );
    }
    state.messages.forEach((m, i) => log.append(renderMessage(m, i)));
    if (state.planning) renderPlanStep();
    scroll();
  }

  function renderMessage(m, i) {
    if (m.role === "user") {
      return el(
        "div",
        { class: "hdc-msg hdc-user", "data-idx": i },
        el("div", { class: "hdc-bubble" }, m.content),
      );
    }
    const bubble = el("div", { class: "hdc-bubble" });
    if (m.plan) bubble.append(renderPlan(m.plan));
    const body = el("div", { class: "hdc-body" });
    body.innerHTML = renderMarkdown(m.content || "", m.sources);
    bubble.append(body);
    if (m.status)
      bubble.append(
        el(
          "div",
          { class: "hdc-status" },
          el("span", { class: "hdc-dots" }),
          m.status,
        ),
      );
    if (m.error) bubble.append(el("p", { class: "hdc-error" }, m.error));
    if (m.sources && m.sources.length && !m.status) {
      bubble.append(
        el(
          "details",
          { class: "hdc-sources" },
          el("summary", {}, `Sources (${m.sources.length})`),
          el(
            "ol",
            {},
            m.sources.map((s) =>
              el(
                "li",
                {},
                el(
                  "a",
                  { href: s.url, target: "_blank", rel: "noopener" },
                  s.heading ? `${s.title}: ${s.heading}` : s.title,
                ),
                ` (${s.source})`,
              ),
            ),
          ),
        ),
      );
    }
    if (m.done && m.content) {
      bubble.append(
        el(
          "div",
          { class: "hdc-feedback" },
          m.rated
            ? el("span", {}, "Thanks for the feedback!")
            : [
                el("span", {}, "Helpful?"),
                el(
                  "button",
                  {
                    type: "button",
                    "aria-label": "Helpful",
                    onclick: () => rate(i, "up"),
                  },
                  "👍",
                ),
                el(
                  "button",
                  {
                    type: "button",
                    "aria-label": "Not helpful",
                    onclick: () => rate(i, "down"),
                  },
                  "👎",
                ),
              ],
        ),
      );
    }
    if (m.suggestPlan && !state.planAnswers) {
      bubble.append(
        el(
          "div",
          { class: "hdc-actions" },
          el(
            "button",
            {
              class: "hdc-chip hdc-primary",
              type: "button",
              onclick: () => startPlan(m.suggestPlan),
            },
            "🗺️ Get a tailored tool recommendation",
          ),
        ),
      );
    }
    return el("div", { class: "hdc-msg hdc-assistant", "data-idx": i }, bubble);
  }

  function renderPlan(plan) {
    return el(
      "div",
      { class: "hdc-plan" },
      el("p", { class: "hdc-plan-scope" }, plan.scope),
      plan.stages.map((s) =>
        el(
          "div",
          { class: "hdc-stage" },
          el("p", { class: "hdc-stage-label" }, s.label),
          s.tools.map((t) =>
            el(
              "div",
              { class: "hdc-tool" },
              el(
                "a",
                { href: t.url, target: "_blank", rel: "noopener" },
                t.name,
              ),
              el("p", {}, t.reasons.join(" ")),
            ),
          ),
        ),
      ),
      plan.notes.length
        ? el(
            "ul",
            { class: "hdc-notes" },
            plan.notes.map((n) => el("li", {}, n)),
          )
        : null,
    );
  }

  // --- Planner -------------------------------------------------------------

  async function startPlan(goal) {
    state.planning = goal ? { goal } : {};
    save();
    await renderPlanStep();
  }

  async function renderPlanStep() {
    const step = el(
      "div",
      { class: "hdc-msg hdc-assistant hdc-planstep" },
      el("div", { class: "hdc-bubble" }, el("span", { class: "hdc-dots" })),
    );
    log.querySelectorAll(".hdc-planstep").forEach((n) => n.remove());
    log.append(step);
    scroll();
    let res;
    try {
      res = await api("/api/plan/next", { answers: state.planning });
    } catch (e) {
      step.firstChild.replaceChildren(
        el("p", { class: "hdc-error" }, e.message),
      );
      return;
    }
    if (res.plan) {
      step.remove();
      finishPlan(res.plan);
      return;
    }
    const q = res.question;
    const answer = (value, label) => {
      state.planning[q.id] = value;
      state.messages.push({ role: "user", content: label, planStep: true });
      save();
      log.insertBefore(
        renderMessage(state.messages.at(-1), state.messages.length - 1),
        step,
      );
      renderPlanStep();
    };
    const bubble = el(
      "div",
      { class: "hdc-bubble" },
      el("p", {}, el("strong", {}, `Question ${res.answered + 1}: `), q.text),
    );
    if (q.type === "text") {
      const field = el("input", {
        class: "hdc-text",
        type: "text",
        placeholder: q.placeholder || "",
        "aria-label": q.text,
      });
      const submit = () =>
        field.value.trim() && answer(field.value.trim(), field.value.trim());
      field.addEventListener("keydown", (e) => e.key === "Enter" && submit());
      bubble.append(
        el(
          "div",
          { class: "hdc-actions" },
          field,
          el(
            "button",
            { class: "hdc-chip hdc-primary", type: "button", onclick: submit },
            "Next",
          ),
        ),
      );
      setTimeout(() => field.focus(), 50);
    } else {
      bubble.append(
        el(
          "div",
          { class: "hdc-actions hdc-options" },
          q.options.map((o) =>
            el(
              "button",
              {
                class: "hdc-chip",
                type: "button",
                onclick: () => answer(o.value, o.label),
              },
              o.label,
            ),
          ),
        ),
      );
    }
    bubble.append(
      el(
        "button",
        {
          class: "hdc-link",
          type: "button",
          onclick: () => {
            state.planning = null;
            save();
            renderAll();
          },
        },
        "Cancel planning",
      ),
    );
    step.replaceChildren(bubble);
    scroll();
  }

  function finishPlan(plan) {
    state.planAnswers = state.planning;
    state.planning = null;
    // Collapse planner Q&A after showing the result
    state.messages = state.messages.filter((m) => !m.planStep);
    state.messages.push({ role: "assistant", content: "", plan, done: false });
    save();
    renderAll();
    stream(
      { messages: [], plan_answers: state.planAnswers },
      state.messages.length - 1,
    );
  }

  // --- Chat ----------------------------------------------------------------

  async function api(path, body) {
    const r = await fetch(API_URL + path, {
      method: body ? "POST" : "GET",
      headers: body ? { "Content-Type": "application/json" } : {},
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!r.ok) {
      const detail = await r.json().catch(() => ({}));
      throw new Error(detail.detail || `Request failed (${r.status})`);
    }
    return r.json();
  }

  function send(text) {
    text = (text ?? input.value).trim();
    if (!text || busy) return;
    input.value = "";
    input.style.height = "auto";
    if (state.planning) state.planning = null;
    state.messages.push({ role: "user", content: text });
    const firstQuestion =
      state.messages.filter((m) => m.role === "user" && !m.planStep).length ===
      1;
    state.messages.push({
      role: "assistant",
      content: "",
      suggestPlan: firstQuestion && PLAN_HINT.test(text) ? text : null,
    });
    save();
    renderAll();
    const history = state.messages
      .slice(0, -1)
      .filter((m) => m.content && !m.planStep && !m.error)
      .map((m) => ({ role: m.role, content: m.content.slice(0, 4000) }))
      .slice(-12);
    stream(
      { messages: history, plan_answers: state.planAnswers },
      state.messages.length - 1,
    );
  }

  function setBusy(on) {
    busy = on;
    sendBtn.disabled = on;
    stopBtn.hidden = !on;
  }

  async function stream(body, idx) {
    const msg = state.messages[idx];
    const update = () => {
      const old = log.querySelector(`[data-idx="${idx}"]`);
      if (old) old.replaceWith(renderMessage(msg, idx));
      scroll();
    };
    const started = Date.now();
    const timer = setInterval(() => {
      if (msg.status && msg.stage === "thinking" && !msg.content) {
        const s = Math.round((Date.now() - started) / 1000);
        msg.status = `Thinking… ${s}s (this may take some time)`;
        update();
      }
    }, 1000);
    controller = new AbortController();
    setBusy(true);
    msg.status = "Searching the docs…";
    update();
    try {
      const r = await fetch(API_URL + "/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal: controller.signal,
      });
      if (!r.ok) {
        const detail = await r.json().catch(() => ({}));
        throw new Error(detail.detail || `Request failed (${r.status})`);
      }
      const reader = r.body.getReader();
      const decoder = new TextDecoder();
      let buf = "";
      let lastPaint = 0;
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        let sep;
        while ((sep = buf.indexOf("\n\n")) >= 0) {
          const raw = buf.slice(0, sep);
          buf = buf.slice(sep + 2);
          const event = (raw.match(/^event: (.*)$/m) || [])[1];
          const data = JSON.parse(
            (raw.match(/^data: (.*)$/m) || [])[1] || "null",
          );
          if (event === "status") {
            msg.stage = data.stage;
            msg.status =
              data.stage === "queued"
                ? `Other people are asking too, you're number ${data.position} in the queue…`
                : data.stage === "thinking"
                  ? "Thinking… (this may take some time)"
                  : "Searching the docs…";
          } else if (event === "sources") {
            msg.sources = data;
          } else if (event === "token") {
            msg.status = null;
            msg.content += data.t;
          } else if (event === "error") {
            msg.error = data.message;
          } else if (event === "done") {
            msg.grounded = data.grounded;
          }
        }
        // Limit streaming repaints to ~10 per second
        if (Date.now() - lastPaint > 100) {
          lastPaint = Date.now();
          update();
        }
      }
    } catch (e) {
      msg.error =
        e.name === "AbortError"
          ? "Stopped."
          : e.message || "Connection failed.";
    } finally {
      clearInterval(timer);
      msg.status = null;
      msg.done = true;
      controller = null;
      setBusy(false);
      save();
      update();
    }
  }

  function rate(i, rating) {
    const m = state.messages[i];
    const question = [...state.messages.slice(0, i)]
      .reverse()
      .find((x) => x.role === "user");
    api("/api/feedback", {
      rating,
      question: question ? question.content.slice(0, 1000) : "(plan)",
      answer: (m.content || "").slice(0, 4000),
    }).catch(() => {});
    m.rated = true;
    save();
    log.querySelector(`[data-idx="${i}"]`).replaceWith(renderMessage(m, i));
  }

  // --- Mount ---------------------------------------------------------------

  function mount() {
    if (root && !document.body.contains(root)) document.body.append(root);
  }

  async function init() {
    try {
      const ctrl = new AbortController();
      setTimeout(() => ctrl.abort(), 4000);
      const r = await fetch(API_URL + "/health", { signal: ctrl.signal });
      if (!r.ok) return;
    } catch {
      return; // backend not deployed or unreachable: stay hidden
    }
    build();
    mount();
    if (window.document$) window.document$.subscribe(mount);
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();
