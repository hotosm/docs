# Allow Svelte for new frontends

Amends [0003 - React](./0003-react.md).

## Context and Problem Statement

0003 standardised on React. Context since that decision:

- Many HOT users still work on slow or expensive connections and low-spec Android
  devices.
- Several tools, e.g. Field-TM, need rich map-heavy UIs maintained by very small
  teams, increasingly with AI assistance.
- The web is converging on **signals** for reactivity. There is a TC39 proposal,
  and Svelte, Solid, Vue, Angular and Preact all use signals. React keeps its
  re-render and virtual-DOM model instead (due to difficulty migrating /
  affects on such a large user base).

## Considered Options

- React (status quo)
- Solid 2.0
- Svelte 5
- No framework (HTML-first / HTMX, vanilla TypeScript)

## Decision Outcome

New frontends may use **Svelte 5 (runes)**. Existing React projects stay on
React. Pages that are mostly forms and lists should stay HTML-first.

Why Svelte:

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

Why not Solid, for now: it has the same signals model and familiar JSX, but:

- 2.0 is still a release candidate (October 2026), and the MapLibre bindings
  don't support it yet.
- JSX invites React habits that break Solid. Components run only once, and
  destructuring props loses reactivity.
- It has a smaller community & adoption, and is more bleeding edge than Svelte.
  Adoption by less experienced devs would be more difficult.

Guidelines:

- Use Svelte 5 runes only, with TypeScript and Vite. Ship a static build, with
  no Node server in production.
- Set up the Svelte MCP (`npx sv add mcp`) and add its prompt to `AGENTS.md`.
- Keep domain logic in plain TypeScript modules, not in components.

## Consequences

- ✅ Lighter, faster apps for low-bandwidth and low-spec users.
- ✅ Simpler code for small teams and AI-assisted development.
- ✅ Aligned with web standards (signals).
- ❌ HOT now has two frontend frameworks. The contractor pool is smaller than
  React's.
- ❌ React components can't be reused. Shared UI must live in `@hotosm/ui`
  web components.
