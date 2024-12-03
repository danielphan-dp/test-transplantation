import sys
import json
import pytest
import inspect
import traceback
from pathlib import Path
from typing import Dict, Set, List
from contextlib import contextmanager
from .collect_unit_tests import collect_tests, TestCollection
import click


class MethodCallTracer:
    def __init__(self, package_name: str):
        self.package_name = package_name
        self.calls = []
        self.current_test = None
        self.ignore_paths = {"site-packages", "dist-packages", "lib/python"}

    def should_trace(self, filename: str) -> bool:
        """Check if this file should be traced"""
        if not filename:
            return False
        return self.package_name in filename and not any(p in filename for p in self.ignore_paths)

    def trace_calls(self, frame, event, arg):
        """Trace function calls"""
        if event != "call":
            return

        # Add decorator handling
        if event == "call" and frame.f_code.co_name == "wrapper":
            # Try to get the original function name from closure
            if frame.f_code.co_freevars:
                for var in frame.f_code.co_freevars:
                    if var in frame.f_locals:
                        original_func = frame.f_locals[var]
                        if hasattr(original_func, "__name__"):
                            func_name = original_func.__name__
                            # Record the decorator call
                            call_info = {
                                "function": func_name,
                                "filename": frame.f_code.co_filename,
                                "line": frame.f_lineno,
                                "caller": "decorator",
                            }
                            self.calls.append(call_info)

        # Get call info
        code = frame.f_code
        filename = code.co_filename

        if not self.should_trace(filename):
            return

        func_name = code.co_name
        # Get the class name if this is a method
        if "self" in frame.f_locals:
            cls = frame.f_locals["self"].__class__
            func_name = f"{cls.__name__}.{func_name}"

        lineno = frame.f_lineno

        call_info = {
            "function": func_name,
            "filename": filename,
            "line": lineno,
            "caller": traceback.extract_stack()[-3].name,  # Get the calling function
        }

        self.calls.append(call_info)
        return self.trace_calls

    @contextmanager
    def trace_context(self, test_name: str):
        """Context manager for tracing"""
        self.current_test = test_name
        self.calls = []
        old_trace = sys.gettrace()
        sys.settrace(self.trace_calls)
        try:
            yield
        finally:
            sys.settrace(old_trace)


class TestAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.package_name = self.repo_path.name
        self.tests_dir = self.repo_path / "tests"
        self.tracer = MethodCallTracer(self.package_name)

    def run_static_analysis(self) -> TestCollection:
        """Run static analysis using collect_unit_tests"""
        return collect_tests(str(self.tests_dir), set())

    def run_test_with_tracing(self, test_path: str, test_name: str) -> List[Dict]:
        """Run a specific test while tracing method calls"""
        with self.tracer.trace_context(test_name):
            # Create a custom pytest args to run just this test
            test_id = f"{test_path}::{test_name}"
            pytest.main([test_id, "-v"])
        return self.tracer.calls

    def analyze_test(self, test_case: dict) -> Dict:
        """Analyze a single test case using both static and dynamic analysis"""
        test_path = test_case["file_path"]
        test_name = test_case["name"]

        # Static analysis results
        static_methods = [m["name"] for m in test_case["methods_under_test"]]

        # Dynamic analysis - trace actual method calls
        traced_calls = self.run_test_with_tracing(test_path, test_name)

        # Filter out test framework calls
        actual_methods = [
            call
            for call in traced_calls
            if not call["function"].startswith("test_") and not call["function"].startswith("pytest_")
        ]

        return {
            "test_name": test_name,
            "test_file": test_path,
            "static_methods": static_methods,
            "dynamic_methods": actual_methods,
            "assertions": test_case["assertions"],
            "mocks": test_case["mocks"],
        }

    def print_analysis(self, analysis: Dict):
        """Print the analysis results in a readable format"""
        print("\n" + "=" * 80)
        print(f"Test: {analysis['test_name']}")
        print(f"File: {analysis['test_file']}")

        print("\nMethods Under Test (Static Analysis):")
        for method in analysis["static_methods"]:
            print(f"  - {method}")

        print("\nMethods Actually Called (Dynamic Analysis):")
        seen_methods = set()
        for call in analysis["dynamic_methods"]:
            method_sig = f"{call['function']} ({Path(call['filename']).name}:{call['line']})"
            if method_sig not in seen_methods:
                print(f"  - {method_sig}")
                print(f"    Called by: {call['caller']}")
                seen_methods.add(method_sig)

        print("\nAssertions:")
        for assertion in analysis["assertions"]:
            print(f"  - {assertion}")

        print("\nMocks:")
        for mock in analysis["mocks"]:
            print(f"  - {mock}")
        print("=" * 80)


@click.command()
@click.option(
    "--input-dir",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Repository path to analyze",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    required=True,
    help="Directory to store analysis results",
)
def main(input_dir: str, output_dir: str):
    """Analyze unit tests in the given repository."""
    analyzer = TestAnalyzer(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Run static analysis
    click.echo("Running static analysis...")
    test_collection = analyzer.run_static_analysis()

    # Analyze each test
    click.echo("\nAnalyzing tests...")
    for test_case in test_collection.tests:
        try:
            analysis = analyzer.analyze_test(test_case.model_dump())
            analyzer.print_analysis(analysis)

            # Save detailed results
            output_file = output_path / f"test_analysis_{test_case.name}.json"
            with open(output_file, "w") as f:
                json.dump(analysis, f, indent=2)
            click.echo(f"Detailed analysis saved to: {output_file}")
        except Exception as e:
            click.echo(f"Error analyzing test {test_case.name}: {str(e)}", err=True)


if __name__ == "__main__":
    main()
