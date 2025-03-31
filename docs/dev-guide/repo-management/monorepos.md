# Using Monorepos

- It may seem intuitive to divide up each part of a project into logical
  components / separate Git repositories (backend / frontend as an example).
- However, there are many benefits to monorepos (all in a single repository),
  and they often allow for faster development cycles.

  **At HOT, we mostly prefer a monorepo-based setup**

## Advantages Of Monorepos

- **Discoverability**: particularly when working with an open-source community
  around a tool. Having all code in one place makes for an easier entrypoint
  for potential contributors.
- **Easier management**: manage issues and discussions about a tool in one place,
  including documentation.
- **Component compatibility**: having frontend and backend components in one
  place ensures that versions of both should always be compatible with
  one another (especially when released together).
- **Better collaboration**: avoids silos for 'backend' and 'frontend' teams.
- **Easier testing**: for full E2E tests involving both the frontend and backend,
  it is often easier running the code from a single repo (e.g. start the
  backend first, then run API calls from the frontend).
- **Easier deployment**: tightly coupling releases for components and sharing
  CI/CD workflows for the testing and deployment.
- **Standardized tooling**: every developer uses the same tools for a project.
  Hopefully, this avoids 'it works on my machine' issues.

### UV Workspaces (Python)

- If working on a Python project with many self-contained, packageable
  modules, `uv` workspaces are an excellent tool for managing and
  publishing multiple modules from the same repository. This is
  similar to Cargo in Rust.

## When To Use Separate Repos

- **Very large teams**: in organizations with 100+ developers, monorepos can
  become difficult to manage, leading to bottlenecks in workflows such as
  CI/CD and version control conflicts.
- **Unrelated projects**: if different parts of a system have little or no  
  dependency on each other (e.g. a backend API unrelated to a frontend app),  
  splitting them into separate repositories might be more logical.
- **Scalability concerns**: as a monorepo grows, issues can arise with  
  repository size, build times, and dependency management. Modular
  repositories can scale better over time.
- Using **entirely different technology stacks** between projects.
