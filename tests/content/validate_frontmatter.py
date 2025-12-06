#!/usr/bin/env python3
"""
Frontmatter Validator for Physical AI & Humanoid Robotics Textbook

Validates that all chapter MDX files contain correct frontmatter according to
the schema defined in contracts/chapter-frontmatter.yaml.

Usage:
    python tests/content/validate_frontmatter.py [--fix]

Arguments:
    --fix    Attempt to auto-fix common issues (adds missing required fields with placeholders)

Exit Codes:
    0: All chapters valid
    1: Validation errors found
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any
import argparse

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class FrontmatterValidator:
    """Validates MDX frontmatter against chapter schema."""

    def __init__(self, schema_path: str, docs_path: str):
        self.schema_path = Path(schema_path)
        self.docs_path = Path(docs_path)
        self.schema = self._load_schema()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def _load_schema(self) -> Dict[str, Any]:
        """Load the JSON Schema for chapter frontmatter."""
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {self.schema_path}")

        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _extract_frontmatter(self, content: str) -> Tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter from MDX content."""
        # Match frontmatter between --- delimiters
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return {}, content

        frontmatter_text = match.group(1)
        body = match.group(2)

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter or {}, body
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in frontmatter: {e}")
            return {}, body

    def _validate_required_fields(self, frontmatter: Dict[str, Any], file_path: Path) -> bool:
        """Check that all required fields are present."""
        required = self.schema.get('required', [])
        valid = True

        for field in required:
            if field not in frontmatter:
                self.errors.append(f"{file_path}: Missing required field '{field}'")
                valid = False

        return valid

    def _validate_tier_support(self, frontmatter: Dict[str, Any], file_path: Path) -> bool:
        """Validate tier_support structure and Tier A requirement."""
        valid = True

        if 'tier_support' not in frontmatter:
            return valid  # Handled by required field check

        tier_support = frontmatter['tier_support']

        if not isinstance(tier_support, dict):
            self.errors.append(f"{file_path}: tier_support must be an object")
            return False

        # Tier A must be true (Three-Tier Imperative)
        if tier_support.get('A') is not True:
            self.errors.append(
                f"{file_path}: tier_support.A must be true (Three-Tier Imperative - Tier A is mandatory)"
            )
            valid = False

        # Tier B and C are optional but must be boolean if present
        for tier in ['B', 'C']:
            if tier in tier_support and not isinstance(tier_support[tier], bool):
                self.errors.append(f"{file_path}: tier_support.{tier} must be boolean")
                valid = False

        return valid

    def _validate_learning_outcomes(self, frontmatter: Dict[str, Any], file_path: Path) -> bool:
        """Validate learning_outcomes structure."""
        valid = True

        if 'learning_outcomes' not in frontmatter:
            return valid

        outcomes = frontmatter['learning_outcomes']

        if not isinstance(outcomes, list):
            self.errors.append(f"{file_path}: learning_outcomes must be an array")
            return False

        if len(outcomes) < 3:
            self.warnings.append(
                f"{file_path}: Recommended to have at least 3 learning outcomes (found {len(outcomes)})"
            )

        for i, outcome in enumerate(outcomes):
            if not isinstance(outcome, str):
                self.errors.append(f"{file_path}: learning_outcomes[{i}] must be a string")
                valid = False
            elif len(outcome) < 10:
                self.warnings.append(
                    f"{file_path}: learning_outcomes[{i}] is very short ('{outcome}')"
                )

        return valid

    def _validate_estimated_time(self, frontmatter: Dict[str, Any], file_path: Path) -> bool:
        """Validate estimated_time is a positive integer."""
        valid = True

        if 'estimated_time' not in frontmatter:
            return valid

        time = frontmatter['estimated_time']

        if not isinstance(time, int) or time <= 0:
            self.errors.append(
                f"{file_path}: estimated_time must be a positive integer (minutes)"
            )
            valid = False

        return valid

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single MDX file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"{file_path}: Failed to read file: {e}")
            return False

        frontmatter, body = self._extract_frontmatter(content)

        if not frontmatter:
            self.errors.append(f"{file_path}: No frontmatter found (must start with ---)")
            return False

        # Run all validation checks
        valid = True
        valid &= self._validate_required_fields(frontmatter, file_path)
        valid &= self._validate_tier_support(frontmatter, file_path)
        valid &= self._validate_learning_outcomes(frontmatter, file_path)
        valid &= self._validate_estimated_time(frontmatter, file_path)

        return valid

    def validate_all(self) -> bool:
        """Validate all MDX files in the docs directory."""
        mdx_files = list(self.docs_path.rglob("*.mdx"))

        if not mdx_files:
            self.warnings.append(f"No .mdx files found in {self.docs_path}")
            return True

        print(f"📝 Validating {len(mdx_files)} chapter files...")

        all_valid = True
        for file_path in sorted(mdx_files):
            # Skip generated files or examples
            if 'node_modules' in str(file_path) or '.docusaurus' in str(file_path):
                continue

            valid = self.validate_file(file_path)
            if valid:
                print(f"  ✓ {file_path.relative_to(self.docs_path)}")
            else:
                print(f"  ✗ {file_path.relative_to(self.docs_path)}")
                all_valid = False

        return all_valid

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*60)

        if self.errors:
            print(f"❌ VALIDATION FAILED: {len(self.errors)} error(s) found")
            print("\nErrors:")
            for error in self.errors:
                print(f"  • {error}")
        else:
            print("✅ VALIDATION PASSED: All frontmatter valid")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"  • {warning}")

        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Validate chapter frontmatter against schema'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Attempt to auto-fix common issues (not implemented yet)'
    )
    args = parser.parse_args()

    # Paths relative to repo root
    repo_root = Path(__file__).parent.parent.parent
    schema_path = repo_root / 'specs' / '001-robotics-textbook' / 'contracts' / 'chapter-frontmatter.yaml'
    docs_path = repo_root / 'frontend' / 'docs'

    if not schema_path.exists():
        print(f"❌ Schema not found: {schema_path}")
        print("   Make sure contracts/chapter-frontmatter.yaml exists")
        sys.exit(1)

    if not docs_path.exists():
        print(f"❌ Docs directory not found: {docs_path}")
        sys.exit(1)

    validator = FrontmatterValidator(str(schema_path), str(docs_path))

    try:
        all_valid = validator.validate_all()
        validator.print_summary()

        if args.fix:
            print("\n⚠️  --fix flag not yet implemented")

        sys.exit(0 if all_valid else 1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
