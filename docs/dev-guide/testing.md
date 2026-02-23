# Testing

## Types of Testing

![test-pyramid](../images/test_pyramid.webp)

### Unit Testing

- Testing specific isolated functions or classes in your code.
- Inputs are pre-defined and outputs are mocked to verify the code
  works as intended.
- Unit tests can be written for the backend (e.g. Pytest) and frontend
  (e.g. Vitest).

### Integration Testing

- Verifies that different units or modules work together as expected.
- For example and endpoint on a web API can be tested as such:
  - Call and endpoint that triggers code in various modules.
  - Standarise the input to the test, for example a specific JSON.
  - Check the output data matches the expected output, every time it runs.
- Typically backend tests, but can also be written to group together
  multiple frontend unit tests (for example, testing a component state).

### End-to-End (E2E) Testing

- Similar to integration tests, except the entire expected user
  workflow is tested (i.e. the ordering is important).
- For example, if you expect a user to create a user account -->
  create a project --> perform some processing, then these steps will
  be tested in order (as if the user was using the software).

### User Interface (UI) Testing

- Checking for changes to the user interface functionality can be
  automated.
- As of 2024, a great tool to do this is
  [Playwright](https://github.com/microsoft/playwright).
- The idea is to navigate to various pages and see if the output is as
  expected.
- For example, a screenshot of a page can be taken on a page load, then
  compared against a page load in a future test. This will determine if
  any unexpected visual regression has occured.
- Page elements can be navigated and interacted with using [various
  properties](https://playwright.dev/docs/locators), such as element
  names, ids, labels, to lower level CSS and XPath if required.

### Performance Testing

- Evaluates the system's responsiveness, scalability, and stability
  under different conditions.
- Includes:
  - Load testing, for expected and peak load.
  - Stress testing, for abnormally high load / upper limit testing.
  - Scalability testing, used to identify optimal configuration to handle load.
- Generally for backend or database code.
- An example could be using a profiler to determine response time in a web API,
  or using `EXPLAIN ANALYSE` on a database to determine bottlenecks.

### Security Testing

- Identifies Common Vulnerabilities and Exposures (CVEs) in software.
- CVEs are publically available lists of identified security flaws in code.
- One way to test this could be container image scanning, which checks for
  vulnerabilities in the underlying operating system, plus the code and dependencies.

### Smoke Testing

- A test to pretty much see if your application starts up.
- If a smoke test fails, then you application failed to initialise.
- Particularly useful to test if a container runs as expected.
- Useful to include in CI to prevent deployment if smoke test fails.

## Testing Terminology

### White Box Testing

- Examines the internal logic, code structure, and implementation
  details of the software.
- Requires knowledge of the internal workings of the application.

### Black Box Testing

- Tests the software's functionality without knowing its internal code or logic.
- Focuses on inputs and outputs, treating the software as a "black box".

### Alpha Testing

- Conducted by a select group of users before the software's public release.
- Focuses on identifying major issues before wider deployment.

### Beta Testing

- Conducted by a larger group of users in a real-world environment.
- Gathers feedback from end-users to improve the software before the final release.

## Python

### PyTest

- PyTest is a popular **unit testing** framework for Python, with more
  in-built functionality than the standard Python `unittest` module.
- It has a simple and concise syntax, many plugins, plus async support,
  and detailed / informative reporting.
- Two major advantages are:
  - Fixtures: allows you to set up and tear down resources during
    testing, for example database entries.
  - Parameterised testing: allowing you to run the same test with
    different input values.
- With the help of plugins, it's easy to write **integration tests** too.
- For example a FastAPI endpoint can be called with inputs, to test the
  outputs are as expected.

Usage:

```bash
pytest
```

### Coverage

- The concept of coverage is to determine the amount of your code that
  is executed during unit tests.
- This metric is a rough approximation of how thoroughly your tests
  actually test your code.
- Use with care, this is only an assessment of how much code is touched by
  your tests. A 100% coverage codebase may still be poorly tested.

Usage:

```bash
coverage run -m pytest
```

Generating reports:

```bash
coverage report -m
```

## Javascript

### ViTest

### Playwright
