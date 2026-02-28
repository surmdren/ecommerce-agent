#!/usr/bin/env python3
"""
Intelligent Test Selector for Bug Fixer Skill

Analyzes code changes and bug impact to determine which test types to run.
Returns a list of recommended test types: unit, api, integration, e2e
"""

import sys
import json
from typing import List, Set
from pathlib import Path


class TestSelector:
    """
    Determines which tests to run based on:
    1. Modified file paths and patterns
    2. Bug severity and impact description
    3. Code change patterns (e.g., API changes, UI changes, business logic)
    """

    # File pattern mappings to test types
    FILE_PATTERNS = {
        "unit": [
            r".*\.(py|js|ts|go|java)$",  # Source code files
            r".*/models/.*",
            r".*/services/.*",
            r".*/utils/.*",
            r".*/helpers/.*",
        ],
        "api": [
            r".*/api/.*",
            r".*/routes/.*",
            r".*/controllers/.*",
            r".*/handlers/.*",
            r".*/endpoints/.*",
        ],
        "integration": [
            r".*/api/.*",
            r".*/database/.*",
            r".*/repositories/.*",
            r".*/middleware/.*",
            r".*/services/.*",
        ],
        "e2e": [
            r".*/views/.*",
            r".*/components/.*",
            r".*/pages/.*",
            r".*/frontend/.*",
            r".*/ui/.*",
            r".*\.(jsx|tsx|vue|svelte)$",
        ],
    }

    # Keywords in bug description that suggest test types
    DESCRIPTION_KEYWORDS = {
        "unit": ["logic", "calculation", "algorithm", "validation", "parse", "format"],
        "api": ["endpoint", "api", "request", "response", "status code", "header"],
        "integration": ["workflow", "integration", "multiple", "interaction", "database", "external"],
        "e2e": ["user", "ui", "interface", "button", "form", "page", "flow", "journey"],
    }

    def select_tests(
        self,
        modified_files: List[str],
        bug_description: str,
        severity: str = "medium"
    ) -> List[str]:
        """
        Select test types based on modified files and bug context

        Args:
            modified_files: List of file paths that were changed
            bug_description: Bug description text
            severity: Bug severity (low/medium/high/critical)

        Returns:
            List of test types to run (e.g., ['unit', 'api', 'integration'])
        """
        test_scores: dict = {"unit": 0, "api": 0, "integration": 0, "e2e": 0}

        # Score based on file patterns
        for file_path in modified_files:
            for test_type, patterns in self.FILE_PATTERNS.items():
                for pattern in patterns:
                    if self._matches_pattern(file_path, pattern):
                        test_scores[test_type] += 2
                        break

        # Score based on bug description keywords
        description_lower = bug_description.lower()
        for test_type, keywords in self.DESCRIPTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    test_scores[test_type] += 1

        # Severity-based adjustments
        if severity in ["high", "critical"]:
            # High severity bugs should run more comprehensive tests
            test_scores["integration"] += 2
            test_scores["e2e"] += 2

        # Always run unit tests if source code changed
        if any(f.endswith((".py", ".js", ".ts", ".go", ".java")) for f in modified_files):
            test_scores["unit"] += 3

        # Select tests with score > threshold
        threshold = 2
        selected_tests = [
            test_type for test_type, score in test_scores.items()
            if score >= threshold
        ]

        # Ensure at least unit tests run
        if not selected_tests:
            selected_tests = ["unit"]

        return sorted(selected_tests)

    @staticmethod
    def _matches_pattern(file_path: str, pattern: str) -> bool:
        """Simple pattern matching (supports basic wildcards)"""
        import re
        return bool(re.match(pattern, file_path))


def main():
    if len(sys.argv) < 3:
        print("Usage: python test_selector.py <files_json> <description> [severity]")
        print('Example: python test_selector.py \'["src/api/users.py"]\' "API endpoint error" high')
        sys.exit(1)

    try:
        modified_files = json.loads(sys.argv[1])
        bug_description = sys.argv[2]
        severity = sys.argv[3] if len(sys.argv) >= 4 else "medium"

        selector = TestSelector()
        selected_tests = selector.select_tests(modified_files, bug_description, severity)

        print(json.dumps({"tests": selected_tests}))

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
