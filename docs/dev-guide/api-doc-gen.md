# Auto Documentation Generation

## Python

- Ensure that functions and class method have descriptive docstrings.
- Type hinting should be used for parameter and return types.
- With this in place, there are many tools to automatically extract
  API documentation from your code.
  - MKDocs has a great extension `mkdocstrings-python` for this purpose.
  - Example markdown page to automatically extract docs:

```markdown
# your_module.py

::: your_package.your_module.function1
options:
show_source: false
heading_level: 3

::: your_package.your_module.function2
options:
show_source: false
heading_level: 3

::: your_package.your_module.Class1
options:
show_source: false
heading_level: 3
```

> Note that all methods within a class a picked up automatically.

## Javascript

- JSDoc docstrings are the standard here.
- When adding typing (typescript) to your project, there are two options:
  - TypeScript: code-based, compiled TS --> JS.
  - JSDoc type hints: docstring-based, built on standard JS.
