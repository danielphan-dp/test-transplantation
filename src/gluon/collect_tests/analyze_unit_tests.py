import sys
import os
import logging

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import pytest
import inspect
import traceback
import threading
from pathlib import Path
from typing import Dict, List, Optional
from contextlib import contextmanager
from gluon.collect_tests.collect_unit_tests import collect_tests, TestCollection
import click
import warnings
import subprocess


logger = logging.getLogger(__name__)


class MethodCallTracer:
    def __init__(self, package_path: str):
        self.package_path = package_path
        self.calls = []
        self.ignore_paths = {"site-packages", "dist-packages", "lib/python"}
        self.current_thread = threading.current_thread()

    def should_trace(self, filename: str) -> bool:
        """Check if this file should be traced"""
        if not filename:
            return False
        filename = os.path.normpath(filename)
        package_path = os.path.normpath(self.package_path)
        return filename.startswith(package_path) and not any(p in filename for p in self.ignore_paths)

    def trace_calls(self, frame, event, arg):
        """Trace function calls"""
        if threading.current_thread() != self.current_thread:
            # Ignore calls from threads other than the current one
            return

        if event != "call":
            return

        code = frame.f_code
        filename = code.co_filename

        if not self.should_trace(filename):
            return

        func_name = code.co_name

        # Get the class name if this is a method
        if "self" in frame.f_locals:
            cls = frame.f_locals["self"].__class__
            func_name = f"{cls.__name__}.{func_name}"
        elif "cls" in frame.f_locals:
            cls = frame.f_locals["cls"]
            func_name = f"{cls.__name__}.{func_name}"

        lineno = frame.f_lineno

        # Get the caller function name
        caller_frame = frame.f_back
        if caller_frame:
            caller_name = caller_frame.f_code.co_name
        else:
            caller_name = None

        call_info = {
            "function": func_name,
            "filename": filename,
            "line": lineno,
            "caller": caller_name,
        }

        self.calls.append(call_info)
        return self.trace_calls

    @contextmanager
    def trace_context(self, test_name: str):
        """Context manager for tracing"""
        self.calls = []
        old_trace = sys.gettrace()
        sys.settrace(self.trace_calls)
        try:
            yield
        finally:
            sys.settrace(old_trace)


class TestAnalyzer:
    def __init__(self, repo_path: str, tests_dir: Optional[str] = None):
        self.repo_path = Path(repo_path)
        self.package_path = str(self.repo_path.resolve())
        self.tests_dir = Path(tests_dir) if tests_dir else self.repo_path
        self.tracer = MethodCallTracer(self.package_path)

    def run_static_analysis(self) -> TestCollection:
        """Run static analysis using collect_unit_tests"""
        return collect_tests(str(self.tests_dir), set())

    def run_test_with_tracing(self, test_case: Dict) -> List[Dict]:
        """Runs the test case with tracing and returns the collected method calls."""
        test_path = Path(test_case["file_path"]).resolve()
        test_name = test_case["name"]
        test_identifier = f"{test_path}::{test_name}"

        # Find the project root (where the tests directory is located)
        project_root = test_path
        while project_root.name != "tests" and project_root.parent != project_root:
            project_root = project_root.parent
        if project_root.name == "tests":
            project_root = project_root.parent

        # Set up environment with correct PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{str(project_root)}:{env.get('PYTHONPATH', '')}"

        cmd = [
            "pytest",
            str(test_identifier),
            "-v",  # verbose output
            "--no-header",  # remove pytest header
            "--tb=short",  # shorter traceback
        ]

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                cwd=str(project_root),
            )

            # Consider the test successful if it passes (return code 0) or has expected failures
            success = result.returncode == 0 or "XFAIL" in result.stdout

            if not success:
                logger.warning(f"Test {test_identifier} failed or had errors.")
                logger.debug(f"STDOUT:\n{result.stdout}")
                logger.debug(f"STDERR:\n{result.stderr}")

            # Extract static method calls from the test case
            static_calls = []
            for method in test_case.get("methods_under_test", []):
                static_calls.append(
                    {
                        "function": method["name"],
                        "filename": method.get("file_path", ""),
                        "line": method.get("line_number", 0),
                        "caller": test_name,
                    }
                )

            return static_calls, success

        except Exception as e:
            logger.warning(f"Error running test {test_identifier}: {str(e)}")
            return [], False

    def analyze_test(self, test_case: Dict) -> Dict:
        """Analyze a single test case using both static and dynamic analysis"""
        try:
            # Static analysis results
            static_methods = []
            for method in test_case["methods_under_test"]:
                # Include the method name and its source code
                static_methods.append(
                    {
                        "name": method["name"],
                        "source_code": method.get("body", ""),  # Include the source code
                        "file_path": method.get("file_path", ""),
                        "line_number": method.get("line_number", 0),
                    }
                )

            # Run the test and get static calls and success status
            traced_calls, success = self.run_test_with_tracing(test_case)

            return {
                "test_name": test_case["name"],
                "test_file": test_case["file_path"],
                "static_methods": static_methods,  # Now includes source code
                "dynamic_methods": traced_calls,
                "assertions": test_case.get("assertions", []),
                "mocks": test_case.get("mocks", []),
                "success": success,
                "test_source_code": test_case.get("source_code", ""),  # Also include test source code
            }
        except Exception as e:
            logger.warning(f"Error analyzing test {test_case['name']}: {str(e)}")
            return {
                "test_name": test_case["name"],
                "test_file": test_case["file_path"],
                "static_methods": [],
                "dynamic_methods": [],
                "assertions": [],
                "mocks": [],
                "success": False,
                "error": str(e),
                "test_source_code": test_case.get("source_code", ""),
            }

    def print_analysis(self, analysis: Dict):
        """Print the analysis results in a readable format"""
        print("\n" + "=" * 80)
        print(f"Test: {analysis['test_name']}")
        print(f"File: {analysis['test_file']}")

        print("\nMethods Under Test (Static Analysis):")
        for method in analysis["static_methods"]:
            print(f"  - {method['name']} ({Path(method['file_path']).name}:{method['line_number']})")
            if method.get("source_code"):
                print("    Source code:")
                for line in method["source_code"].splitlines():
                    print(f"      {line}")

        print("\nMethods Actually Called (Dynamic Analysis):")
        seen_methods = set()
        for call in analysis["dynamic_methods"]:
            method_sig = f"{call['function']} ({Path(call['filename']).name}:{call['line']})"
            if method_sig not in seen_methods:
                print(f"  - {method_sig}")
                print(f"    Called by: {call['caller']}")
                seen_methods.add(method_sig)

        print("\nTest Source Code:")
        if analysis.get("test_source_code"):
            for line in analysis["test_source_code"].splitlines():
                print(f"  {line}")

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
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    analyzer = TestAnalyzer(input_dir, tests_dir=input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Run static analysis
    click.echo("Running static analysis...")
    test_collection = analyzer.run_static_analysis()

    # Analyze each test
    click.echo("\nAnalyzing tests...")
    total_tests = len(test_collection.tests)
    logger.info(f"Total tests to analyze: {total_tests}")
    for idx, test_case in enumerate(test_collection.tests, start=1):
        logger.info(f"Analyzing test {idx}/{total_tests}: {test_case.name}")
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
            traceback.print_exc()


if __name__ == "__main__":
    main()
