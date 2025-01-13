# Use Python as our main backend language

## Context and Problem Statement

At HOTOSM we mostly develop:

- Web applications.
- Data processing pipelines.

We need a backend language that is:

- Beginner friendly, allowing for easy community contribution.
- Simply and quick to develop with, making us responsive when needed.
- Reasonably performant.
- General purpose, allowing us to achieve lots with the same skillset.
- Good existing library support, reducing code duplication.

## Considered Options

- Python
- Golang
- Rust
- C++
- JavaScript
- Java / Kotlin

## Decision Outcome

Python was chosen as the best compromise across all languages listed.

JavaScript would have the benefit of keeping our stack to a single language,
however, it is doesn't have great performance. It is also more complex than
Python, particularly when it comes to asynchronous programming.

Rust and C++ are too low-level and complex for our use cases (unless a specific
performance critical need arises).

Golang is an excellent beginners language, however, may be slightly too low-level
to recommend it to everyone (requiring knowledge of pointers etc). It's a good
choice for specific cases, but library support is also lacking.

Java is popular because of historic use, and is still arguably a good language,
however it's pros do not outweight the cons when compared to more modern
languages such as Golang or Rust.

### Consequences

- Good, the many people have Python experience. It broadens the pool of available
  contractors, and fits well with existing skills in the team.
- Good, because it's the most versatile language listed as of 2025, including
  excellent support for Web APIs, Machine Learning libraries, backend processing.
- Good, because it's very intuitive and simple to learn, often being a great first
  language to learn for junior developers.
- Good, because of a huge amount of existing libraries in Python, meaning we have
  to code less!
- Bad, because we use separate languages for frontend / backend development.
- Bad, it's not the most performant language of the bunch, particularly due to the
  Global Interpreter Lock.
- Bad, because far from perfect dependency management (which might be solved
  with the advent of <https://github.com/astral-sh/uv>)
