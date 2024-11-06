# Use mkdocs for technical documentation

## Context and Problem Statement

We need to both:

- Display written technical documentation.
- Generate technical API docs automatically.

## Considered Options

- Vanilla MKDocs
- MKDocs with mkdocs-material theme
- Vanilla Astro
- Astro Starlight
- Manual HTML / JS / CSS
- Any other web framework

## Decision Outcome

We chose MKDocs with mkdocs-material theme as an excellent open-source
tool with a large community backing it.

Many of the other options either have too high of a maintenance burden,
or don't integrate as nicely with our code.

Astro Starlight is a close contender, as it's an equally good markdown
renderer, with probably nicer themeing. This decision was taken prior
to full knowledge and testing of Astro Starlight, so it was not given
as fair of a chance. Previous experience with a tool counts for something,
and more devs at HOT had knowledge of mkdocs. It's also a Python tool,
when most of our backend code is written in Python, giving the option
for auto-generating API docs.

### Consequences

- Good, because markdown is super simple, even for non-technical users, broadening
  the possible number of users that could contribute (not just devs).
- Good, because mkdocs-material does most of the work for us of making the docs
  look half decent.
- Good, because it's a Python tool at heart, so we can use plugins like
  `mkdocstrings-python` to very easily read docstrings and type hints to
  auto-generate API documentation for us.
- Bad, because less customisation than would be possible with other solutions.
  The docs may look slightly generic and less appealing.
