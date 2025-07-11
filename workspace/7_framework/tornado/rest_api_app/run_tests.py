#!/usr/bin/env python3
"""
Test runner script for Tornado REST API application.

This script provides a convenient way to run tests with different options.
"""

import sys
import unittest
import subprocess
import os

def run_tests(verbosity=2, pattern="test_*.py"):
    """Run the test suite with specified verbosity level."""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern=pattern)

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return result.wasSuccessful()

def run_with_coverage():
    """Run tests with coverage report if coverage is installed."""
    try:
        import coverage
        cov = coverage.Coverage()
        cov.start()

        # Run tests
        success = run_tests(verbosity=1)

        cov.stop()
        cov.save()

        print("\n" + "="*50)
        print("COVERAGE REPORT")
        print("="*50)
        cov.report()

        return success

    except ImportError:
        print("Coverage not installed. Install with: pip install coverage")
        print("Running tests without coverage...")
        return run_tests()

def main():
    """Main entry point for the test runner."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "coverage":
            success = run_with_coverage()
        elif command == "quiet":
            success = run_tests(verbosity=1)
        elif command == "verbose":
            success = run_tests(verbosity=2)
        elif command == "help":
            print_help()
            return
        else:
            print(f"Unknown command: {command}")
            print_help()
            return
    else:
        # Default: run with normal verbosity
        success = run_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)

def print_help():
    """Print help information."""
    print("Tornado REST API Test Runner")
    print("=" * 30)
    print("Usage: python run_tests.py [command]")
    print("\nCommands:")
    print("  (no command)  - Run tests with normal verbosity")
    print("  verbose       - Run tests with verbose output")
    print("  quiet         - Run tests with minimal output")
    print("  coverage      - Run tests with coverage report")
    print("  help          - Show this help message")
    print("\nExamples:")
    print("  python run_tests.py")
    print("  python run_tests.py verbose")
    print("  python run_tests.py coverage")

if __name__ == "__main__":
    main()
