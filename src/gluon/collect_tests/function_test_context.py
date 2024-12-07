from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
import ast
from collections import defaultdict


@dataclass
class FunctionTestContext:
    """Context for a specific function being tested"""

    # Function metadata
    function_name: str
    module_path: str
    class_name: Optional[str]
    source_code: str  # Full source code of the function
    line_range: tuple[int, int]  # Start and end line numbers

    # Function signature
    parameters: List[Dict[str, str]]  # name, type, default value
    return_type: Optional[str]
    decorators: List[str]

    # Documentation
    docstring: Optional[str]
    type_hints: Dict[str, str]
    parameter_docs: Dict[str, str]  # Parameter descriptions from docstring
    return_doc: Optional[str]  # Return value description from docstring

    # Dependencies
    imports: List[str]
    dependencies: List[str]  # Other functions called
    external_dependencies: Set[str]  # Third-party library dependencies

    # Existing tests
    existing_tests: List[Dict[str, Any]]  # Existing test cases
    test_patterns: List[str]  # Common test patterns for similar functions

    # Test requirements
    required_fixtures: List[Dict[str, Any]]  # Required test fixtures
    mock_patterns: List[Dict[str, Any]]  # Common mocking patterns
    assertion_patterns: List[Dict[str, Any]]  # Common assertion patterns

    # Error handling
    exceptions: List[str]  # Exceptions that might be raised
    error_cases: List[Dict[str, Any]]  # Known error cases to test

    # Test data
    example_inputs: List[Dict[str, Any]]  # Example input values
    example_outputs: List[Any]  # Example output values
    edge_cases: List[Dict[str, Any]]  # Edge cases to test

    # New fields to match analyze_unit_tests.py capabilities
    test_success: bool  # Whether the test passed when executed
    test_complexity: Dict[str, int]  # Metrics about test complexity
    assertion_density: float  # Assertions per line of code
    mock_density: float  # Mocks per test
    test_isolation_level: str  # 'fully_isolated', 'partially_isolated', or 'no_isolation'
    dynamic_calls: List[Dict[str, Any]]  # Methods actually called during test execution

    # Test execution metrics
    execution_time: float  # Time taken to execute the test
    memory_usage: float  # Memory used during test execution


class FunctionContextExtractor:
    """Extracts context for a specific function"""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def extract_context(self, file_path: str, function_name: str) -> FunctionTestContext:
        """Extract comprehensive context for a function"""
        with open(file_path, "r") as f:
            content = f.read()
            tree = ast.parse(content)

        function_node = self._find_function_node(tree, function_name)
        if not function_node:
            raise ValueError(f"Function {function_name} not found in {file_path}")

        class_node = self._find_parent_class(tree, function_node)

        return FunctionTestContext(
            function_name=function_name,
            module_path=file_path,
            class_name=class_node.name if class_node else None,
            source_code=ast.get_source_segment(content, function_node),
            line_range=(function_node.lineno, function_node.end_lineno),
            parameters=self._extract_parameters(function_node),
            return_type=self._extract_return_type(function_node),
            decorators=self._extract_decorators(function_node),
            docstring=self._parse_docstring(function_node),
            type_hints=self._extract_type_hints(function_node),
            parameter_docs=self._extract_parameter_docs(function_node),
            return_doc=self._extract_return_doc(function_node),
            imports=self._extract_imports(tree),
            dependencies=self._extract_dependencies(function_node),
            external_dependencies=self._extract_external_dependencies(tree),
            existing_tests=self._find_existing_tests(file_path, function_name),
            test_patterns=self._analyze_test_patterns(file_path, function_name),
            required_fixtures=self._identify_required_fixtures(function_node),
            mock_patterns=self._analyze_mock_patterns(file_path, function_name),
            assertion_patterns=self._analyze_assertion_patterns(file_path, function_name),
            exceptions=self._extract_exceptions(function_node),
            error_cases=self._identify_error_cases(function_node),
            example_inputs=self._extract_example_inputs(function_node),
            example_outputs=self._extract_example_outputs(function_node),
            edge_cases=self._identify_edge_cases(function_node),
        )

    def _find_function_node(self, tree: ast.AST, function_name: str) -> Optional[ast.FunctionDef]:
        """Find the AST node for the target function"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return node
        return None

    def _find_parent_class(self, tree: ast.AST, function_node: ast.FunctionDef) -> Optional[ast.ClassDef]:
        """Find the parent class of a function if it exists"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if function_node in node.body:
                    return node
        return None

    def _extract_parameters(self, node: ast.FunctionDef) -> List[Dict[str, str]]:
        """Extract function parameters with their types and default values"""
        parameters = []
        for arg in node.args.args:
            param = {"name": arg.arg, "type": ast.unparse(arg.annotation) if arg.annotation else None, "default": None}
            parameters.append(param)

        # Handle defaults
        defaults = [None] * (len(node.args.args) - len(node.args.defaults)) + [
            ast.unparse(default) for default in node.args.defaults
        ]
        for param, default in zip(parameters, defaults):
            param["default"] = default

        return parameters

    def _extract_type_hints(self, node: ast.FunctionDef) -> Dict[str, str]:
        """Extract type hints from function signature and annotations"""
        type_hints = {}

        # Parameter type hints
        for arg in node.args.args:
            if arg.annotation:
                type_hints[arg.arg] = ast.unparse(arg.annotation)

        # Return type hint
        if node.returns:
            type_hints["return"] = ast.unparse(node.returns)

        return type_hints

    def _find_existing_tests(self, file_path: str, function_name: str) -> List[Dict[str, Any]]:
        """Find existing tests for the function"""
        test_files = self._get_potential_test_files(file_path)
        existing_tests = []

        for test_file in test_files:
            if test_file.exists():
                with open(test_file, "r") as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                        # Check if this test references our target function
                        if self._test_references_function(node, function_name):
                            existing_tests.append(
                                {
                                    "name": node.name,
                                    "source": ast.get_source_segment(f.read(), node),
                                    "fixtures": self._extract_fixtures_from_test(node),
                                    "assertions": self._extract_assertions_from_test(node),
                                    "mocks": self._extract_mocks_from_test(node),
                                }
                            )

        return existing_tests

    def _get_potential_test_files(self, file_path: str) -> List[Path]:
        """Get potential test file locations"""
        source_path = Path(file_path)
        return [
            source_path.parent / f"test_{source_path.name}",
            source_path.parent / f"{source_path.stem}_test.py",
            source_path.parent / "tests" / f"test_{source_path.name}",
            self.repo_path / "tests" / f"test_{source_path.name}",
        ]

    def _identify_required_fixtures(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Identify fixtures that would be needed for testing"""
        fixtures = []

        # Analyze function dependencies to determine required fixtures
        dependencies = self._extract_dependencies(node)
        for dep in dependencies:
            if self._might_need_fixture(dep):
                fixtures.append({"name": f"{dep}_fixture", "dependency": dep, "scope": "function"})

        return fixtures

    def _analyze_mock_patterns(self, file_path: str, function_name: str) -> List[Dict[str, Any]]:
        """Analyze common mocking patterns for similar functions"""
        mock_patterns = []

        # Look at existing tests for mocking patterns
        existing_tests = self._find_existing_tests(file_path, function_name)
        for test in existing_tests:
            mocks = self._extract_mocks_from_test(ast.parse(test["source"]))
            if mocks:
                mock_patterns.extend(mocks)

        return mock_patterns

    def _identify_edge_cases(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Identify potential edge cases for testing"""
        edge_cases = []

        # Analyze parameters for potential edge cases
        for param in self._extract_parameters(node):
            param_type = param.get("type")
            if param_type:
                edge_cases.extend(self._get_type_edge_cases(param["name"], param_type))

        return edge_cases

    def _get_type_edge_cases(self, param_name: str, param_type: str) -> List[Dict[str, Any]]:
        """Get edge cases for a specific parameter type"""
        edge_cases = []

        type_edge_cases = {
            "str": ["", "very_long_string" * 100, "special_chars!@#$"],
            "int": [0, -1, 2**31 - 1, -(2**31)],
            "list": [[], [1] * 1000],
            "dict": [{}, {"key": "value" * 1000}],
        }

        if param_type in type_edge_cases:
            for value in type_edge_cases[param_type]:
                edge_cases.append(
                    {"parameter": param_name, "value": value, "description": f"Edge case for {param_type}"}
                )

        return edge_cases
