import os
from pathlib import Path
from coverage import Coverage

class CoverageReporter:
    def __init__(self, source_directory: str, test_directory: str, report_file: str = "coverage_report.txt"):
        """
        Initializes the CoverageReporter class.

        Args:
            source_directory: Directory containing the source code to be analyzed.
            test_directory: Directory containing the test files.
            report_file: Path to save the generated report.
        """
        self.source_directory = Path(source_directory)
        self.test_directory = Path(test_directory)
        self.report_file = Path(report_file)
        self.coverage = Coverage(source=[str(self.source_directory)], branch=True)

    def run_tests_and_collect_coverage(self):
        """
        Executes the test files and collects coverage data.
        """
        self.coverage.start()

        test_files = list(self.test_directory.glob("test_*.py"))

        for test_file in test_files:
            print(f"Running tests in {test_file}")
            os.system(f"coverage run -m pytest {test_file} --disable-warnings")

        self.coverage.stop()
        self.coverage.save()

    def generate_text_report(self):
        """
        Generates a textual coverage report and saves it to the specified file.
        """
        with open(self.report_file, "w") as report:
            self.coverage.report(file=report, show_missing=True)

        print(f"Coverage report generated at {self.report_file}")

    def print_report_to_console(self):
        """
        Prints the coverage report directly to the console.
        """
        self.coverage.report(show_missing=True)

if __name__ == "__main__":
    source_dir = "./fastapi"
    # source_dir = "./fastapi"
    test_dir = "./fastapi/tests"
    report_file = "coverage_report.txt"

    reporter = CoverageReporter(source_directory=source_dir, test_directory=test_dir, report_file=report_file)

    print("Running tests and collecting coverage...")
    reporter.run_tests_and_collect_coverage()

    print("Generating coverage report...")
    reporter.generate_text_report()
    reporter.print_report_to_console()
