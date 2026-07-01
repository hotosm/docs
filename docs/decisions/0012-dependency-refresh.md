# Use Renovate for automated dependency refreshes

## Context and Problem Statement

We need automated dependency refreshes to keep frontend, backend, and infrastructure
packages current with minimal manual effort.

## Considered Options

- Dependabot
- Renovate

## Decision Outcome

Renovate was selected.

The primary reason is that Renovate is platform agnostic, reducing vendor lock-in
to GitHub. It can run across GitHub, GitLab, Gitea, Forgejo, and self-hosted setups,
which better matches our long-term portability goals.

Renovate also has stronger grouping, scheduling, dashboard, and monorepo update
features than Dependabot.

## Consequences

- ✅ Reduces dependency on GitHub-specific automation.
- ✅ Supports more flexible grouping and scheduling of updates.
- ✅ Works well across monorepos and multiple dependency ecosystems.
- ❌ Requires configuring the Renovate app or self-hosted runner.
- ❌ Slightly more setup and maintenance than GitHub-native Dependabot.
