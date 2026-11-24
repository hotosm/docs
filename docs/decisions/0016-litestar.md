# Use Litestar for new Python web backends

## Context and Problem Statement

The [web backend guide](../dev-guide/web-backend.md) recommended FastAPI
as of 2024, and listed Litestar as a contender. Since then, our newest
backends have moved to Litestar:

- **Field-TM** replaced FastAPI with Litestar for its built-in HTMX and
  templating support.
- **The OAM uploader** chose Litestar to match Field-TM.
- **Drone-TM v2 - in progress** needs a thin JSON API (writes and a sync proxy) behind a
  Svelte app.

We should pick one default, so that the same team reuses the same patterns
across tools.

## Considered Options

- FastAPI
- Litestar
- Others like Django

## Decision Outcome

Use Litestar for new Python web backends. Existing FastAPI services can stay
as they are, with no rewrite needed.

For a small JSON API there is little technical difference between the two.
We are choosing for consistency:

- **One set of patterns:** psycopg with raw SQL, `hotosm-auth[litestar]`,
  dependency injection, tests and the Helm layout are shared across tools.
- **Governance:** Litestar is run by a group of maintainers, whereas FastAPI
  depends mostly on one.
- **More built in:** HTMX, templating, msgspec, stores and rate limiting,
  with fewer plugins to maintain.
- **Familiar:** the syntax is close to FastAPI's, and Pydantic models work
  unchanged.

### Consequences

- ✅ HOT's backends share the same patterns, so code and fixes move between
  tools easily.
- ✅ A FastAPI developer can read Litestar code straight away.
- ❌ Fewer contributors, answers and examples know Litestar than FastAPI.
- ❌ Small differences to learn: `Provide()` for dependencies, the request
  body arrives as `data`, `@post` returns 201 by default, and validation
  errors are 400, not 422.
- ❌ Litestar 3 is in development, so expect one major upgrade.
