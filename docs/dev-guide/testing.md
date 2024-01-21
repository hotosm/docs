# Testing

## Types of Testing

- **Unit Testing:**

  - Focuses on testing individual units or components of a software in isolation.
  - Validates that each unit of code performs as designed.

- **Integration Testing:**

  - Verifies that different units or modules work together as expected.
  - Identifies issues in interactions between integrated components.

- **Functional Testing:**

  - Validates that the software functions according to specified requirements.
  - Ensures that the system behaves as expected from the end-users' perspective.

- **Regression Testing:**

  - Ensures that new code changes don't negatively impact existing functionalities.
  - Detects unintended side effects caused by modifications.

- **Acceptance Testing:**

  - Validates that the entire system meets the specified requirements
    and is accepted by stakeholders.
  - Can include user acceptance testing (UAT) and business acceptance testing.

- **Performance Testing:**

  - Evaluates the system's responsiveness, scalability, and stability
    under different conditions.
  - Includes load testing, stress testing, and scalability testing.

- **Security Testing:**

  - Identifies vulnerabilities and weaknesses in the software's security features.
  - Ensures that sensitive data is protected and the system is resistant to attacks.

- **Usability Testing:**

  - Assesses the software's user interface, user experience, and overall
    user-friendliness.
  - Focuses on how easily users can interact with and navigate through the application.

- **Compatibility Testing:**

  - Ensures that the software functions correctly across different
    devices, browsers, and operating systems.
  - Verifies compatibility with various configurations.

- **Smoke Testing:**

  - A subset of tests to verify basic functionality and ensure the
    stability of a new build.
  - Quick checks performed before more comprehensive testing.

- **Exploratory Testing:**

  - Informal testing approach where testers explore the application to find defects.
  - Emphasizes discovery and learning during the testing process.

- **White Box Testing:**

  - Examines the internal logic, code structure, and implementation
    details of the software.
  - Requires knowledge of the internal workings of the application.

- **Black Box Testing:**

  - Tests the software's functionality without knowing its internal code or logic.
  - Focuses on inputs and outputs, treating the software as a "black box".

- **Ad-hoc Testing:**

  - Informal and unplanned testing approach.
  - Testers explore the application without predefined test cases.

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
