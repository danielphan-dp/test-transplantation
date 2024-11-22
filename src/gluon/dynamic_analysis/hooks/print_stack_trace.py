import inspect
import os
import sys
from functools import wraps
from typing import Callable, TypeVar, Any

T = TypeVar("T")


def print_stack_trace(func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that prints a clean, meaningful stack trace of function calls,
    including internal function calls within the decorated function.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            # Get project root directory (Flask repo directory in this case)
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            )

            print(f"\nStack Trace for: {func.__name__}")
            print(f"Project root: {os.path.basename(project_root)}")
            print("-" * 80)

            # Set up trace function
            def traceit(frame, event, arg):
                if event == "call":
                    filepath = os.path.abspath(frame.f_code.co_filename)

                    # Only skip system files and our wrapper
                    # if frame.f_code.co_name == "wrapper" or "site-packages" in filepath or "lib/python" in filepath:
                    #     return traceit

                    # Format function arguments
                    args_str = []
                    for name, value in frame.f_locals.items():
                        if name == "self":  # Skip self for class methods
                            continue
                        try:
                            val_str = repr(value)
                            if len(val_str) > 50:
                                val_str = val_str[:47] + "..."
                            args_str.append(f"{name}={val_str}")
                        except Exception:
                            args_str.append(f"{name}=<unprintable>")

                    # Print frame info
                    try:
                        rel_path = os.path.relpath(filepath, project_root)
                    except ValueError:
                        rel_path = filepath

                    print(f"-> {rel_path}:{frame.f_lineno} - {frame.f_code.co_name}")
                    if args_str:
                        print(f"   Args: {', '.join(args_str)}")

                return traceit

            # Enable tracing
            sys.settrace(traceit)
            result = func(*args, **kwargs)
            sys.settrace(None)

            print("-" * 80)
            print(f"End trace for: {func.__name__}\n")
            return result

        except Exception as e:
            print(f"Stack trace error: {e}")
            import traceback

            traceback.print_exc()
            sys.settrace(None)
            return func(*args, **kwargs)

    return wrapper
