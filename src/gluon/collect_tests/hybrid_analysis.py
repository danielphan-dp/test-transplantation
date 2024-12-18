import sys
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from contextlib import contextmanager
import click
import pytest
import coverage
import ast
import stdlib_list
import pkg_resources
import astroid
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    filename="hybrid_analysis.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a global cache
ast_cache = {}

# -----------------------------------------------------------------------------
# Classes and Functions from static_analysis.py
# -----------------------------------------------------------------------------


class MethodUnderTest(BaseModel):
    name: str
    body: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None


class TestCase(BaseModel):
    name: str
    module: str
    class_name: Optional[str] = None
    file_path: str
    line_number: int
    end_line_number: int
    source_code: str
    docstring: Optional[str] = None
    decorators: List[str] = Field(default_factory=list)
    arguments: List[str] = Field(default_factory=list)
    imports: List[str] = Field(default_factory=list)
    fixtures: List[str] = Field(default_factory=list)
    assertions: List[str] = Field(default_factory=list)
    setup_method: Optional[str] = None
    teardown_method: Optional[str] = None
    mocks: List[str] = Field(default_factory=list)
    methods_under_test: List[MethodUnderTest] = Field(default_factory=list)


class TestCollection(BaseModel):
    tests: List[TestCase] = Field(default_factory=list)


def extract_imports(tree: ast.AST) -> List[str]:
    imports = []
    if tree is None:
        return imports
    for node in ast.walk(tree):
        if node is None:
            continue
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.extend(f"{module}.{alias.name}" for alias in node.names)
    return imports


def extract_fixtures(node: ast.FunctionDef) -> List[str]:
    return [
        d.args[0].s
        for d in node.decorator_list
        if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "fixture"
    ]


def extract_assertions(node: ast.FunctionDef) -> List[str]:
    assertions = []
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Assert):
            try:
                assertion_code = ast.unparse(sub_node)
            except Exception as e:
                logger.warning(f"Could not unparse assertion: {e}")
                assertion_code = ""
            assertions.append(assertion_code)
        elif isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Name):
            if sub_node.func.id.startswith("assert") or sub_node.func.id.startswith("self.assert"):
                try:
                    assertion_code = ast.unparse(sub_node)
                except Exception as e:
                    logger.warning(f"Could not unparse assertion call: {e}")
                    assertion_code = ""
                assertions.append(assertion_code)
    return assertions


def extract_mocks(node: ast.FunctionDef) -> List[str]:
    mocks = []
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Name):
            if sub_node.func.id in ["patch", "patch.object"]:
                try:
                    mock_code = ast.unparse(sub_node)
                except Exception as e:
                    logger.warning(f"Could not unparse mock: {e}")
                    mock_code = ""
                mocks.append(mock_code)
    return mocks


def get_standard_library_names() -> Set[str]:
    return set(stdlib_list.stdlib_list())


def get_third_party_library_names() -> Set[str]:
    third_party_packages = {dist.key for dist in pkg_resources.working_set}
    return third_party_packages


def scan_source_files(directory: str) -> Dict[str, Tuple[str, ast.Module]]:
    """
    Modified to include a global or module-level cache of parsed ASTs.
    This prevents re-parsing the same file multiple times when it's
    referenced repeatedly during analysis.
    """
    global ast_cache
    source_files = {}
    directory_path = Path(directory)
    source_file_paths = list(directory_path.rglob("*.py"))
    logger.info(f"Scanned {len(source_file_paths)} source files")

    for source_file in source_file_paths:
        source_file_str = str(source_file)
        if source_file_str in ast_cache:
            # If we've already parsed this file, pull from the cache
            content, tree = ast_cache[source_file_str]
            source_files[source_file_str] = (content, tree)
            continue

        try:
            with open(source_file, "r", encoding="utf-8") as file:
                content = file.read()

            tree = ast.parse(content, filename=source_file_str)
            if tree is None:
                logger.warning(f"AST parse returned None for {source_file}")
                continue

            # Store in local result and in cache
            source_files[source_file_str] = (content, tree)
            ast_cache[source_file_str] = (content, tree)
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.warning(f"Failed to parse {source_file}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error parsing {source_file}: {e}")
    return source_files


def get_full_func_name(node, scope: Dict[str, str] = None) -> Optional[str]:
    if node is None:
        return None
    if isinstance(node, ast.Name):
        return scope.get(node.id, node.id) if scope else node.id
    elif isinstance(node, ast.Attribute):
        value = get_full_func_name(node.value, scope)
        if value:
            return f"{value}.{node.attr}"
        else:
            return node.attr
    elif isinstance(node, ast.Call):
        return get_full_func_name(node.func, scope)
    elif isinstance(node, ast.Subscript):
        return get_full_func_name(node.value, scope)
    elif isinstance(node, ast.Lambda):
        return "<lambda>"
    else:
        return None


def is_standard_or_third_party(
    func_name: str,
    standard_lib_names: Set[str],
    third_party_lib_names: Set[str],
) -> bool:
    if not func_name:
        return False
    module_name = func_name.split(".")[0]
    return module_name in standard_lib_names or module_name in third_party_lib_names


def resolve_method(
    func_name: str, current_module: str, source_files: Dict[str, Tuple[str, ast.Module]]
) -> Optional[Dict[str, Any]]:
    # First, attempt to find the method in the current module
    file_content, tree = source_files.get(current_module, (None, None))
    if tree:
        method_info = find_method_in_tree(tree, func_name)
        if method_info:
            method_info["file_path"] = current_module
            return method_info

    # Next, search imported modules
    imports = get_imports_from_module(tree)
    for imported_module in imports:
        module_path = resolve_module_path(imported_module, set(source_files.keys()))
        if module_path:
            file_content, tree = source_files.get(module_path, (None, None))
            method_info = find_method_in_tree(tree, func_name)
            if method_info:
                method_info["file_path"] = module_path
                return method_info

    return None


def handle_decorator(decorator: ast.AST, source_files: Dict[str, Tuple[str, ast.Module]]):
    decorator_name = get_full_func_name(decorator)

    # Check if the decorator is a route or endpoint registration
    if decorator_name and decorator_name.endswith(
        (".route", ".get", ".post", ".put", ".delete", ".patch", ".options", ".head")
    ):
        # Retrieve the method that is being decorated
        function_node = decorator.parent
        if isinstance(function_node, ast.FunctionDef):
            method_name = function_node.name
            file_path = getattr(function_node, "file_path", "")
            line_number = function_node.lineno
            source_code = ast.get_source_segment(function_node, function_node) or ""
            return {
                "name": method_name,
                "body": source_code,
                "file_path": file_path,
                "line_number": line_number,
            }
    return None


def extract_methods_under_test(
    node: ast.FunctionDef,
    current_module: str,
    application_modules: Set[str],
    standard_lib_names: Set[str],
    third_party_lib_names: Set[str],
    source_files: Dict[str, Tuple[str, ast.Module]],
    scope: Dict[str, str] = None,
) -> List[MethodUnderTest]:
    methods_under_test = []

    def is_relevant_call(func_name):
        return func_name is not None and not is_standard_or_third_party(
            func_name, standard_lib_names, third_party_lib_names
        )

    def process_call(call_node):
        if call_node is None or not hasattr(call_node, "func"):
            return
        func_name = get_full_func_name(call_node.func, scope)
        logger.debug(f"Processing call to function: {func_name}")
        if func_name and is_relevant_call(func_name):
            method_info = resolve_method(func_name, current_module, source_files)
            if method_info:
                methods_under_test.append(MethodUnderTest(**method_info))
            else:
                # Attempt to resolve using astroid
                method_info = resolve_method_with_astroid(func_name, current_module)
                if method_info:
                    methods_under_test.append(MethodUnderTest(**method_info))
                else:
                    # Fallback method under test
                    methods_under_test.append(
                        MethodUnderTest(
                            name=func_name,
                            body="",
                            file_path="",
                            line_number=0,
                        )
                    )
        else:
            logger.debug(f"Ignoring standard or third-party function: {func_name}")

    # Add null checks for node
    if node is None:
        return methods_under_test

    for sub_node in ast.walk(node):
        if sub_node is None:
            continue
        if isinstance(sub_node, ast.Call):
            process_call(sub_node)
        elif isinstance(sub_node, ast.With):
            for item in sub_node.items:
                if item is None:
                    continue
                context_expr = getattr(item, "context_expr", None)
                if isinstance(context_expr, ast.Call):
                    process_call(context_expr)

    # Handle decorators with null check
    if hasattr(node, "decorator_list"):
        for decorator in node.decorator_list:
            if decorator is None:
                continue
            method_info = handle_decorator(decorator, source_files)
            if method_info:
                methods_under_test.append(MethodUnderTest(**method_info))

    return methods_under_test


def process_test_function(
    node: ast.FunctionDef,
    test_file: Path,
    file_content: str,
    imports: List[str],
    setup_method: Optional[str],
    teardown_method: Optional[str],
    standard_lib_names: Set[str],
    third_party_lib_names: Set[str],
    source_files: Dict[str, Tuple[str, ast.Module]],
    class_name: Optional[str] = None,
) -> Optional[TestCase]:
    logger.debug(f"Found test method: {node.name}")
    source_code = ast.get_source_segment(file_content, node) or ""
    docstring = ast.get_docstring(node)
    decorators = []
    for d in node.decorator_list:
        try:
            decorator_code = ast.unparse(d)
        except Exception as e:
            logger.warning(f"Could not unparse decorator: {e}")
            decorator_code = ""
        decorators.append(decorator_code)
    arguments = [arg.arg for arg in node.args.args]
    fixtures = extract_fixtures(node)
    assertions = extract_assertions(node)
    mocks = extract_mocks(node)
    methods_under_test = extract_methods_under_test(
        node,
        str(test_file),
        set(),
        standard_lib_names,
        third_party_lib_names,
        source_files,
    )

    return TestCase(
        name=node.name,
        module=test_file.stem,
        class_name=class_name,
        file_path=str(test_file),
        line_number=node.lineno,
        end_line_number=getattr(node, "end_lineno", node.lineno),
        source_code=source_code,
        docstring=docstring,
        decorators=decorators,
        arguments=arguments,
        imports=imports,
        fixtures=fixtures,
        assertions=assertions,
        setup_method=setup_method,
        teardown_method=teardown_method,
        mocks=mocks,
        methods_under_test=methods_under_test,
    )


def collect_tests(directory: str, application_modules: Set[str], output_dir: Optional[str] = None) -> TestCollection:
    logger.info(f"Starting test collection from directory: {directory}")
    test_collection = TestCollection()
    directory_path = Path(directory)

    logger.info("Gathering standard and third-party libraries")
    standard_lib_names = get_standard_library_names()
    third_party_lib_names = get_third_party_library_names()

    logger.info("Scanning source files")
    repo_root = directory_path.resolve()
    source_files = scan_source_files(str(repo_root))

    test_files = list(directory_path.rglob("test_*.py")) + list(directory_path.rglob("*_test.py"))
    logger.info(f"Found {len(test_files)} test files")

    for test_file in tqdm(test_files, desc="Collecting tests", unit="file"):
        logger.info(f"Processing test file: {test_file}")
        try:
            with open(test_file, "r", encoding="utf-8") as file:
                file_content = file.read()
                # Parse the AST
                tree = ast.parse(file_content, filename=str(test_file))
                if tree is None:
                    logger.warning(f"AST parse returned None for {test_file}")
                    continue
                # Add parent references to the AST nodes
                add_parent_references(tree)
        except Exception as e:
            logger.error(f"Failed to process {test_file}: {e}")
            continue

        imports = extract_imports(tree)
        setup_method = None
        teardown_method = None

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "setup_method":
                    setup_method = ast.get_source_segment(file_content, node) or ""
                elif node.name == "teardown_method":
                    teardown_method = ast.get_source_segment(file_content, node) or ""
                elif node.name.startswith("test_"):
                    test_case = process_test_function(
                        node,
                        test_file,
                        file_content,
                        imports,
                        setup_method,
                        teardown_method,
                        standard_lib_names,
                        third_party_lib_names,
                        source_files,
                    )
                    if test_case:
                        test_collection.tests.append(test_case)
            elif isinstance(node, ast.ClassDef):
                class_setup_method = None
                class_teardown_method = None
                for class_node in node.body:
                    if isinstance(class_node, ast.FunctionDef):
                        if class_node.name == "setup_method":
                            class_setup_method = ast.get_source_segment(file_content, class_node) or ""
                        elif class_node.name == "teardown_method":
                            class_teardown_method = ast.get_source_segment(file_content, class_node) or ""
                for class_node in node.body:
                    if isinstance(class_node, ast.FunctionDef) and class_node.name.startswith("test_"):
                        test_case = process_test_function(
                            class_node,
                            test_file,
                            file_content,
                            imports,
                            class_setup_method,
                            class_teardown_method,
                            standard_lib_names,
                            third_party_lib_names,
                            source_files,
                            class_name=node.name,
                        )
                        if test_case:
                            test_collection.tests.append(test_case)

    logger.info(f"Collected {len(test_collection.tests)} tests in total")

    # -------------------------------------------------------------------------
    # Optional: Write out the collected test metadata to a JSON file
    # -------------------------------------------------------------------------
    if output_dir:
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            tests_output_file = output_path / "collected_tests.json"
            with open(tests_output_file, "w", encoding="utf-8") as f:
                json.dump(test_collection.model_dump(), f, indent=2)
            logger.info(f"Wrote collected test metadata to {tests_output_file}")
        except Exception as e:
            logger.error(f"Failed to write test collection file: {e}")
    # -------------------------------------------------------------------------

    return test_collection


def add_parent_references(node, parent=None):
    if node is None:
        return
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        if child is None:
            continue
        add_parent_references(child, node)


def resolve_method_with_astroid(func_name: str, source_file: str) -> Optional[Dict[str, Any]]:
    try:
        with open(source_file, "r", encoding="utf-8") as f:
            code = f.read()
        module = astroid.parse(code)
        for node in module.body:
            if isinstance(node, astroid.FunctionDef) and node.name == func_name:
                return {
                    "name": node.name,
                    "body": node.as_string(),
                    "file_path": source_file,
                    "line_number": node.lineno,
                }
            elif isinstance(node, astroid.ClassDef):
                for class_node in node.body:
                    if isinstance(class_node, astroid.FunctionDef) and class_node.name == func_name:
                        return {
                            "name": f"{node.name}.{class_node.name}",
                            "body": class_node.as_string(),
                            "file_path": source_file,
                            "line_number": class_node.lineno,
                        }
    except Exception as e:
        logger.warning(f"Failed to resolve method {func_name} using astroid: {e}")
    return None


def find_method_in_tree(tree: ast.AST, func_name: str) -> Optional[Dict[str, Any]]:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
            source_code = ast.get_source_segment(tree, node) or ""
            return {
                "name": node.name,
                "body": source_code,
                "line_number": node.lineno,
            }
        elif isinstance(node, ast.ClassDef):
            for class_node in node.body:
                if isinstance(class_node, (ast.FunctionDef, ast.AsyncFunctionDef)) and class_node.name == func_name:
                    source_code = ast.get_source_segment(tree, class_node) or ""
                    return {
                        "name": f"{node.name}.{class_node.name}",
                        "body": source_code,
                        "line_number": class_node.lineno,
                    }
    return None


def get_imports_from_module(tree: ast.AST) -> List[str]:
    if tree is None:
        return []
    imports = []
    for node in ast.walk(tree):
        if node is None:
            continue
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
            else:
                # Handle relative imports like 'from . import module'
                imports.append("")
    return imports


def resolve_module_path(module_name: str, source_file_paths: Set[str]) -> Optional[str]:
    module_parts = module_name.split(".")
    possible_paths = [
        os.path.join(*module_parts) + ".py",
        os.path.join(*module_parts, "__init__.py"),
    ]
    for file_path in source_file_paths:
        for possible_path in possible_paths:
            if file_path.endswith(possible_path):
                return file_path
    return None


# -----------------------------------------------------------------------------
# Rest of hybrid_analysis.py implementation
# -----------------------------------------------------------------------------


class MethodCallTracer:
    def __init__(self, package_path: str):
        self.package_path = package_path
        self.calls = []
        self.ignore_paths = {"site-packages", "dist-packages", "lib/python"}
        self.current_thread = threading.current_thread()

    def should_trace(self, filename: str) -> bool:
        """Check if this file should be traced"""
        if not filename:
            return False
        filename = os.path.normpath(filename)
        package_path = os.path.normpath(self.package_path)
        return filename.startswith(package_path) and not any(p in filename for p in self.ignore_paths)

    def trace_calls(self, frame, event, arg):
        """Trace function calls, including those wrapped by decorators."""
        if event != "call":
            return

        code = frame.f_code
        filename = code.co_filename

        if not self.should_trace(filename):
            return

        func_name = code.co_name

        # Attempt to get the qualified name, handling decorators
        qualified_name = self.get_qualified_name(frame)

        # Get the class name if this is a method
        if "self" in frame.f_locals:
            cls = frame.f_locals["self"].__class__
            func_name = f"{cls.__name__}.{func_name}"
        elif "cls" in frame.f_locals:
            cls = frame.f_locals["cls"]
            func_name = f"{cls.__name__}.{func_name}"

        lineno = frame.f_lineno

        # Get the caller function name
        caller_frame = frame.f_back
        caller_name = caller_frame.f_code.co_name if caller_frame else None

        call_info = {
            "function": qualified_name or func_name,
            "filename": filename,
            "line": lineno,
            "caller": caller_name,
        }

        self.calls.append(call_info)
        return

    def get_qualified_name(self, frame):
        """Attempt to get the qualified name of the current function."""
        func = frame.f_globals.get(frame.f_code.co_name)
        if func:
            try:
                return func.__qualname__
            except AttributeError:
                pass
        return frame.f_code.co_name

    @contextmanager
    def trace_context(self, test_name: str):
        """Context manager for tracing"""
        self.calls = []
        old_trace = sys.gettrace()
        sys.settrace(self.trace_calls)
        try:
            yield
        finally:
            sys.settrace(old_trace)


class TestAnalyzer:
    def __init__(self, repo_path: str, tests_dir: Optional[str] = None):
        self.repo_path = Path(repo_path)
        self.package_path = str(self.repo_path.resolve())
        self.tests_dir = Path(tests_dir) if tests_dir else self.repo_path
        self.tracer = MethodCallTracer(self.package_path)

    def run_static_analysis(self) -> TestCollection:
        """Run static analysis using collect_tests"""
        return collect_tests(str(self.tests_dir), set())

    def run_test_with_coverage(self, test_case: Dict) -> Tuple[List[Dict], bool]:
        """Run a test case and collect coverage data."""
        test_path = Path(test_case["file_path"]).resolve()
        test_name = test_case["name"]
        class_name = test_case.get("class_name")
        if class_name:
            test_identifier = f"{test_path}::{class_name}::{test_name}"
        else:
            test_identifier = f"{test_path}::{test_name}"

        env = os.environ.copy()
        env["PYTHONPATH"] = f"{self.package_path}:{env.get('PYTHONPATH', '')}"

        cov = coverage.Coverage(
            source=[self.package_path],
            omit=["*/tests/*"],
            concurrency="thread",
        )
        cov.start()

        try:
            result = pytest.main([test_identifier], env=env)
        finally:
            cov.stop()
            cov.save()

        success = result == 0
        coverage_data = self.process_coverage_data(cov)

        return coverage_data, success

    def process_coverage_data(self, cov: coverage.Coverage) -> List[Dict]:
        """Process coverage data to extract executed methods."""
        coverage_data = []
        data = cov.get_data()
        for file_path in data.measured_files():
            executed_lines = data.lines(file_path) or []
            with open(file_path, "r") as f:
                source = f.read()
            tree = ast.parse(source, filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    function_lines = set(range(node.lineno, getattr(node, "end_lineno", node.lineno) + 1))
                    if function_lines & set(executed_lines):
                        func_name = node.name
                        coverage_data.append(
                            {
                                "function": func_name,
                                "filename": file_path,
                                "line": node.lineno,
                            }
                        )
        return coverage_data

    def analyze_test(self, test_case: Dict) -> Dict:
        """Analyze a single test case using both static and dynamic analysis"""
        try:
            # Static analysis results
            static_methods = []
            for method in test_case["methods_under_test"]:
                # Include the method name and its source code
                source_code = ""
                file_path = method.get("file_path", "")
                if file_path and os.path.exists(file_path):
                    try:
                        with open(file_path, "r") as f:
                            source_lines = f.readlines()
                        line_number = method.get("line_number", 0)
                        if line_number > 0:
                            # Extract full method source code
                            method_lines = []
                            i = line_number - 1
                            # Get the method signature
                            method_lines.append(source_lines[i].rstrip())
                            # Get the method body
                            i += 1
                            while i < len(source_lines) and (
                                source_lines[i].strip() and source_lines[i].startswith(" " * 4)
                            ):
                                method_lines.append(source_lines[i].rstrip())
                                i += 1
                            source_code = "\n".join(method_lines)
                    except Exception as e:
                        logger.warning(f"Could not extract source code for {method['name']}: {e}")

                static_methods.append(
                    {
                        "name": method["name"],
                        "source_code": source_code,
                        "file_path": method.get("file_path", ""),
                        "line_number": method.get("line_number", 0),
                    }
                )

            # Run the test and get dynamic calls and success status
            traced_calls, success = self.run_test_with_coverage(test_case)

            return {
                "test_name": test_case["name"],
                "test_file": test_case["file_path"],
                "static_methods": static_methods,
                "dynamic_methods": traced_calls,
                "assertions": test_case.get("assertions", []),
                "mocks": test_case.get("mocks", []),
                "success": success,
                "test_source_code": test_case.get("source_code", ""),
            }

        except Exception as e:
            logger.warning(f"Error analyzing test {test_case['name']}: {str(e)}")
            return {
                "test_name": test_case["name"],
                "test_file": test_case["file_path"],
                "static_methods": [],
                "dynamic_methods": [],
                "assertions": [],
                "mocks": [],
                "success": False,
                "error": str(e),
                "test_source_code": test_case.get("source_code", ""),
            }

    def analyze_tests_parallel(self, test_cases, max_workers=None, output_dir=None):
        """Analyze multiple tests in parallel, writing out each result as soon as it completes."""
        analyses = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit each test for analysis
            future_to_test = {
                executor.submit(self.analyze_test, test_case.model_dump()): test_case.name for test_case in test_cases
            }

            # As soon as a future finishes, write out the results
            for future in as_completed(future_to_test):
                test_name = future_to_test[future]
                try:
                    analysis = future.result()
                    analyses.append(analysis)
                    logger.info(f"Completed analysis for {test_name}")

                    if output_dir:
                        # Immediately save this test's analysis to disk
                        out_dir = Path(output_dir)
                        out_dir.mkdir(parents=True, exist_ok=True)

                        # Construct a unique safe filename
                        test_file = analysis.get("test_file", "")
                        class_name = analysis.get("test_class", "")
                        parts = [
                            Path(test_file).stem,
                            class_name if class_name else "",
                            analysis.get("test_name", "unknown_test"),
                        ]
                        safe_parts = [
                            "".join(c if c.isalnum() or c == "_" else "_" for c in part) for part in parts if part
                        ]
                        filename = "__".join(safe_parts) + ".json"

                        analysis_file = out_dir / filename
                        with open(analysis_file, "w") as f:
                            json.dump(analysis, f, indent=2)

                        logger.info(f"Saved analysis for test '{analysis.get('test_name')}' to: {analysis_file}")
                except Exception as e:
                    logger.error(f"Error analyzing test {test_name}: {str(e)}")

        return analyses


def calculate_advanced_metrics(test_collection: TestCollection, analyses: List[Dict]) -> Dict[str, Any]:
    """Calculate metrics based on the test collection and analyses."""
    total_tests = len(test_collection.tests)
    tests_passed = sum(1 for analysis in analyses if analysis.get("success", False))
    tests_failed = total_tests - tests_passed

    # Example additional metrics
    total_assertions = sum(len(analysis.get("assertions", [])) for analysis in analyses)
    average_assertions = total_assertions / total_tests if total_tests else 0

    metrics = {
        "total_tests": total_tests,
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "total_assertions": total_assertions,
        "average_assertions_per_test": average_assertions,
    }
    return metrics


# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------


@click.command()
@click.option(
    "--input-dir",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Repository path to analyze",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    required=True,
    help="Directory to store analysis results",
)
@click.option(
    "--log-file",
    type=click.Path(),
    help="Path to log file (optional)",
)
@click.option("--workers", type=int, default=None, help="Number of worker threads")
def main(input_dir: str, output_dir: str, log_file: str = None, workers: int = None):
    """Analyze unit tests in the given repository."""
    # Set up logging to file if specified
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    if log_file:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(),
            ],
        )
    else:
        logging.basicConfig(level=logging.INFO, format=log_format)

    logger = logging.getLogger(__name__)
    logger.info(f"Starting analysis of {input_dir}")

    analyzer = TestAnalyzer(input_dir, tests_dir=input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Run static analysis
    logger.info("Running static analysis...")
    test_collection = analyzer.run_static_analysis()

    # Analyze each test
    logger.info("\nAnalyzing tests...")
    total_tests = len(test_collection.tests)
    logger.info(f"Total tests to analyze: {total_tests}")

    # Analyze tests in parallel
    analyses = analyzer.analyze_tests_parallel(test_collection.tests, max_workers=workers, output_dir=output_dir)

    # Calculate metrics
    metrics = calculate_advanced_metrics(test_collection, analyses)
    metrics_file = output_path / "metrics.json"
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Saved metrics to: {metrics_file}")


if __name__ == "__main__":
    main()
