#!/usr/bin/env python3
"""
Doctest runner for math_utils package.

This script runs all doctests found in the calculator module and provides
detailed output about the test results.
"""

import doctest
import sys
from app import calculator


def run_doctests():
    """Run all doctests in the calculator module."""
    print("Running doctests for math_utils calculator module...")
    print("=" * 60)

    # Run doctests with verbose output
    result = doctest.testmod(calculator, verbose=True)

    print("=" * 60)
    print("Doctest Summary:")
    print(f"Tests run: {result.attempted}")
    print(f"Failures: {result.failed}")

    if result.failed == 0:
        print("All doctests passed!")
        return True
    else:
        print(f"{result.failed} doctest(s) failed!")
        return False


def run_specific_function_doctest(function_name):
    """Run doctests for a specific function."""
    if not hasattr(calculator, function_name):
        print(f"Error: Function '{function_name}' not found in calculator module")
        return False

    func = getattr(calculator, function_name)
    print(f"Running doctests for {function_name}()...")
    print("-" * 40)

    # Create a temporary module-like object with just this function
    import types
    temp_module = types.ModuleType("temp")
    setattr(temp_module, function_name, func)

    result = doctest.testmod(temp_module, verbose=True)

    print("-" * 40)
    print(f"Tests run: {result.attempted}")
    print(f"Failures: {result.failed}")

    return result.failed == 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run doctest for specific function
        function_name = sys.argv[1]
        success = run_specific_function_doctest(function_name)
    else:
        # Run all doctests
        success = run_doctests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
