# Use React as our main frontend library

## Context and Problem Statement

At HOTOSM we mostly develop web applications, which require a frontend
component.

We need to balance:

- Complexity / learning curve.
- Existing knowledge of staff.
- Knowledge of key contractors for various tools.
- Performance.
- Existing library support (community & ecosystem).
- Scalability & maintainability.

## Considered Options

- Angular
- Vue
- React
- Svelte
- Solid
- Qwik
- Vanilla JS + Web Components

## Decision Outcome

This decision was made many years ago (~2018) with the introduction
of Tasking Manager v3.

The decision was to use React, as that is where the industry was
centered around at that time.

Due to technical debt, skills / knowledge with React within the team, and
with various contractors, this decision has been carried forward into
future projects, in an attempt to standardize:

- The learning curve / pool of experience.
- Speed and ease of setting up new projects.
- Avoiding the churn of frontend libraries: contractors must use React.

This decision still stands as of 2025, however, it is becoming
[increasingly apparent](https://www.zachleat.com/web/react-criticism)
that this should be revisited in the near future.

There is also the higher level discussion for
[if we need a frontend framework at all](https://infrequently.org/2024/11/if-not-react-then-what),
as much of our functionality could be implemented with simpler HTML-first
technologies such as HTMX, with
[progressive enhancement](https://www.gov.uk/service-manual/technology/using-progressive-enhancement).

As a result, some flexibility is possible to choose more suitable tools for
newly started projects.

### Consequences

- Good, the many people have React experience. It broadens the pool of available
  contractors, and fits well with existing skills in the team.
- Bad, because performance is superceded by frameworks that do not rely on the
  virtual-DOM, such as Svelte and Solid.
- Bad, because React is not as user friendly as it claims to be. It's far easier
  to write bad React code, in comparison to frameworks like Svelte.
- Bad, because this unfriendliness to new developers does not only affect performance,
  but also extends to the code complexity and ease of understanding / onboarding.
- Bad, because we don't necessarily need a web framework for all our tools!
  We could probably build more resilient code using HTML with progressive enhancement.
