# Architectural Decisions

Markdown Architectural Decision Records documenting the technical decision
taken across HOTOSM projects.

These decisions are advisory, with some scope for variation in projects if
specific requirements arise.

## Replacing a decision

Decision records are not rewritten once accepted, so the reasoning at the time
is kept. When a decision changes:

1. Write a new record, starting with `Amends [00XX](...)` or
   `Supersedes [00XX](...)`.
2. Add a note at the top of the old record linking to the new one.
3. In `mkdocs.yml`, point the topic's nav entry at the new record and move
   the old one under **Amended / Superseded**.
