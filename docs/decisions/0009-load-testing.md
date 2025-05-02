# Use k6 or Oha for application load testing

## Context and Problem Statement

We need lightweight tools to simulate real-world traffic for
performance testing of our APIs and services.

Requirements include:

- Easy setup and usage.
- Ability to run both quick, one-off benchmarks and complex scripted scenarios.
- CI/CD integration capability.

## Considered Options

- Apache JMeter
- Locust
- k6
- oha
- wrk

## Decision Outcome

We adopted a hybrid approach using oha for simple benchmarks and
k6 for more advanced, scripted load tests.

oha is fast and easy to use for quick HTTP benchmarking (similar to wrk,
but with a simpler interface and better reporting).

k6 is a developer-centric load testing tool that supports JavaScript
scripting for complex test scenarios, integrates well with CI pipelines,
and produces meaningful metrics.

## Consequences

- ✅ oha gives us a fast, no-frills tool to test latency and throughput of HTTP endpoints.
- ✅ k6 allows scripting advanced load test scenarios using JavaScript, including
  auth flows and dynamic data.
- ✅ Both tools are CLI-friendly and CI-compatible.
- ❌ Splitting tools means learning two interfaces.
- ❌ k6 can be resource-intensive during heavy test scenarios.
