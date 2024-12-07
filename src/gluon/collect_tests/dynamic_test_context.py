from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import time
import sys
import threading
from pathlib import Path
import resource


@dataclass
class DynamicTestContext:
    """Captures runtime behavior of tests"""

    # Test execution data
    execution_success: bool = False
    execution_time: float = 0.0
    memory_usage: float = 0.0  # Optional, will be 0.0 on non-Unix systems

    # Method call tracing
    method_calls: List[Dict[str, Any]] = field(default_factory=list)
    call_stack: List[str] = field(default_factory=list)

    # Runtime metrics
    actual_coverage: Dict[str, int] = field(default_factory=dict)  # Methods actually called during execution
    external_calls: List[str] = field(default_factory=list)  # Calls to external dependencies
    runtime_errors: List[Dict[str, Any]] = field(default_factory=list)  # Any errors that occurred during execution

    @classmethod
    def from_test_execution(cls, test_case: Dict, tracer: "MethodCallTracer") -> "DynamicTestContext":
        """Create context from test execution results"""
        start_time = time.time()
        try:
            start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        except (AttributeError, ImportError):
            start_memory = 0

        success = False
        runtime_errors = []

        try:
            with tracer.trace_context(test_case["name"]):
                # Execute the test
                success = True  # Will be set to False if any exceptions occur
        except Exception as e:
            success = False
            runtime_errors.append({"type": type(e).__name__, "message": str(e), "traceback": e.__traceback__})

        end_time = time.time()
        try:
            end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            memory_used = (end_memory - start_memory) / 1024  # Convert to MB
        except (AttributeError, ImportError):
            memory_used = 0

        # Process method calls
        method_calls = tracer.calls
        call_stack = [call["function"] for call in method_calls]

        # Calculate actual coverage
        actual_coverage = {}
        for call in method_calls:
            func_name = call["function"]
            actual_coverage[func_name] = actual_coverage.get(func_name, 0) + 1

        # Identify external calls
        external_calls = cls._identify_external_calls(method_calls)

        return cls(
            execution_success=success,
            execution_time=end_time - start_time,
            memory_usage=memory_used,
            method_calls=method_calls,
            call_stack=call_stack,
            actual_coverage=actual_coverage,
            external_calls=external_calls,
            runtime_errors=runtime_errors,
        )

    @staticmethod
    def _identify_external_calls(method_calls: List[Dict[str, Any]]) -> List[str]:
        """Identify calls to external dependencies"""
        external_calls = []
        standard_lib_prefixes = {"os.", "sys.", "time.", "datetime.", "json.", "csv."}

        for call in method_calls:
            func_name = call["function"]
            # Check if it's an external call (not in the project directory)
            if any(func_name.startswith(prefix) for prefix in standard_lib_prefixes):
                external_calls.append(func_name)
            elif "site-packages" in call.get("filename", ""):
                external_calls.append(func_name)

        return external_calls

    def get_call_graph(self) -> Dict[str, List[str]]:
        """Generate a call graph from the recorded method calls"""
        call_graph = {}

        for i, call in enumerate(self.method_calls):
            caller = call.get("caller")
            callee = call["function"]

            if caller:
                if caller not in call_graph:
                    call_graph[caller] = []
                if callee not in call_graph[caller]:
                    call_graph[caller].append(callee)

        return call_graph

    def get_coverage_summary(self) -> Dict[str, Any]:
        """Generate a summary of test coverage"""
        return {
            "total_methods_called": len(self.actual_coverage),
            "call_frequencies": self.actual_coverage,
            "external_dependencies": len(self.external_calls),
            "max_stack_depth": len(self.call_stack),
        }

    def get_performance_metrics(self) -> Dict[str, float]:
        """Get performance-related metrics"""
        return {
            "execution_time": self.execution_time,
            "memory_usage": self.memory_usage,
            "calls_per_second": len(self.method_calls) / self.execution_time if self.execution_time > 0 else 0,
        }

    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of runtime errors"""
        error_types = {}
        for error in self.runtime_errors:
            error_type = error["type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1

        return {
            "total_errors": len(self.runtime_errors),
            "error_types": error_types,
            "has_failures": not self.execution_success,
        }


class MethodCallTracer:
    """Traces method calls during test execution"""

    def __init__(self, package_path: str):
        self.package_path = Path(package_path).resolve()
        self.calls = []
        self.ignore_paths = {"site-packages", "dist-packages", "lib/python"}
        self.current_thread = threading.current_thread()

    def should_trace(self, filename: str) -> bool:
        """Check if this file should be traced"""
        if not filename:
            return False

        filename = Path(filename).resolve()
        return str(filename).startswith(str(self.package_path)) and not any(
            p in str(filename) for p in self.ignore_paths
        )

    def trace_calls(self, frame, event, arg):
        """Trace function calls"""
        if threading.current_thread() != self.current_thread:
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

        # Get the caller information
        caller_frame = frame.f_back
        caller_name = None
        if caller_frame:
            caller_code = caller_frame.f_code
            caller_name = caller_code.co_name
            if "self" in caller_frame.f_locals:
                caller_cls = caller_frame.f_locals["self"].__class__
                caller_name = f"{caller_cls.__name__}.{caller_name}"

        self.calls.append(
            {
                "function": func_name,
                "filename": filename,
                "line": frame.f_lineno,
                "caller": caller_name,
                "locals": {k: str(v) for k, v in frame.f_locals.items() if isinstance(v, (str, int, float, bool))},
            }
        )

        return self.trace_calls

    def get_call_stack(self) -> List[str]:
        """Get the current call stack"""
        return [call["function"] for call in self.calls]

    def clear(self):
        """Clear the recorded calls"""
        self.calls = []

    def __enter__(self):
        """Start tracing"""
        self.clear()
        sys.settrace(self.trace_calls)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop tracing"""
        sys.settrace(None)
