import inspect
import os
import sys
import types
import traceback
import ast
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar, Any, Optional, Dict, List, Tuple

T = TypeVar("T")


class StackLevel:
    """Manages stack level tracking and timing for function calls."""

    def __init__(self):
        self.level = 0
        self.call_times: Dict[int, datetime] = {}  # Track entry time for each level

    def increase(self) -> None:
        self.level += 1
        self.call_times[self.level] = datetime.now()

    def decrease(self) -> Optional[float]:
        if self.level in self.call_times:
            duration = (datetime.now() - self.call_times[self.level]).total_seconds()
            del self.call_times[self.level]
            self.level = max(0, self.level - 1)
            return duration
        self.level = max(0, self.level - 1)
        return None

    def indent(self, is_last: bool = False) -> str:
        if is_last:
            return "│  " * (self.level - 1) + "└─"
        return "│  " * self.level + "├─"


class MethodAnalyzer:
    """Analyzes and extracts method information including dependencies and full source."""

    @staticmethod
    def get_complete_source(obj: Any) -> str:
        """Get the complete source code of an object including decorators."""
        try:
            source_lines, start_line = inspect.getsourcelines(obj)
            return "".join(source_lines)
        except Exception:
            return "Source code not available"

    @staticmethod
    def get_method_dependencies(method: Callable) -> List[str]:
        """Extract method dependencies by analyzing the source code."""
        dependencies = []
        try:
            source = inspect.getsource(method)
            tree = ast.parse(source)

            class DependencyVisitor(ast.NodeVisitor):
                def visit_Name(self, node: ast.Name) -> None:
                    if isinstance(node.ctx, ast.Load):
                        dependencies.append(node.id)

                def visit_Attribute(self, node: ast.Attribute) -> None:
                    if isinstance(node.ctx, ast.Load):
                        dependencies.append(node.attr)

            DependencyVisitor().visit(tree)
            return list(set(dependencies))
        except Exception:
            return []

    @staticmethod
    def get_method_info(method: Callable) -> Dict[str, Any]:
        """Get comprehensive information about a method."""
        try:
            return {
                "name": method.__name__,
                "signature": str(inspect.signature(method)),
                "source": MethodAnalyzer.get_complete_source(method),
                "dependencies": MethodAnalyzer.get_method_dependencies(method),
                "module": method.__module__,
                "qualname": method.__qualname__,
                "doc": inspect.getdoc(method) or "No documentation available",
            }
        except Exception as e:
            return {"error": str(e)}


def format_value(value: Any, max_length: int = 50) -> str:
    """Safely format a value with length limitation."""
    try:
        val_str = repr(value)
        if len(val_str) > max_length:
            return f"{val_str[:max_length-3]}..."
        return val_str
    except Exception:
        return "<unprintable>"


def print_stack_trace(
    func: Callable[..., T],
    display_test_info: bool = True,
    max_depth: int = 50,
    include_timing: bool = True,
    show_dependencies: bool = True,
) -> Callable[..., T]:
    """
    Enhanced decorator that prints a detailed, tree-structured stack trace of function calls.

    Args:
        func: The function to decorate
        display_test_info: Whether to display additional test information
        max_depth: Maximum stack depth to prevent infinite recursion
        include_timing: Whether to include timing information for each call
        show_dependencies: Whether to show method dependencies
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        stack_level = StackLevel()
        start_time = datetime.now()

        try:
            # Get project root path
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            )

            print("\n" + "=" * 80)
            print(f"Stack Trace for: {func.__name__}")
            print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Project root: {os.path.basename(project_root)}")

            # Display test information if applicable
            if display_test_info and func.__name__.startswith("test"):
                print("\nTest Information:")
                print("=" * 80)

                if args and hasattr(args[0], "__class__"):
                    test_class = args[0].__class__

                    # Get module information
                    module = inspect.getmodule(test_class)
                    print(f"Module: {module.__name__}")

                    # Get test class information
                    print(f"Test Class: {test_class.__name__}")
                    if test_class.__doc__:
                        print(f"Class Description: {test_class.__doc__.strip()}")

                    # Get the test method details
                    test_method = getattr(test_class, func.__name__)
                    method_info = MethodAnalyzer.get_method_info(test_method)

                    print("\nTest Method Details:")
                    print(f"Name: {method_info['name']}")
                    print(f"Signature: {method_info['signature']}")
                    print(f"Documentation:\n{method_info['doc']}")

                    print(f"\nMethod Under Test: {func.__name__}")
                    print(f"Defined in: {func.__module__}.{func.__qualname__}")
                    if show_dependencies:
                        print("\nMethod Dependencies:")
                        for dep in method_info["dependencies"]:
                            print(f"  - {dep}")

                    if show_dependencies:
                        print("\nMethod Dependencies:")
                        for dep in method_info["dependencies"]:
                            print(f"  - {dep}")

                    print("\nComplete Method Source:")
                    print("-" * 80)
                    print(method_info["source"])
                    print("-" * 80)

                    # Get all test methods in the class
                    test_methods = [
                        name
                        for name, value in inspect.getmembers(
                            test_class,
                            predicate=lambda x: isinstance(x, types.FunctionType) and x.__name__.startswith("test_"),
                        )
                    ]
                    print(f"\nAll test methods in class: {', '.join(test_methods)}")

            def traceit(frame: Any, event: str, arg: Any) -> Callable:
                if stack_level.level > max_depth:
                    return traceit

                filepath = os.path.abspath(frame.f_code.co_filename)

                # Skip system files
                if "site-packages" in filepath or "lib/python" in filepath:
                    return traceit

                if event == "call":
                    # Get caller information using sys._getframe
                    caller_info = ""
                    try:
                        caller_frame = sys._getframe(2)
                        caller_file = os.path.relpath(caller_frame.f_code.co_filename, project_root)
                        caller_info = f" (called from {caller_file}:{caller_frame.f_lineno})"
                    except (ValueError, AttributeError):
                        pass

                    stack_level.increase()

                    # Format function arguments
                    args_str = []
                    for name, value in frame.f_locals.items():
                        if name == "self":
                            continue
                        args_str.append(f"{name}={format_value(value)}")

                    # Print frame info with tree structure
                    try:
                        rel_path = os.path.relpath(filepath, project_root)
                    except ValueError:
                        rel_path = filepath

                    indent = stack_level.indent()
                    print(f"{indent} {rel_path}:{frame.f_lineno} - {frame.f_code.co_name}{caller_info}")

                    if args_str:
                        print(f"{indent.replace('├─', '│ ')}   Args: {', '.join(args_str)}")

                elif event == "return":
                    duration = stack_level.decrease()
                    if include_timing and duration is not None:
                        indent = "│  " * stack_level.level + "└─"
                        print(f"{indent} Completed {frame.f_code.co_name} in {duration:.4f}s")

                return traceit

            # Enable tracing
            sys.settrace(traceit)
            result = func(*args, **kwargs)
            sys.settrace(None)

            # Print summary
            duration = (datetime.now() - start_time).total_seconds()
            print("\nExecution Summary:")
            print(f"Total time: {duration:.4f}s")
            print("=" * 80 + "\n")

            return result

        except Exception as e:
            print(f"Stack trace error: {str(e)}")
            traceback.print_exc()
            sys.settrace(None)
            return func(*args, **kwargs)

    return wrapper
