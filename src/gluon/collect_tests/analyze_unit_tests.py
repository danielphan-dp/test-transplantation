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
from collections import Counter
import statistics
from typing import Dict, Set


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
                # Try to find the source code for this method
                source_code = ""
                file_path = method.get("file_path", "")
                if file_path and os.path.exists(file_path):
                    try:
                        with open(file_path, "r") as f:
                            source_lines = f.readlines()
                        line_number = method.get("line_number", 0)
                        if line_number > 0:
                            # Find the start of the method (including decorators)
                            start_line = line_number - 1
                            while start_line > 0:
                                line = source_lines[start_line - 1].strip()
                                if line.startswith("@"):
                                    start_line -= 1
                                else:
                                    break

                            # Find the end of the method by looking for the next non-indented line
                            base_indent = len(source_lines[line_number - 1]) - len(
                                source_lines[line_number - 1].lstrip()
                            )
                            end_line = line_number
                            while end_line < len(source_lines):
                                line = source_lines[end_line]
                                if line.strip() and len(line) - len(line.lstrip()) <= base_indent:
                                    break
                                end_line += 1

                            source_code = "".join(source_lines[start_line:end_line])
                    except Exception as e:
                        logger.warning(f"Could not extract source code for {method['name']}: {e}")

                static_calls.append(
                    {
                        "function": method["name"],
                        "filename": file_path,
                        "line": method.get("line_number", 0),
                        "caller": test_name,
                        "source_code": source_code,
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
                source_code = ""
                file_path = method.get("file_path", "")
                if file_path and os.path.exists(file_path):
                    try:
                        with open(file_path, "r") as f:
                            source_lines = f.readlines()
                        line_number = method.get("line_number", 0)
                        if line_number > 0:
                            # Extract full method source code
                            method_lines = []
                            i = line_number - 1
                            # Get the method signature
                            method_lines.append(source_lines[i].rstrip())
                            # Get the method body
                            i += 1
                            while i < len(source_lines) and (
                                source_lines[i].strip() and source_lines[i].startswith(" " * 4)
                            ):
                                method_lines.append(source_lines[i].rstrip())
                                i += 1
                            source_code = "\n".join(method_lines)
                    except Exception as e:
                        logger.warning(f"Could not extract source code for {method['name']}: {e}")

                static_methods.append(
                    {
                        "name": method["name"],
                        "source_code": source_code,
                        "file_path": method.get("file_path", ""),
                        "line_number": method.get("line_number", 0),
                    }
                )

            # Run the test and get static calls and success status
            traced_calls, success = self.run_test_with_tracing(test_case)

            return {
                "test_name": test_case["name"],
                "test_file": test_case["file_path"],
                "static_methods": static_methods,
                "dynamic_methods": traced_calls,
                "assertions": test_case.get("assertions", []),
                "mocks": test_case.get("mocks", []),
                "success": success,
                "test_source_code": test_case.get("source_code", ""),
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


def calculate_advanced_metrics(test_collection, analyses) -> Dict:
    """Calculate advanced metrics from test analyses"""
    metrics = {
        # Basic metrics (from before)
        "total_tests": len(test_collection.tests),
        "successful_tests": 0,
        "failed_tests": 0,
        "total_assertions": 0,
        "total_mocks": 0,
        "total_static_methods": 0,
        "total_dynamic_methods": 0,
        "tests_with_docstrings": 0,
        "tests_with_fixtures": 0,
        "average_test_length": 0,
        # New advanced metrics
        "test_complexity": {
            "simple": 0,  # 0-2 assertions
            "moderate": 0,  # 3-5 assertions
            "complex": 0,  # 6+ assertions
        },
        "most_tested_methods": Counter(),
        "most_used_fixtures": Counter(),
        "most_common_mocks": Counter(),
        "test_lengths": [],
        "assertion_density": 0.0,  # assertions per line
        "mock_density": 0.0,  # mocks per test
        "coverage_metrics": {"methods_with_multiple_tests": 0, "untested_methods": 0, "average_tests_per_method": 0.0},
        "test_isolation": {
            "fully_isolated": 0,  # tests with mocks for all external deps
            "partially_isolated": 0,  # tests with some mocks
            "no_isolation": 0,  # tests with no mocks
        },
    }

    total_lines = 0
    all_methods: Set[str] = set()
    tested_methods: List[str] = []

    for test_case in test_collection.tests:
        analysis = next((a for a in analyses if a["test_name"] == test_case.name), None)
        if not analysis:
            continue

        # Update basic metrics
        metrics["successful_tests"] += 1 if analysis["success"] else 0
        metrics["failed_tests"] += 0 if analysis["success"] else 1
        num_assertions = len(analysis["assertions"])
        metrics["total_assertions"] += num_assertions
        num_mocks = len(analysis["mocks"])
        metrics["total_mocks"] += num_mocks
        metrics["total_static_methods"] += len(analysis["static_methods"])
        metrics["total_dynamic_methods"] += len(analysis["dynamic_methods"])
        metrics["tests_with_docstrings"] += 1 if test_case.docstring else 0
        metrics["tests_with_fixtures"] += 1 if test_case.fixtures else 0

        # Test complexity
        if num_assertions <= 2:
            metrics["test_complexity"]["simple"] += 1
        elif num_assertions <= 5:
            metrics["test_complexity"]["moderate"] += 1
        else:
            metrics["test_complexity"]["complex"] += 1

        # Track methods under test
        for method in analysis["static_methods"]:
            metrics["most_tested_methods"][method["name"]] += 1
            all_methods.add(method["name"])
            tested_methods.append(method["name"])

        # Track fixtures and mocks
        for fixture in test_case.fixtures:
            metrics["most_used_fixtures"][fixture] += 1
        for mock in analysis["mocks"]:
            metrics["most_common_mocks"][mock] += 1

        # Test length and density metrics
        test_length = test_case.end_line_number - test_case.line_number + 1
        metrics["test_lengths"].append(test_length)
        total_lines += test_length

        # Test isolation
        if num_mocks == 0:
            metrics["test_isolation"]["no_isolation"] += 1
        elif num_mocks >= len(analysis["dynamic_methods"]):
            metrics["test_isolation"]["fully_isolated"] += 1
        else:
            metrics["test_isolation"]["partially_isolated"] += 1

    # Calculate aggregate metrics
    total_tests = metrics["total_tests"]
    if total_tests > 0:
        metrics["average_test_length"] = total_lines / total_tests
        metrics["assertion_density"] = metrics["total_assertions"] / total_lines
        metrics["mock_density"] = metrics["total_mocks"] / total_tests

        # Test length statistics
        metrics["test_length_stats"] = {
            "min": min(metrics["test_lengths"]),
            "max": max(metrics["test_lengths"]),
            "median": statistics.median(metrics["test_lengths"]),
            "std_dev": statistics.stdev(metrics["test_lengths"]) if len(metrics["test_lengths"]) > 1 else 0,
        }

        # Coverage metrics
        method_test_counts = Counter(tested_methods)
        metrics["coverage_metrics"].update(
            {
                "methods_with_multiple_tests": sum(1 for count in method_test_counts.values() if count > 1),
                "untested_methods": len(all_methods) - len(method_test_counts),
                "average_tests_per_method": len(tested_methods) / len(all_methods) if all_methods else 0,
            }
        )

        # Keep only top 5 for each counter
        metrics["most_tested_methods"] = dict(metrics["most_tested_methods"].most_common(5))
        metrics["most_used_fixtures"] = dict(metrics["most_used_fixtures"].most_common(5))
        metrics["most_common_mocks"] = dict(metrics["most_common_mocks"].most_common(5))

    return metrics


def print_metrics(metrics: Dict):
    """Print formatted metrics"""
    click.echo("\n" + "=" * 80)
    click.echo("TEST ANALYSIS METRICS")
    click.echo("=" * 80)

    click.echo("\n📊 Basic Metrics:")
    click.echo(f"Total Tests: {metrics['total_tests']}")
    click.echo(f"✅ Successful Tests: {metrics['successful_tests']}")
    click.echo(f"❌ Failed Tests: {metrics['failed_tests']}")
    click.echo(f"Assertions: {metrics['total_assertions']}")
    click.echo(f"Mocks: {metrics['total_mocks']}")

    click.echo("\n📏 Test Size and Complexity:")
    click.echo(f"Average Length: {metrics['average_test_length']:.2f} lines")
    click.echo(f"Length Statistics:")
    click.echo(f"  • Min: {metrics['test_length_stats']['min']} lines")
    click.echo(f"  • Max: {metrics['test_length_stats']['max']} lines")
    click.echo(f"  • Median: {metrics['test_length_stats']['median']} lines")
    click.echo(f"  • Std Dev: {metrics['test_length_stats']['std_dev']:.2f} lines")
    click.echo("\nComplexity Distribution:")
    click.echo(f"  • Simple Tests (0-2 assertions): {metrics['test_complexity']['simple']}")
    click.echo(f"  • Moderate Tests (3-5 assertions): {metrics['test_complexity']['moderate']}")
    click.echo(f"  • Complex Tests (6+ assertions): {metrics['test_complexity']['complex']}")

    click.echo("\n🎯 Coverage and Density:")
    click.echo(f"Assertion Density: {metrics['assertion_density']:.2f} assertions per line")
    click.echo(f"Mock Density: {metrics['mock_density']:.2f} mocks per test")
    click.echo(f"Methods with Multiple Tests: {metrics['coverage_metrics']['methods_with_multiple_tests']}")
    click.echo(f"Untested Methods: {metrics['coverage_metrics']['untested_methods']}")
    click.echo(f"Average Tests per Method: {metrics['coverage_metrics']['average_tests_per_method']:.2f}")

    click.echo("\n🔍 Test Isolation:")
    click.echo(f"Fully Isolated: {metrics['test_isolation']['fully_isolated']}")
    click.echo(f"Partially Isolated: {metrics['test_isolation']['partially_isolated']}")
    click.echo(f"No Isolation: {metrics['test_isolation']['no_isolation']}")


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
