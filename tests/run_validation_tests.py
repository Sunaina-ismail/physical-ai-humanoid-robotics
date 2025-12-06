#!/usr/bin/env python3
"""
Simple test runner for content validation tests.

This script runs all content validation tests to ensure they pass.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("PASS: PASSED\n")
            return True
        else:
            print("FAIL: FAILED")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            print()
            return False
    except subprocess.TimeoutExpired:
        print("FAIL: TIMEOUT")
        print()
        return False
    except Exception as e:
        print(f"FAIL: ERROR: {e}")
        print()
        return False


def main():
    """Run all validation tests."""
    print("Running all content validation tests...\n")

    all_passed = True

    # Test diagram validation on a sample file
    success = run_command(
        ["python", "tests/content/validate_diagrams.py", "frontend/docs/module-1/week-1/ch01-physical-ai-intro.mdx"],
        "Diagram validation on ch01-physical-ai-intro.mdx"
    )
    all_passed = all_passed and success

    # Test diagram validation on a directory
    success = run_command(
        ["python", "tests/content/validate_diagrams.py", "frontend/docs/module-1/week-1/"],
        "Diagram validation on module-1/week-1/"
    )
    all_passed = all_passed and success

    # Test tier validation on a sample file
    success = run_command(
        ["python", "tests/content/validate_tiers.py", "frontend/docs/module-1/week-1/ch01-physical-ai-intro.mdx"],
        "Tier validation on ch01-physical-ai-intro.mdx"
    )
    all_passed = all_passed and success

    # Test tier validation on a directory
    success = run_command(
        ["python", "tests/content/validate_tiers.py", "frontend/docs/module-1/week-1/"],
        "Tier validation on module-1/week-1/"
    )
    all_passed = all_passed and success

    # Test on the chapter we fixed (chapter 16)
    success = run_command(
        ["python", "tests/content/validate_diagrams.py", "frontend/docs/module-3/week-8/ch16-isaac-sim-concepts.mdx"],
        "Diagram validation on ch16-isaac-sim-concepts.mdx (the fixed chapter)"
    )
    all_passed = all_passed and success

    success = run_command(
        ["python", "tests/content/validate_tiers.py", "frontend/docs/module-3/week-8/ch16-isaac-sim-concepts.mdx"],
        "Tier validation on ch16-isaac-sim-concepts.mdx (the fixed chapter)"
    )
    all_passed = all_passed and success

    print("="*50)
    if all_passed:
        print("ALL TESTS PASSED!")
        print("All validation scripts are working correctly.")
        return 0
    else:
        print("SOME TESTS FAILED!")
        print("Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())