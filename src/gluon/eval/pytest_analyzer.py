import os
import sys
import coverage
import pytest
from typing import Dict, List, Tuple
from pathlib import Path

class TestAnalyzer:
    def __init__(self, test_directory: str, source_directory: str):
        """
        Initialize the test analyzer.
        
        Args:
            test_directory: Directory containing generated test files
            source_directory: Directory containing source code to be tested
        """
        self.test_directory = Path(test_directory)
        self.source_directory = Path(source_directory)
        self.cov = coverage.Coverage(branch=True)
        
    def find_test_files(self) -> List[Path]:
        """Find all Python test files in the test directory."""
        return list(self.test_directory.glob("test_*.py"))
    
    def validate_test_file(self, test_file: Path) -> Tuple[bool, str]:
        """
        Check if a test file is valid and can be executed using pytest.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            result = pytest.main([
                str(test_file),
                "-v",
                "--capture=no",
                "--disable-warnings"
            ])
            
            if result == pytest.ExitCode.OK:
                return True, "Test file is valid"
            elif result == pytest.ExitCode.TESTS_FAILED:
                return False, f"Tests in {test_file.name} failed"
            else:
                return False, f"Error running {test_file.name}: pytest exit code {result}"
                
        except Exception as e:
            return False, f"Error in {test_file.name}: {str(e)}"
    
    def run_coverage_analysis(self) -> Dict:
        """
        Run coverage analysis on all valid test files using pytest.
        
        Returns:
            Dictionary containing coverage metrics
        """
        # Start coverage collection
        self.cov.start()
        
        # Run all test files with pytest
        test_files = [str(f) for f in self.find_test_files()]
        pytest.main([
            *test_files,
            "--capture=no",
            "--disable-warnings"
        ])
        
        # Stop coverage collection
        self.cov.stop()
        
        # Get coverage data
        total_statements = 0
        total_missing = 0
        total_branches = 0
        total_missing_branches = 0

        for filename in self.cov.get_data().measured_files():
            analysis = self.cov._analyze(filename)
            total_statements += len(analysis.statements)
            total_missing += len(analysis.missing)
            
            if hasattr(analysis, 'branches') and analysis.branches:
                total_branches += len(analysis.branches)
                total_missing_branches += len(analysis.missing_branches)

        # Calculate coverage percentages
        line_coverage = ((total_statements - total_missing) / total_statements * 100) if total_statements > 0 else 0
        branch_coverage = ((total_branches - total_missing_branches) / total_branches * 100) if total_branches > 0 else 0
        
        return {
            "line_coverage": round(line_coverage, 2),
            "branch_coverage": round(branch_coverage, 2),
            "total_statements": total_statements,
            "covered_statements": total_statements - total_missing,
            "total_branches": total_branches,
            "covered_branches": total_branches - total_missing_branches
        }
    
    @staticmethod
    def collect_test_outcomes(test_file: Path) -> Dict:
        """
        Collect detailed test outcomes for a specific file using pytest.
        
        Returns:
            Dictionary containing test results
        """
        class TestResultCollector:
            def __init__(self):
                self.passed = []
                self.failed = []
                self.errors = []
                self.skipped = []

            def pytest_runtest_logreport(self, report):
                if report.when == 'call':
                    if report.passed:
                        self.passed.append(report.nodeid)
                    elif report.failed:
                        self.failed.append(report.nodeid)
                    elif report.skipped:
                        self.skipped.append(report.nodeid)
                elif report.when == 'setup' and report.failed:
                    self.errors.append(report.nodeid)

        collector = TestResultCollector()
        pytest.main([
            str(test_file),
            "-v",
            "--capture=no"
        ], plugins=[collector])

        return {
            "passed": len(collector.passed),
            "failed": len(collector.failed),
            "errors": len(collector.errors),
            "skipped": len(collector.skipped)
        }
    
    def generate_report(self) -> str:
        """Generate a complete analysis report."""
        report = []
        report.append("Test Coverage Analysis Report")
        report.append("===========================\n")
        
        # Test file validation and detailed results
        report.append("Test File Results:")
        total_tests = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
        
        for test_file in self.find_test_files():
            is_valid, message = self.validate_test_file(test_file)
            status = "✓" if is_valid else "✗"
            report.append(f"\n{status} {test_file.name}:")
            report.append(f"  Status: {message}")
            
            # Collect detailed test results
            results = self.collect_test_outcomes(test_file)
            report.append("  Test Results:")
            report.append(f"    Passed: {results['passed']}")
            report.append(f"    Failed: {results['failed']}")
            report.append(f"    Errors: {results['errors']}")
            report.append(f"    Skipped: {results['skipped']}")
            
            # Update totals
            for key in total_tests:
                total_tests[key] += results[key]
        
        # Overall test summary
        report.append("\nOverall Test Summary:")
        report.append(f"Total Tests Passed: {total_tests['passed']}")
        report.append(f"Total Tests Failed: {total_tests['failed']}")
        report.append(f"Total Test Errors: {total_tests['errors']}")
        report.append(f"Total Tests Skipped: {total_tests['skipped']}")
        
        # Coverage analysis
        report.append("\nCoverage Analysis:")
        coverage_metrics = self.run_coverage_analysis()
        report.append(f"Line Coverage: {coverage_metrics['line_coverage']}%")
        report.append(f"Branch Coverage: {coverage_metrics['branch_coverage']}%")
        report.append(f"Total Statements: {coverage_metrics['total_statements']}")
        report.append(f"Covered Statements: {coverage_metrics['covered_statements']}")
        report.append(f"Total Branches: {coverage_metrics['total_branches']}")
        report.append(f"Covered Branches: {coverage_metrics['covered_branches']}")
        
        return "\n".join(report)


if __name__ == "__main__":
    
    analyzer = TestAnalyzer(
        test_directory="./fastapi/tests",
        source_directory="./fastapi"
    )
    # print(analyzer.generate_report())

    # Output the report to a file
    with open("test_coverage_report.txt", "w") as file:
        file.write(analyzer.generate_report())