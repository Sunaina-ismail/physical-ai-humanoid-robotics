#!/usr/bin/env python3
"""
Validate tier support in MDX files to ensure all chapters have Tier A support.

This script checks that:
1. All chapter MDX files have valid frontmatter
2. All chapters have tier_support.A = true (Tier A mandatory)
3. Tier support is properly structured according to contracts
"""

import re
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any


def extract_frontmatter(file_path: Path) -> Dict[str, Any]:
    """
    Extract YAML frontmatter from an MDX file.

    Returns the frontmatter as a dictionary, or empty dict if no frontmatter found.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for YAML frontmatter between --- delimiters
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)

    if frontmatter_match:
        frontmatter_yaml = frontmatter_match.group(1)
        try:
            return yaml.safe_load(frontmatter_yaml)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in frontmatter: {e}")

    return {}


def validate_tier_support(frontmatter: Dict[str, Any], file_path: Path) -> List[str]:
    """
    Validate tier support in the frontmatter.

    Returns list of validation errors.
    """
    errors = []

    # Check if tier_support exists
    if 'tier_support' not in frontmatter:
        errors.append(f"{file_path}: Missing 'tier_support' in frontmatter")
        return errors

    tier_support = frontmatter['tier_support']

    # Check if it's a dictionary/object
    if not isinstance(tier_support, dict):
        errors.append(f"{file_path}: 'tier_support' must be an object")
        return errors

    # Check that Tier A is present and true (mandatory)
    if 'A' not in tier_support:
        errors.append(f"{file_path}: Missing 'A' tier in tier_support (Tier A is mandatory)")
    elif tier_support['A'] is not True:
        errors.append(f"{file_path}: Tier A must be true (currently {tier_support['A']})")

    # Validate other tiers if present
    for tier in ['B', 'C']:
        if tier in tier_support and not isinstance(tier_support[tier], bool):
            errors.append(f"{file_path}: Tier {tier} must be boolean (true/false)")

    return errors


def validate_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate tier support in a single MDX file.

    Returns (is_valid, list_of_errors)
    """
    errors = []

    try:
        frontmatter = extract_frontmatter(file_path)
    except ValueError as e:
        return False, [f"{file_path}: {e}"]

    # Only validate files that have tier_support (chapters, not indexes)
    if 'tier_support' in frontmatter or 'chapter_number' in frontmatter:
        tier_errors = validate_tier_support(frontmatter, file_path)
        errors.extend(tier_errors)

    return len(errors) == 0, errors


def validate_directory(directory: Path) -> Tuple[bool, List[str]]:
    """
    Validate all MDX files in a directory for tier support.

    Returns (is_valid, list_of_all_errors)
    """
    all_errors = []

    # Find all .mdx files in the directory and subdirectories
    mdx_files = list(directory.rglob("*.mdx"))

    for file_path in mdx_files:
        # Skip if this looks like a module index file (doesn't need tier support)
        if 'index.mdx' in str(file_path) or 'index.md' in str(file_path):
            continue

        is_valid, errors = validate_file(file_path)
        if not is_valid:
            all_errors.extend(errors)

    return len(all_errors) == 0, all_errors


def main():
    parser = argparse.ArgumentParser(description="Validate tier support in MDX files")
    parser.add_argument("path", help="Path to MDX file or directory to validate")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")

    args = parser.parse_args()

    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path {path} does not exist", file=sys.stderr)
        sys.exit(1)

    if path.is_file():
        # Validate single file
        if path.suffix.lower() != '.mdx':
            print(f"Error: File {path} is not an MDX file", file=sys.stderr)
            sys.exit(1)

        is_valid, errors = validate_file(path)

        if is_valid:
            if args.verbose:
                print(f"PASS: {path} - Tier support validation passed")
            sys.exit(0)
        else:
            print(f"FAIL: {path} - Found {len(errors)} tier validation error(s):")
            for error in errors:
                print(error)
            sys.exit(1)

    elif path.is_dir():
        # Validate directory
        is_valid, errors = validate_directory(path)

        if is_valid:
            if args.verbose:
                print(f"PASS: All tier validations passed in {path}")
            sys.exit(0)
        else:
            print(f"FAIL: Found {len(errors)} tier validation error(s) in {path}:")
            for error in errors:
                print(error)
                print()  # Extra line for readability
            sys.exit(1)

    else:
        print(f"Error: {path} is neither a file nor a directory", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()