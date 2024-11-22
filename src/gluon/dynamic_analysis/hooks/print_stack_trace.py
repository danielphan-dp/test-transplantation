import inspect
import os
import sys
from functools import wraps
from typing import Callable, TypeVar, Any

T = TypeVar('T')

def print_stack_trace(func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that prints a clean, meaningful stack trace of function calls,
    including internal function calls within the decorated function.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            # Get project root directory
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
            
            # Set up trace function
            def traceit(frame, event, arg):
                if event == 'call':
                    filepath = os.path.abspath(frame.f_code.co_filename)
                    
                    # Skip if not in project files
                    if (not filepath.startswith(project_root) or
                        'site-packages' in filepath or
                        frame.f_code.co_name in ('wrapper', '<module>')):
                        return traceit
                    
                    # Format function arguments
                    args_str = []
                    for name, value in frame.f_locals.items():
                        if name.startswith('__'):
                            continue
                        try:
                            val_str = repr(value)
                            if len(val_str) > 50:
                                val_str = val_str[:47] + "..."
                            args_str.append(f"{name}={val_str}")
                        except Exception:
                            args_str.append(f"{name}=<unprintable>")
                    
                    # Print frame info
                    rel_path = os.path.relpath(filepath, project_root)
                    print(f"{rel_path}:{frame.f_lineno} - {frame.f_code.co_name}")
                    if args_str:
                        print(f"    Args: {', '.join(args_str)}")
                
                return traceit

            print(f"\nStack Trace for: {func.__name__}")
            print("-" * 80)
            
            # Enable tracing
            sys.settrace(traceit)
            result = func(*args, **kwargs)
            sys.settrace(None)
            
            print("-" * 80)
            return result
            
        except Exception as e:
            print(f"Stack trace error: {e}")
            sys.settrace(None)
            return func(*args, **kwargs)
    
    return wrapper
