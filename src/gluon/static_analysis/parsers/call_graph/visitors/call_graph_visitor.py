import ast
from typing import Optional, Dict, Union

from ..models.call_node import CallNode


class CallGraphVisitor(ast.NodeVisitor):
    """AST visitor for building the call graph"""

    def __init__(self, builder: "CallGraphBuilder"):
        self.builder = builder
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None
        self.imports: Dict[str, str] = {}

    def visit_ClassDef(self, node: ast.ClassDef):
        """Process class definitions"""
        previous_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = previous_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Process function definitions"""
        self._process_function_def(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Process async function definitions"""
        self._process_function_def(node, is_async=True)

    def _process_function_def(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], is_async: bool = False):
        """Process function/method definition"""
        func_id = self._get_function_id(node.name)
        func_type = self._get_function_type(node)
        parameters = [arg.arg for arg in node.args.args]

        # Create node
        self.builder.nodes[func_id] = CallNode(
            name=node.name,
            module=self.builder.module,
            class_name=self.current_class,
            line_number=node.lineno,
            type=func_type,
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
            docstring=ast.get_docstring(node),
            parameters=parameters,
        )

        # Process function body
        previous_function = self.current_function
        self.current_function = func_id
        self.generic_visit(node)
        self.current_function = previous_function

    def visit_Call(self, node: ast.Call):
        """Process function calls"""
        if self.current_function is None:
            return self.generic_visit(node)

        called_func_id = self._get_call_target(node)
        if called_func_id:
            self.builder.edges.append((self.current_function, called_func_id))
            if "::" not in called_func_id:  # External dependency
                self.builder.external_deps.add(called_func_id)

        self.generic_visit(node)

    def _get_function_id(self, func_name: str) -> str:
        """Generate unique identifier for a function"""
        if self.current_class:
            return f"{self.builder.module}::{self.current_class}::{func_name}"
        return f"{self.builder.module}::{func_name}"

    def _get_function_type(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> str:
        """Determine the type of function"""
        if not self.current_class:
            return "function"

        decorators = {self._get_decorator_name(d) for d in node.decorator_list}
        if "@staticmethod" in decorators:
            return "static_method"
        elif "@classmethod" in decorators:
            return "class_method"
        return "method"

    def _get_decorator_name(self, node: ast.expr) -> str:
        """Extract decorator name from AST node"""
        if isinstance(node, ast.Name):
            return f"@{node.id}"
        elif isinstance(node, ast.Attribute):
            return f"@{self._get_attribute_name(node)}"
        elif isinstance(node, ast.Call):
            return f"@{self._get_call_name(node)}"
        return str(node)

    def _get_call_target(self, node: ast.Call) -> Optional[str]:
        """Determine the target of a function call"""
        if isinstance(node.func, ast.Name):
            return self._resolve_name(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            return self._resolve_attribute(node.func)
        return None

    def _resolve_name(self, name: str) -> str:
        """Resolve a simple name to its full path"""
        return self.imports.get(name, name)

    def _resolve_attribute(self, node: ast.Attribute) -> str:
        """Resolve an attribute access to its full path"""
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value

        if isinstance(current, ast.Name):
            parts.append(current.id)
        else:
            return None

        return ".".join(reversed(parts))

    def _get_call_name(self, node: ast.Call) -> str:
        """Get the name of a call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return self._get_attribute_name(node.func)
        return str(node.func)

    def _get_attribute_name(self, node: ast.Attribute) -> str:
        """Get the full name of an attribute node"""
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))
