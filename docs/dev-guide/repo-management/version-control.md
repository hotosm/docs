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

- Sometimes SemVer doesn't make sense. For example, in a user-facing
  **software service/tool**, what does a 'breaking' change denote?
- In these cases, other conventions may be better suited.
- At HOT, we use `YYYY.VERSION.PATCH`, in line with the developers of the ODK ecosystem.
  - YYYY: the current year.
  - VERSION: the release version for the current year. Resets in the next year.
  - PATCH: a patch to the released version, typically bugfixes.

## Conventional Commits

A [specification](https://www.conventionalcommits.org/en/v1.0.0/)
for adding human and machine readable meaning to commit messages.

A 'new' standard for commit messages.

**Format**: `<type>[optional scope]: <description>`

Example `feat: allow provided config object to extend other configs`
Example `fix: fixed the bug in issue #123`

**Advantage**: Automated SemVer version management (major.minor.patch),
and automated changelogs.

## Tool: Commitizen

- [Commitizen](https://commitizen-tools.github.io/commitizen) is a
  Python tool to help with creating **conventional commits** and
  automating version control.

- Versions are managed by Commitizen from the `pyproject.toml` file in a
  repo.

- Versions are determined by conventional commit messages:
  - `fix: xxx` denotes a patch, `feat: xxx` denotes a minor increment.
  - Breaking changes are applied every year to increment the `YYYY` in
    place of `MAJOR`.

### Install

`pip install commitizen`

### Commiting Code

- Instead of `git commit` use `cz commit` and follow the prompts.
- You can select the type of commit, plus additional metadata.

### Bumping a Version

- When you decide it is time to create a new version:

  ```bash
  pip install commitizen # (if not installed)

  cz bump --check-consistency --changelog

  git push
  git push --tag
  ```

<!-- markdownlint-disable -->

!!! warning

    This assumes you have repo write access and are working on the main branch.

<!-- markdownlint-enable -->

This will:

- Update the SemVer version number in locations specific in `pyproject.toml`,
  throughout the codebase.
  - If a `feat` commit is included, the version is bumped by a minor
    increment (0.x.0), if only `fix` is included a patch will be used
    (0.0.x).
- Automatically update CHANGELOG.md with all changes since the last version.
- Create a tag matching the version number.

<!-- markdownlint-disable -->

!!! tip

    Oh no I made a mistake!

    Worry not, the version increment can be reverted:

    ```bash
    # Revert the commit
    git reset --soft HEAD~1

    # Delete the branch
    git branch -d v0.x.x
    git push --delete origin v0.x.x
    ```

<!-- markdownlint-enable -->

## Tool: uv

- Using **workspaces** it's possible to setup your Python packages in a
  [monorepo](./monorepos.md).
- `uv` can be used to manage, and publish, each package independently.
- To publish a specific package from a monorepo, go to the directory
  where the `pyproject.toml` is located:

  ```bash
  uv --project=./packages/project1 build
  uv --project=./packages/project1 publish
  ```

## Creating Releases

1. Update the version throughout the code ([Bumping a Version](#bumping-a-version)).
2. Go to the Releases page of your repo
   (<https://github.com/ORG/REPO/releases>).
3. Click `Draft a new release`.
4. Click `Choose a tag`, then input the current version number and press
   enter (this will automatically create a matching tag for your release).
5. Set the `Release title` to v`x.x.x`, replacing with your version number.
6. Add a description if possible, then release.

This should trigger the PyPi publishing workflow (for HOT repos), and
your version will be available on [PyPi.org](https://www.pypi.org).
