import inspect
import os
import sys
from functools import wraps
from typing import Callable, TypeVar, Any, Optional, Union
import traceback

T = TypeVar("T")


def resolve_flask_method(frame):
    """Identify if the current frame is executing a Flask method"""
    module = inspect.getmodule(frame.f_code)
    if module and "flask" in module.__name__:
        return True, module.__name__, frame.f_code.co_name
    return False, None, None


def print_stack_trace(
    func: Callable[..., T], project_root: Optional[str] = None, context: Optional[dict] = None
) -> Callable[..., T]:
    """
    A decorator that prints a clean, meaningful stack trace of function calls,
    including internal function calls within the decorated function.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            root_dir = project_root or os.getcwd()

            # Print test context first
            print(f"\nStack Trace for: {func.__name__}")
            if context:
                if "description" in context:
                    print(f"Test Description: {context['description']}")
                if "test_class" in context:
                    print(f"Test Class: {context['test_class']}")
                if "flask_calls" in context:
                    print("Expected Flask calls:")
                    for call in context["flask_calls"]:
                        print(f"  - {call}")
            print(f"Project root: {os.path.basename(root_dir)}")
            print("-" * 80)

            # Track actual Flask methods called
            flask_methods_called = set()

            def traceit(frame, event, arg):
                if event == "call":
                    is_flask, module_name, method_name = resolve_flask_method(frame)
                    if is_flask:
                        flask_methods_called.add(f"{module_name}.{method_name}")
                        print(f"Flask method: {module_name}.{method_name}")

                        # Print source location
                        filepath = os.path.abspath(frame.f_code.co_filename)
                        try:
                            rel_path = os.path.relpath(filepath, project_root)
                        except ValueError:
                            rel_path = filepath
                        print(f"-> {rel_path}:{frame.f_lineno} - {method_name}")

                        # Print method arguments
                        args_str = format_arguments(frame)
                        if args_str:
                            print(f"   Args: {args_str}")

                    # For non-Flask calls, only trace if in project root
                    elif project_root and frame.f_code.co_filename.startswith(project_root):
                        filepath = os.path.abspath(frame.f_code.co_filename)
                        if filepath.startswith(project_root):
                            print(
                                f"-> {os.path.relpath(filepath, project_root)}:"
                                f"{frame.f_lineno} - {frame.f_code.co_name}"
                            )

                return traceit

            # Enable tracing
            sys.settrace(traceit)
            result = func(*args, **kwargs)
            sys.settrace(None)

            # Print summary
            print("-" * 80)
            print(f"End trace for: {func.__name__}")
            print(f"Flask methods called: {', '.join(sorted(flask_methods_called))}\n")

            return result

        except Exception as e:
            print(f"Stack trace error: {e}")
            traceback.print_exc()
            sys.settrace(None)
            return func(*args, **kwargs)

    return wrapper


def format_arguments(frame):
    """Format function arguments for printing"""
    args_str = []
    for name, value in frame.f_locals.items():
        if name == "self":  # Skip self for class methods
            continue
        try:
            val_str = repr(value)
            args_str.append(f"{name}={val_str}")
        except Exception:
            args_str.append(f"{name}=<unprintable>")
    return ", ".join(args_str)
