# List available commands
[private]
default:
  just help

# List available commands
help:
  just --justfile {{justfile()}} --list

# Run pre-commit hooks
lint:
  uv run pre-commit run --all-files

# Run dev mkdocs server
dev:
  docker run --rm -p 3000:3000 -v $PWD:/docs --workdir /docs \
  ghcr.io/hotosm/gh-workflows/mkdocs:main serve --dev-addr 0.0.0.0:3000
