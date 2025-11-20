# 0x03. Unittests and Integration Tests

This project covers how to write unit tests and integration tests in Python using the `unittest` framework, `mock`, and `parameterized`. The goal is to learn how to properly test functions, mock external calls, and validate full code paths end-to-end.

## Learning Objectives

By the end of this project, I should be able to explain:

- The difference between unit tests and integration tests.
- How to use the `unittest` module.
- Common testing patterns such as:
  - Mocking
  - Parametrization
  - Fixtures
- How to test exceptions and error cases.
- How to mock external services such as HTTP requests.
- How to write integration tests that test entire workflows.

## Requirements

- Python 3.7+
- All code interpreted on Ubuntu 18.04 LTS.
- Code must follow `pycodestyle` (PEP 8) style guidelines.
- All files must be executable.
- Every module, class, and function must have documentation.
- All functions and coroutines must be type-annotated.

## Files in This Project

- **utils.py** – Contains helper utility functions.
- **client.py** – Contains the GitHub client logic.
- **fixtures.py** – Contains test fixtures and payloads.
- **test_utils.py** – Unit tests for `utils.py`.
- **test_client.py** – Unit and integration tests for `client.py`.

## Running Tests

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py