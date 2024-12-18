import os
import sys
import pytest
from pathlib import Path
from typing import List, Tuple

class TestAnalyzer:
    def __init__(self, test_directory: str):
        """
        Initialize the TestAnalyzer.

        Args:
            test_directory: Directory containing the test files.
        """
        self.test_directory = Path(test_directory)

    def find_test_files(self) -> List[Path]:
        """Find all Python test files in the test directory."""
        return list(self.test_directory.glob("test_*.py"))

    def validate_test_file(self, test_file: Path) -> Tuple[bool, str]:
        """
        Validate a single test file using pytest.

        Args:
            test_file: Path to the test file.

        Returns:
            Tuple of (is_valid, message).
        """
        try:
            result = pytest.main([
                str(test_file),
                "--maxfail=1",
                "--disable-warnings",
                "--tb=short",
            ])
            if result == pytest.ExitCode.OK:
                return True, "Valid test file."
            elif result == pytest.ExitCode.TESTS_FAILED:
                return False, "Tests failed."
            else:
                return False, f"Error running tests (exit code: {result})."
        except Exception as e:
            return False, f"Exception occurred: {e}"

    def analyze_tests(self):
        """
        Analyze all test files for validity.

        Returns:
            A summary report containing:
                - Number of valid test files.
                - Number of invalid test files.
                - Percentage of valid test files.
        """
        test_files = self.find_test_files()
        total_files = len(test_files)
        valid_files = 0
        invalid_files = 0

        for test_file in test_files:
            is_valid, _ = self.validate_test_file(test_file)
            if is_valid:
                valid_files += 1
            else:
                invalid_files += 1

        percentage_valid = (valid_files / total_files * 100) if total_files > 0 else 0

        return {
            "total_files": total_files,
            "valid_files": valid_files,
            "invalid_files": invalid_files,
            "percentage_valid": round(percentage_valid, 2),
        }

if __name__ == "__main__":
    test_directory = "./uvicorn/bl_tests"
    analyzer = TestAnalyzer(test_directory)

    result = analyzer.analyze_tests()

    print("\nTest Validation Summary")
    print("========================")
    print(f"Total Test Files: {result['total_files']}")
    print(f"Valid Test Files: {result['valid_files']}")
    print(f"Invalid Test Files: {result['invalid_files']}")
    print(f"Percentage Valid: {result['percentage_valid']}%")
