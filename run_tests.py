#!/usr/bin/env python3
"""
Test runner script for Real Estate MCP Server
"""

import argparse
import subprocess
import sys


def run_tests(test_type="all", verbose=False, coverage=False):
    """Run tests with specified options"""

    cmd = ["python", "-m", "pytest"]

    # Add test path based on type
    if test_type == "unit":
        cmd.append("tests/unit/")
    elif test_type == "integration":
        cmd.append("tests/integration/")
    elif test_type == "all":
        cmd.append("tests/")
    else:
        cmd.append(f"tests/{test_type}")

    # Add verbosity
    if verbose:
        cmd.append("-v")

    # Add coverage
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term-missing"])

    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description="Run Real Estate MCP Server tests")
    parser.add_argument(
        "test_type",
        nargs="?",
        default="all",
        choices=[
            "all",
            "unit",
            "integration",
            "property",
            "agent",
            "market",
            "client",
            "area",
            "system",
            "resources",
            "prompts",
        ],
        help="Type of tests to run",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "-c", "--coverage", action="store_true", help="Generate coverage report"
    )

    args = parser.parse_args()

    print("🏠 Real Estate MCP Server Test Runner")
    print("=" * 50)

    exit_code = run_tests(args.test_type, args.verbose, args.coverage)

    if exit_code == 0:
        print("\n✅ All tests passed!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
