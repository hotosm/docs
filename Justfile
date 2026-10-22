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

# Docs assistant: up | down | logs | test | eval
chat cmd="up":
  #!/usr/bin/env bash
  set -e
  case "{{cmd}}" in
    up)   docker compose up -d --build && echo "Docs: http://localhost:3000 (assistant appears once models load: just chat logs)" ;;
    down) docker compose down ;;
    logs) docker compose logs -f chat-api llm ;;
    test) cd chat && uv run --group dev pytest -q ;;
    eval) cd chat && uv run python evals/run.py ;;
    *)    echo "Unknown: {{cmd}}"; exit 1 ;;
  esac

# Assistant chart tasks: lint, publish, etc.
chart *args:
  @mkdir -p {{justfile_directory()}}/tasks
  @curl -sS https://raw.githubusercontent.com/hotosm/justfiles/main/chart.just \
    -o {{justfile_directory()}}/tasks/chart.just;
  @just --justfile {{justfile_directory()}}/tasks/chart.just --set chart_name "docs-chat" {{args}}
