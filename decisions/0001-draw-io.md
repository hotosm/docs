# Use draw.io (diagrams.net) for technical diagrams

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

- The author deemed UML to be useful for certain circumstances, but
  largely an academic exercise. It shines at creating relationship
  diagrams between Object-oriented code, which is not what we need.
  It also looks pretty bad when public facing.
- Tools like Diagrams and Mermaid could be great to use in certain
  instances (Mermaid is probably favoured for the simplicity of
  markdown). However, they are still not very approachable if
  a non-technical user wishes to edit these diagrams.
- Diagrams.net (draw.io) has many advantages and hence was chosen:

### Consequences

- Good, because draw.io uses an open XML standard to save, plus can be exported in
  SVG or PNG format as needed
- Good, because it's super simple to use, particularly if exported to SVG for
  editing. Anyone should be able to edit the diagrams.
- Good, because draw.io is open-source, with a permisive license even for
  commercial use.
- Good, because the diagrams.net wrapper has Git integration where you save straight
  to a repo, meaning we can auto-deploy docs when diagrams are edited.
- Bad, it is slightly more manual with the design / placement than code --> diagram
  options such as Diagrams or Mermaid.
- Bad, because diagrams.net could decide to shut down or change their license.
  But this would not be a huge deal due to open standards / easy migration.
