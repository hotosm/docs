# Choose the right frontend tool depending on the context

Amends [0003 - React](./0003-react.md).

## Context and Problem Statement

0003 standardised on React. Tasking Manager made React the default early on,
so most HOT tools were designed around it. React's main advantage for us has
been its large pool of volunteer contributors and contractors.

Since then:

- **Users come first.** Many HOT users work on slow or expensive connections and
  low-spec Android devices. Many tools are map-heavy: drawing areas, editing
  polygons and assigning tasks on a map.
- **Volunteers are few.** New tools get few volunteer contributors so far. They
  are built by very small teams, increasingly with AI assistance.
- **Signals are the new standard.** Web standards are converging on signals for
  reactivity. There is a TC39 proposal, and Svelte, Solid, Vue, Angular and
  Preact all use signals. React keeps its re-render and virtual-DOM model,
  partly because migrating its huge user base is hard.
- **We tried other approaches:**
  - **OpenAerialMap uploader:** mostly forms and progress. HTMX suits it well.
  - **Field-TM:** moved to HTMX in its 2025-26 overhaul. Its core screens are
    interactive maps, and HTMX ended up wrapped in thousands of lines of ad-hoc
    JS, with a clunky UX. Those screens are moving to Svelte.

The size of a framework's contributor pool should not decide our tooling on
its own. The best experience for our users comes first.

## Considered Options

- **React everywhere (status quo).** Familiar to most contributors, but
  heavier, slower on low-spec devices, and easier to write badly.
- **HTMX everywhere.** Simple for forms, but clunky for map-heavy UIs.
- **Solid 2.0.** Has signals and familiar JSX, but:
  - It is a release candidate (October 2026).
  - Its MapLibre bindings don't support 2.0 yet.
  - JSX invites React habits that break it (components run once, and
    destructuring props loses reactivity).
  - It has a smaller community, is more bleeding edge, and is harder for less
    experienced developers.
- **Svelte 5.**
- **Choose per tool or page, by how interactive the UI is.**

## Decision Outcome

Use the best tool for the job, choosing by UI type:

| UI is mostly…                               | Use                                            | Example                                                  |
| ------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------- |
| Forms, lists, CRUD, uploads                 | HTML-first: server templates, HTMX, minimal JS | OAM uploader                                             |
| Maps, drawing, editing, live client state   | **Svelte 5 (runes)**                           | Field-TM task planner                                    |
| An existing React app                       | React. No rewrite needed.                      | Tasking Manager, OAM map frontend                        |
| Extending a tool built on another framework | That tool's framework                          | XLSForm Builder (Vue, to reuse ODK Web Forms components) |

Rule of thumb: if the server owns the state, go HTML-first. If the user edits
state in the browser, especially on a map, use Svelte. Mixing the two in one app
is fine when it is split by page or component.

Why Svelte for rich UIs:

- **Performance:** it compiles to direct DOM updates with a small runtime, so
  apps are faster on low-spec devices and slow networks.
- **Simplicity:** there are no dependency arrays or stale closures, and less
  boilerplate. It's easier to learn and harder to write badly.
- **Signals:** this follows where web standards are heading.
- **Ecosystem:** it works natively with `@hotosm/ui` web components and has
  maintained MapLibre bindings: `svelte-maplibre-gl` with TerraDraw and PMTiles
  extensions.
- **AI tooling:** the official [Svelte MCP server](https://svelte.dev/docs/ai/mcp)
  and autofixer keep generated code idiomatic.

Possibly revisit Solid once 2.0 is stable and its ecosystem has caught up.

Guidelines for Svelte:

- Use Svelte 5 runes only, with TypeScript and Vite. Ship a static build, with
  no Node server in production.
- Set up the Svelte MCP (`npx sv add mcp`) and add its prompt to `AGENTS.md`.
- Keep domain logic in plain TypeScript modules, not in components.

## Consequences

- ✅ Lighter, faster apps for low-bandwidth and low-spec users.
- ✅ Simple tools stay simple, and rich tools get a proper UI framework.
- ✅ Simpler code for small teams and AI-assisted development.
- ✅ Aligned with web standards (signals).
- ❌ More than one frontend pattern to learn across HOT.
- ❌ The contributor and contractor pool is smaller than React's.
- ❌ React components can't be reused. Shared UI must live in `@hotosm/ui`
  web components.
