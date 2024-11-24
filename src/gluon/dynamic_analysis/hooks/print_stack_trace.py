import inspect
import os
import sys
import traceback
import ast
import json
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar, Any, Optional, Dict, List, Tuple
from pathlib import Path

T = TypeVar("T")


class OutputManager:
    """Manages file output operations for stack traces and test information."""

    def __init__(self, base_func_name: str):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_path = self._create_output_directory(base_func_name)
        self.stack_trace_file = self.base_path / "stack_trace.txt"
        self.test_info_file = self.base_path / "test_info.txt"
        self.summary_file = self.base_path / "summary.json"

    def _create_output_directory(self, base_func_name: str) -> Path:
        output_dir = Path("trace_outputs") / f"{base_func_name}_{self.timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def write_line(self, content: str, file_type: str = "stack_trace") -> None:
        file_path = getattr(self, f"{file_type}_file")
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content + "\n")

    def write_summary(self, summary_data: Dict[str, Any]) -> None:
        with open(self.summary_file, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2, default=str)


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


class TestInformationCollector:
    """Handles collection and formatting of test-related information."""

    def __init__(self, func: Callable, args: Tuple):
        self.func = func
        self.args = args
        self.test_class = args[0].__class__ if args and hasattr(args[0], "__class__") else None
        self.module = inspect.getmodule(self.test_class) if self.test_class else None

    def collect_test_info(self, show_dependencies: bool = True) -> str:
        if not self.func.__name__.startswith("test"):
            return ""

        output = ["\nTest Information:", "=" * 80]

        if self.test_class:
            output.extend(
                [
                    f"Module: {self.module.__name__}",
                    f"Test Class: {self.test_class.__name__}",
                ]
            )

            method_info = self._get_test_method_info(show_dependencies)
            output.extend(method_info)

        return "\n".join(output)

    def _get_test_method_info(self, show_dependencies: bool) -> List[str]:
        test_method = getattr(self.test_class, self.func.__name__)
        method_info = MethodAnalyzer.get_method_info(test_method)

        info = [
            "\nTest Method Details:",
            f"Name: {method_info['name']}",
            f"Signature: {method_info['signature']}",
            f"Documentation:\n{method_info['doc']}",
            f"\nMethod Under Test: {self.func.__name__}",
            f"Defined in: {self.func.__module__}.{self.func.__qualname__}",
        ]

        if show_dependencies:
            info.extend(["\nMethod Dependencies:", *[f"  - {dep}" for dep in method_info["dependencies"]]])

        info.extend(["\nComplete Method Source:", "-" * 80, method_info["source"], "-" * 80])

        return info


class StackTraceFormatter:
    """Handles formatting and printing of stack trace information."""

    def __init__(self, project_root: str, output_manager: OutputManager):
        self.project_root = project_root
        self.output_manager = output_manager

    def format_frame_info(self, frame: Any, stack_level: StackLevel, caller_info: str = "") -> None:
        filepath = os.path.abspath(frame.f_code.co_filename)
        try:
            rel_path = os.path.relpath(filepath, self.project_root)
        except ValueError:
            rel_path = filepath

        indent = stack_level.indent()
        self.output_manager.write_line(f"{indent} {rel_path}:{frame.f_lineno} - {frame.f_code.co_name}{caller_info}")

        # Format arguments
        args_str = self._format_arguments(frame)
        if args_str:
            self.output_manager.write_line(f"{indent.replace('├─', '│ ')}   Args: {', '.join(args_str)}")

    def _format_arguments(self, frame: Any) -> List[str]:
        return [f"{name}={format_value(value)}" for name, value in frame.f_locals.items() if name != "self"]


class StackTraceHandler:
    """Manages the stack trace processing and output."""

    def __init__(self, func: Callable, max_depth: int, include_timing: bool, output_manager: OutputManager):
        self.func = func
        self.max_depth = max_depth
        self.include_timing = include_timing
        self.stack_level = StackLevel()
        self.project_root = self._get_project_root()
        self.output_manager = output_manager
        self.formatter = StackTraceFormatter(self.project_root, output_manager)

    def _get_project_root(self) -> str:
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        )

    def _get_caller_info(self) -> str:
        try:
            caller_frame = sys._getframe(3)  # Adjusted for wrapper depth
            caller_file = os.path.relpath(caller_frame.f_code.co_filename, self.project_root)
            return f" (called from {caller_file}:{caller_frame.f_lineno})"
        except (ValueError, AttributeError):
            return ""

    def should_trace_file(self, filepath: str) -> bool:
        return "site-packages" not in filepath and "lib/python" not in filepath

    def create_trace_function(self) -> Callable:
        def traceit(frame: Any, event: str, arg: Any) -> Callable:
            if self.stack_level.level > self.max_depth:
                return traceit

            filepath = os.path.abspath(frame.f_code.co_filename)
            if not self.should_trace_file(filepath):
                return traceit

            if event == "call":
                caller_info = self._get_caller_info()
                self.stack_level.increase()
                self.formatter.format_frame_info(frame, self.stack_level, caller_info)

            elif event == "return" and self.include_timing:
                duration = self.stack_level.decrease()
                if duration is not None:
                    indent = "│  " * self.stack_level.level + "└─"
                    self.output_manager.write_line(f"{indent} Completed {frame.f_code.co_name} in {duration:.4f}s")

            return traceit

        return traceit


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
    Enhanced decorator that outputs a detailed, tree-structured stack trace of function calls to files.

    Args:
        func: The function to decorate
        display_test_info: Whether to display additional test information
        max_depth: Maximum stack depth to prevent infinite recursion
        include_timing: Whether to include timing information for each call
        show_dependencies: Whether to show method dependencies
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        output_manager = OutputManager(func.__name__)
        handler = StackTraceHandler(func, max_depth, include_timing, output_manager)
        start_time = datetime.now()

        try:
            # Write header information
            output_manager.write_line("=" * 80)
            output_manager.write_line(f"Stack Trace for: {func.__name__}")
            output_manager.write_line(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            output_manager.write_line(f"Project root: {os.path.basename(handler.project_root)}")

            if display_test_info:
                collector = TestInformationCollector(func, args, output_manager)
                collector.collect_test_info(show_dependencies)

            sys.settrace(handler.create_trace_function())
            result = func(*args, **kwargs)
            sys.settrace(None)

            duration = (datetime.now() - start_time).total_seconds()

            # Write summary information
            output_manager.write_line("\nExecution Summary:")
            output_manager.write_line(f"Total time: {duration:.4f}s")
            output_manager.write_line("=" * 80 + "\n")

            # Write JSON summary
            summary_data = {
                "function_name": func.__name__,
                "start_time": start_time,
                "duration": duration,
                "project_root": handler.project_root,
                "max_depth": max_depth,
                "include_timing": include_timing,
            }
            output_manager.write_summary(summary_data)

            return result

        except Exception as e:
            output_manager.write_line(f"Stack trace error: {str(e)}")
            traceback.print_exc(file=open(output_manager.stack_trace_file, "a"))
            sys.settrace(None)
            return func(*args, **kwargs)

    return wrapper
