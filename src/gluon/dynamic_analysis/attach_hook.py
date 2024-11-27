import inspect
from functools import wraps
from typing import Callable, TypeVar, Any
from gluon.dynamic_analysis._tests._test1 import process_numbers
from gluon.dynamic_analysis._tests._test2 import process_number
from gluon.dynamic_analysis._tests._test3 import process_order
from gluon.dynamic_analysis.hooks.print_stack_trace import print_stack_trace

T = TypeVar("T")


def attach_stack_trace_hook(target_func: Callable[..., T] = process_order) -> Callable[..., T]:
    """
    Attaches a stack trace hook to the specified function.
    If no function is provided, defaults to process_order.

    Args:
        target_func: The function to attach the hook to
    Returns:
        The wrapped function with stack trace functionality
    """
    # Store the original function
    original_func = target_func

    # Create wrapped function with print_stack_trace decorator
    @print_stack_trace
    @wraps(original_func)
    def wrapped_func(*args: Any, **kwargs: Any) -> T:
        return original_func(*args, **kwargs)

    # Get the module where the target function is defined
    module = inspect.getmodule(target_func)

    # Replace the original function with the wrapped version
    if module:
        setattr(module, target_func.__name__, wrapped_func)
        print(f"Hook attached successfully to {target_func.__name__}")

    return wrapped_func


if __name__ == "__main__":
    # Get the wrapped function
    hooked_func = attach_stack_trace_hook()

    # Test 1
    print("\nTesting hooked function:")
    hooked_func = attach_stack_trace_hook(process_numbers)
    result = hooked_func(10, 20)
    print(f"Result: {result:.2f}")

    # Test 2
    print("\nTesting hooked function:")
    hooked_func = attach_stack_trace_hook(process_number)
    result = hooked_func(5)
    print(f"Result: {result:.2f}")

    # Test 3
    print("\nTesting hooked function:")
    hooked_func = attach_stack_trace_hook(process_order)
    test_user_id = 1500
    test_cart_items = [100, 200, 300, 400]
    result = hooked_func(test_user_id, test_cart_items)
    print(f"Result: ${result:.2f}")
