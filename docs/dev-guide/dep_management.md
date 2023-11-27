# Dependency Management

## Javascript

This section will be brief.

Javascript already has a great dependency management ecosystem.

Tools like NPM, Yarn, PNPM all work in a Node environment to
solve dependency version compatibility and install them locally
within your repo, in a `node_modules` directory.

The only recommendation would be to **use PNPM**, as it has a much neater
concept then the other two tools. Dependency locking is fast, and
package installation is _shared_ across repositories using a global
package store on your system.

This sets the standard for dependency management that some Python
tools have attempted to replicate.

## Python

### Using pyproject.toml

### Dependency Solvers
