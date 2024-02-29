# Testing

## Types of Testing

### Code Tests

![test-pyramid](../images/test_pyramid.webp)

- **Unit Testing:**

  - Testing specific isolated functions or classes in your code.
  - Inputs are pre-defined and outputs are mocked to verify the code
    works as intended.
  - Unit tests can be written for the backend (e.g. Pytest) and frontend
    (e.g. Vitest).

- **Integration Testing:**

  - Verifies that different units or modules work together as expected.
  - Identifies issues in interactions between integrated components.
  - For example and endpoint on a web API can be tested for expected
    output, which may run various different functions throughout the code.
  - Typically backend tests, but can also be written to group together
    multiple frontend unit tests (e.g. testing a component state).

- **User Interface (UI) Testing:**

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

- **End-to-End (E2E) Testing:**

  - Similar to integration tests, except the entire expected user
    workflow is tested.
  - For example, if you expect a user to create a user account -->
    create a project --> perform some processing, then these steps will
    be tested in order (as if the user was using the software).

### Other Tests

- **Performance Testing:**

  - Evaluates the system's responsiveness, scalability, and stability
    under different conditions.
  - Includes load testing, stress testing, and scalability testing.

- **Security Testing:**

  - Identifies vulnerabilities and weaknesses in the software's security features.
  - Ensures that sensitive data is protected and the system is resistant to attacks.

- **Smoke Testing:**

  - A test to pretty much see if your application starts up.
  - If a smoke test fails, then you application failed to initialise.
  - Particularly useful to test if a container runs as expected.

- **White Box Testing:**

  - Examines the internal logic, code structure, and implementation
    details of the software.
  - Requires knowledge of the internal workings of the application.

- **Black Box Testing:**

  - Tests the software's functionality without knowing its internal code or logic.
  - Focuses on inputs and outputs, treating the software as a "black box".

- **Alpha Testing:**

  - Conducted by a select group of users before the software's public release.
  - Focuses on identifying major issues before wider deployment.

- **Beta Testing:**

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

Usage:

```bash
pytest
```

### Coverage

- The concept of coverage is to determine the amount of your code that
  is executed during unit tests.
- This metric is a rough approximation of how thoroughly your tests
  actually test your code.

Usage:

```bash
coverage run -m pytest
```

Generating reports:

```bash
coverage report -m
```

## Javascript
