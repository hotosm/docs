# Version Control

## Semantic Versioning (SemVer)

- A method of versioning your software packages.
- Makes most sense for versioning software that is used by another piece
  of software, e.g. a Python package that is installed.
- The version number is composed of three segments: `MAJOR.MINOR.PATCH`,
  for example `1.4.2`.
  - MAJOR: Increments when incompatible API changes are introduced.
    It indicates that there are significant and potentially breaking
    changes that might require modifications in existing code.
  - MINOR: Increments when new features are added in a backward-compatible manner.
    It signals the addition of functionality without breaking existing code.
    Developers can expect that their code will still work as intended.
  - PATCH: Increments for backward-compatible bug fixes.
    It denotes minor improvements or bug fixes that do not introduce new
    features and do not break existing functionality.

## CalVer and others

- Sometimes SemVer doesn't make sense. For example, in a user-facing **software
  service/tool**, what does a 'breaking' change denote?
- In these cases, other conventions may be better suited.
- At HOT, we use `YYYY.VERSION.PATCH`, in line with the developers of the ODK ecosystem.
  - YYYY: the current year.
  - VERSION: the release version for the current year. Resets in the next year.
  - PATCH: a patch to the released version, typically bugfixes.

## Conventional Commits

A [specification](https://www.conventionalcommits.org/en/v1.0.0/)
for adding human and machine readable meaning to commit messages.

Format: `<type>[optional scope]: <description>`

Example: `feat: allow provided config object to extend other configs`

A 'new' standard for commit messages.

Allows for easy semantic versioning, x.x.x, as the type of increment can be
automatically determined based on the commit types.

## Tools

Some tools can make your life easier when working with conventional commits
and SemVer.

### Commitizen
