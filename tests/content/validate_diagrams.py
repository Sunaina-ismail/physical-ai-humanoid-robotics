#!/usr/bin/env python3
"""
Validate Mermaid diagrams in MDX files to ensure all diagrams have altText prop.

This script checks that:
1. All <MermaidDiagram> components have an altText prop
2. The altText prop is not empty
3. The altText is descriptive (not just placeholder text)
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


def find_mermaid_diagrams(file_path: Path) -> List[Tuple[int, str]]:
    """
    Find all MermaidDiagram components in an MDX file.

    Returns list of tuples (line_number, diagram_component_text)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match <MermaidDiagram> components
    # Handles both single-line and multi-line components
    pattern = r'(<MermaidDiagram[\s\S]*?>[\s\S]*?</MermaidDiagram>)'
    matches = re.findall(pattern, content)

    # Find line numbers for each match
    diagram_components = []
    for match in matches:
        # Find the start position of the match
        start_pos = content.find(match)
        if start_pos != -1:
            # Count newlines before this position to get line number
            line_number = content[:start_pos].count('\n') + 1
            diagram_components.append((line_number, match))

    return diagram_components


def check_alt_text(diagram_component: str) -> Tuple[bool, str]:
    """
    Check if a MermaidDiagram component has valid altText prop.

    Returns (is_valid, error_message)
    """
    # Look for altText prop in the component
    alt_text_match = re.search(r'altText\s*=\s*["\']([^"\']*)["\']', diagram_component)

    if not alt_text_match:
        return False, "Missing altText prop"

    alt_text = alt_text_match.group(1)

    if not alt_text.strip():
        return False, "altText prop is empty"

    # Check for common placeholder text
    placeholder_patterns = [
        r'^(diagram|figure|image|chart)\s+.*$',  # "diagram of X"
        r'^.*\s+(diagram|figure|image|chart)$',  # "X diagram"
        r'^\s*$',  # Just whitespace
        r'^[a-z].*$',  # Doesn't start with capital (likely not descriptive)
    ]

    for pattern in placeholder_patterns:
        if re.match(pattern, alt_text.strip(), re.IGNORECASE):
            return False, f"altText appears to be placeholder: '{alt_text}'"

    # Check minimum length (should be descriptive)
    if len(alt_text.strip()) < 10:
        return False, f"altText too short: '{alt_text}' (should be at least 10 characters)"

    return True, "Valid altText"


def validate_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate all MermaidDiagram components in a single file.

    Returns (is_valid, list_of_errors)
    """
    errors = []

    diagrams = find_mermaid_diagrams(file_path)

    if not diagrams:
        return True, []  # No diagrams to validate, so valid

    for line_number, diagram_component in diagrams:
        is_valid, error_msg = check_alt_text(diagram_component)
        if not is_valid:
            errors.append(
                f"{file_path}:{line_number}: {error_msg}\n"
                f"  Component: {diagram_component[:100]}..."
            )

    return len(errors) == 0, errors


def validate_directory(directory: Path) -> Tuple[bool, List[str]]:
    """
    Validate all MDX files in a directory for Mermaid diagram altText.

    Returns (is_valid, list_of_all_errors)
    """
    all_errors = []

    # Find all .mdx files in the directory and subdirectories
    mdx_files = list(directory.rglob("*.mdx"))

    for file_path in mdx_files:
        is_valid, errors = validate_file(file_path)
        if not is_valid:
            all_errors.extend(errors)

    return len(all_errors) == 0, all_errors


def main():
    parser = argparse.ArgumentParser(description="Validate Mermaid diagram altText in MDX files")
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
                print(f"PASS: {path} - All diagrams have valid altText")
            sys.exit(0)
        else:
            print(f"FAIL: {path} - Found {len(errors)} diagram validation error(s):")
            for error in errors:
                print(error)
            sys.exit(1)

    elif path.is_dir():
        # Validate directory
        is_valid, errors = validate_directory(path)

        if is_valid:
            if args.verbose:
                print(f"PASS: All diagrams in {path} have valid altText")
            sys.exit(0)
        else:
            print(f"FAIL: Found {len(errors)} diagram validation error(s) in {path}:")
            for error in errors:
                print(error)
                print()  # Extra line for readability
            sys.exit(1)

    else:
        print(f"Error: {path} is neither a file nor a directory", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()