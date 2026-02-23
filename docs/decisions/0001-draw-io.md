# Use Mermaid for technical diagrams

## Context and Problem Statement

We need a simple and intuitive way to make technical diagrams.

This encompasses drawing flow charts of various forms, architectural
diagrams, and other diagrams showing the relationships between
technical components.

## Considered Options

- UML, drawn via LibreOffice
- [Diagrams as code](https://github.com/mingrammer/diagrams)
- [Diagrams as markdown](https://github.com/mermaid-js/mermaid)
- Simple SVG editing software, such as Inkscape
- Diagrams.net, a wrapper for draw.io

## Decision Outcome

- The team needs diagrams that are easy to diff, review, and update with
  small textual changes.
- Mermaid diagrams are stored directly in markdown and render in both
  MkDocs Material and GitHub, which keeps authoring and review in one place.
- This also enables LLM-assisted updates where diagram structure can be
  edited from plain text descriptions.

### Consequences

- Good, because Mermaid source is plain text and review-friendly in PRs.
- Good, because diagrams can be generated and updated programmatically.
- Good, because there is no dependency on a visual editor for routine edits.
- Bad, because advanced layout control and custom iconography are more limited
  than in draw.io.
- Bad, because larger diagrams can need manual tuning for readability.
