import inspect
from functools import wraps
from typing import Callable, TypeVar, Any
import unittest
import os
import importlib.util
from pathlib import Path
from gluon.dynamic_analysis.hooks.print_stack_trace import print_stack_trace
import pytest

T = TypeVar("T")


def is_test_function(obj: Any) -> bool:
    """Check if an object is a test function."""
    return callable(obj) and hasattr(obj, "__name__") and obj.__name__.startswith("test_")


def is_test_class(obj: Any) -> bool:
    """Check if an object is a test class."""
    return isinstance(obj, type) and issubclass(obj, unittest.TestCase)


def load_module_from_file(file_path: str) -> Any:
    """Dynamically load a Python module from file path."""
    spec = importlib.util.spec_from_file_location("module", file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None


def find_test_files(start_path: str) -> list[str]:
    """Recursively find all test files in the given directory."""
    test_files = []
    for root, _, files in os.walk(start_path):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(root, file))
    return test_files


def attach_hooks_to_tests(flask_repo_path: str) -> None:
    """Attach hooks to all test functions in the Flask repository."""
    test_dir = os.path.join(flask_repo_path, "tests")

    def get_test_context(obj):
        """Extract test context from docstring or source"""
        doc = inspect.getdoc(obj)
        source = inspect.getsource(obj)
        # Parse docstring and source to identify Flask methods being tested
        # Return context information

    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    # Load the module
                    spec = importlib.util.spec_from_file_location(file[:-3], file_path)
                    if spec is None or spec.loader is None:
                        continue
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Find all test functions and attach hooks
                    for name, obj in inspect.getmembers(module):
                        if name.startswith("test_") and inspect.isfunction(obj):
                            context = get_test_context(obj)
                            # Attach context to the trace
                            setattr(module, name, print_stack_trace(obj, flask_repo_path, context))
                            print(f"Attached hook to {name}")
                        elif inspect.isclass(obj):
                            # Handle test methods in test classes
                            for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                                if method_name.startswith("test_"):
                                    # Attach decorator to the method
                                    setattr(obj, method_name, print_stack_trace(method, flask_repo_path))
                                    print(f"Attached hook to {obj.__name__}.{method_name}")

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")


def attach_stack_trace_hook(target_func: Callable[..., T]) -> Callable[..., T]:
    """
    Attaches a stack trace hook to the specified function.
    """

    @print_stack_trace
    @wraps(target_func)
    def wrapped_func(*args: Any, **kwargs: Any) -> T:
        return target_func(*args, **kwargs)

    return wrapped_func


def run_flask_tests(flask_repo_path: str) -> None:
    """Run all Flask tests after attaching hooks."""
    # Convert relative path to absolute path
    abs_path = os.path.abspath(flask_repo_path)

    # First attach hooks to all test functions
    attach_hooks_to_tests(abs_path)

    # Change to the Flask repo directory
    original_dir = os.getcwd()
    os.chdir(abs_path)

    try:
        # Run pytest programmatically
        pytest.main(["-v", "-s"])

    finally:
        # Change back to original directory
        os.chdir(original_dir)


if __name__ == "__main__":
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # The Flask repo is in the 'data/flask' subdirectory of the current directory
    FLASK_REPO_PATH = os.path.join(current_dir, "_data", "flask")
    print(f"Using Flask repo path: {FLASK_REPO_PATH}")
    run_flask_tests(FLASK_REPO_PATH)
