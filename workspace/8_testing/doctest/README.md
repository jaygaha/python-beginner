# Python Doctest

The `doctest` module is a powerful tool included in the Python standard library. It allows you to test your code by running examples embedded in the documentation (docstrings). This ensures that your documentation is always synchronized with your code, providing clear, executable examples of how your functions work.

This directory contains a practical example demonstrating how to implement and run doctests in a typical Python project.

## Example Project: `math_utils`

As a case study, this repository includes the `math_utils` project, a simple calculator library. This project is designed to showcase the best practices for using doctest for testing.

**Explore the project:** [math_utils/](./math_utils/)

### Key Concepts Demonstrated in `math_utils`

The `math_utils` example illustrates several core features of `doctest`.

#### 1. Tests as Documentation

Doctests are written directly inside function docstrings. They look like an interactive Python session, making them intuitive and easy to read.

Here is an example from the `math_utils` calculator:
```python-beginner/workspace/8_testing/doctest/math_utils/app/calculator.py#L5-14
def add(a, b):
    """
    Add two numbers.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b
```

#### 2. Testing for Exceptions

`doctest` provides a simple syntax for verifying that a function correctly raises an exception. You need to include the traceback message that you expect.

```python-beginner/workspace/8_testing/doctest/math_utils/app/calculator.py#L32-45
def divide(a, b):
    """
    Divide a by b, raising ValueError if b is zero.

    >>> divide(6, 3)
    2.0
    >>> divide(5, 2)
    2.5
    >>> divide(10, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot divide by zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

#### 3. Multiple Test Execution Methods

The `math_utils` project demonstrates three different ways to run your doctests:

1.  **Directly via the Command Line**: Run `doctest` on a specific module.
2.  **Custom Test Runner**: A script (`run_doctests.py`) that provides more control and detailed output.
3.  **Integration with `unittest`**: Combine doctests with a traditional `unittest` test suite.

### How to Run the Example Tests

To see `doctest` in action, navigate to the `math_utils` directory and run the following commands.

```bash
cd math_utils
```

**Run doctests on the calculator module directly:**
```bash
python -m doctest app/calculator.py -v
```

**Use the custom test runner for a detailed summary:**
```bash
python run_doctests.py
```

**Run doctests integrated with `unittest`:**
```bash
python -m unittest tests.test_calculator -v
```

For a complete guide on the `math_utils` implementation, including unit tests and project structure, please see its detailed README file:
[math_utils/README.md](./math_utils/README.md)

## Example Project: `math_utils_api`

This directory also contains a more advanced example, `math_utils_api`, which demonstrates how to use `pytest` to run doctests alongside traditional unit tests in a FastAPI application.

**Explore the project:** [math_utils_api/](./math_utils_api/)

### Key Concepts Demonstrated in `math_utils_api`

- **Testing FastAPI with `pytest`**: Shows how to test a web API built with FastAPI.
- **Combined Test Strategy**: Integrates `doctest` for simple function verification and `pytest` for more complex scenarios like API endpoint testing.
- **Modern Project Tooling**: Uses `pyproject.toml` for dependency management, a standard in modern Python projects.

For a complete guide on the `math_utils_api` implementation, including setup, running the server, and testing, please see its detailed README file:
[math_utils_api/README.md](./math_utils_api/README.md)