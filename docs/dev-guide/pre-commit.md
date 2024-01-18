# Pre-Commit Hooks

## Git Hooks

Git has **hooks**, which can run code on various events:

- Prior to commiting code (pre-commit).
- After committing code (post-commit).
- After checking out a branch (post-checkout).
- Before rebasing (pre-rebase).
- Etc.

### Pre-Commit Hook

- Pre-commit Git hooks run checks before a commit is accepted.
- Pre-commit is a package to automate the setup.
- After config, issues such as syntax errors and security flaws are picked up.
- Used mostly for formatting and linting.
- Linting is checking code against a set of formatting rules
  and for syntax errors.

## Pre-Commit (Python Tool)

- [Pre-commit](https://pre-commit.com/) is a Python tool for simplifying
  and applying Git pre-commit hooks.
- Hooks can be configured via a YAML file, then applied on each attempted commit.
- There are many hooks available from different sources.

Install it with:

```bash
pip install pre-commit
```

### Add pre-commit-config.yaml

- Add a `pre-commit-config.yaml` to your repo root.
- A best practice config file, taken from FMTM:

```yaml
repos:
  # Versioning: Commit messages & changelog
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]

  # Autoformat: Python code
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        files: ^src/backend/(?:.*/)*.*$
        args: [--target-version=py39]

  # Lint / autoformat: Python code
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: "v0.1.13"
    hooks:
      - id: ruff
        files: ^src/backend/(?:.*/)*.*$
        args: [--fix, --exit-non-zero-on-fix]

  # Autoformat: YAML, JSON, Markdown, etc.
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        args:
          [
            --ignore-unknown,
            --no-error-on-unmatched-pattern,
            "!CHANGELOG.md",
            "!CONTRIBUTING.md",
            "!LICENSE.md",
            "!src/frontend/pnpm-lock.yaml",
          ]

  # Lint: Bash scripts
  - repo: https://github.com/openstack-dev/bashate.git
    rev: 2.1.1
    hooks:
      - id: bashate

  # Lint: Shell scripts
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.9.0.6
    hooks:
      - id: shellcheck
        args: ["-x"]

  # Lint: Markdown
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.38.0
    hooks:
      - id: markdownlint
        args:
          [
            --fix,
            --ignore,
            LICENSE.md,
            --ignore,
            CHANGELOG.md,
            --ignore,
            .github,
          ]
```

> Note: the config above is for a monorepo configuration.
>
> Your repo may not require both Python and JS code formatting.

### Add Hooks

Run

```bash
# Standard install for most hooks
pre-commit install

# Additional commit-msg hook (for the commitizen hook above)
pre-commit install --hook-type commit-msg
```

Now when you attempt to commit to the repo:

- Code will be auto-formatted.
- An error will show if linting fails.
- An error will show if commit messages are in the wrong format.
