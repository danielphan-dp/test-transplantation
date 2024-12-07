import sys
import os
import builtins

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import ast
import json
import stdlib_list
import pkg_resources
from pathlib import Path
from typing import List, Optional, Set, Dict, Any, Tuple
import os
from tqdm import tqdm
import logging
import click
import inspect

from pydantic import BaseModel, Field

import astor


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
    for node in ast.walk(tree):
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
    source_files = {}
    directory_path = Path(directory)
    source_file_paths = list(directory_path.rglob("*.py"))
    logger.info(f"Scanned {len(source_file_paths)} source files")
    for source_file in source_file_paths:
        try:
            with open(source_file, "r", encoding="utf-8") as file:
                content = file.read()
            tree = ast.parse(content, filename=str(source_file))
            source_files[str(source_file)] = (content, tree)
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.warning(f"Failed to parse {source_file}: {e}")
    return source_files


def get_full_func_name(node) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        value = get_full_func_name(node.value)
        if value:
            return f"{value}.{node.attr}"
        else:
            return node.attr
    elif isinstance(node, ast.Call):
        return get_full_func_name(node.func)
    elif isinstance(node, ast.Subscript):
        return get_full_func_name(node.value)
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


def resolve_method(func_name: str, source_files: Dict[str, Tuple[str, ast.Module]]) -> Optional[Dict[str, Any]]:
    # Split the function name into parts (e.g., "Class.method" -> ["Class", "method"])
    name_parts = func_name.split(".")
    base_name = name_parts[-1]  # Get the actual method name

    # Handle built-in methods and standard library methods
    if base_name in dir(builtins) or func_name.split(".")[0] in stdlib_list.stdlib_list():
        return {
            "name": func_name,
            "body": f"def {base_name}(...): # Built-in or standard library method",
            "file_path": "<built-in>",
            "line_number": 0,
        }

    for file_path, (source_code, tree) in source_files.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == base_name:
                try:
                    # Get the full method source including decorators and body
                    start_line = min(d.lineno for d in node.decorator_list) if node.decorator_list else node.lineno
                    end_line = node.end_lineno if hasattr(node, "end_lineno") else node.lineno

                    # Find the actual end of the function by looking for the next non-indented line
                    lines = source_code.splitlines()
                    base_indent = len(lines[start_line]) - len(lines[start_line].lstrip())

                    while end_line < len(lines):
                        line = lines[end_line]
                        if line.strip() and len(line) - len(line.lstrip()) <= base_indent:
                            break
                        end_line += 1

                    method_lines = lines[start_line - 1 : end_line]
                    body = "\n".join(method_lines)
                except Exception as e:
                    logger.warning(f"Could not get source segment for {func_name}: {e}")
                    body = ""
                return {"name": func_name, "body": body, "file_path": file_path, "line_number": node.lineno}
            elif isinstance(node, ast.ClassDef):
                # If we're looking for a method within a class
                if len(name_parts) > 1 and node.name == name_parts[0]:
                    for class_node in node.body:
                        if isinstance(class_node, ast.FunctionDef) and class_node.name == base_name:
                            try:
                                # Get the full source code including decorators
                                start_line = (
                                    min(d.lineno for d in class_node.decorator_list)
                                    if class_node.decorator_list
                                    else class_node.lineno
                                )

                                # Find the actual end of the method by looking for the next non-indented line
                                lines = source_code.splitlines()
                                base_indent = len(lines[start_line]) - len(lines[start_line].lstrip())
                                end_line = (
                                    class_node.end_lineno if hasattr(class_node, "end_lineno") else class_node.lineno
                                )

                                while end_line < len(lines):
                                    line = lines[end_line]
                                    if line.strip() and len(line) - len(line.lstrip()) <= base_indent:
                                        break
                                    end_line += 1

                                full_lines = lines[start_line - 1 : end_line]
                                body = "\n".join(full_lines)
                            except Exception as e:
                                logger.warning(f"Could not get source segment for {func_name}: {e}")
                                body = ""
                            return {
                                "name": f"{node.name}.{base_name}",
                                "body": body,
                                "file_path": file_path,
                                "line_number": class_node.lineno,
                            }
    return None


def extract_methods_under_test(
    node: ast.FunctionDef,
    application_modules: Set[str],
    standard_lib_names: Set[str],
    third_party_lib_names: Set[str],
    source_files: Dict[str, Tuple[str, ast.Module]],
) -> List[MethodUnderTest]:
    methods_under_test = []

    def is_relevant_call(func_name):
        return func_name is not None and not is_standard_or_third_party(
            func_name, standard_lib_names, third_party_lib_names
        )

    def process_call(call_node):
        func_name = get_full_func_name(call_node.func)
        logger.debug(f"Processing call to function: {func_name}")
        if func_name and is_relevant_call(func_name):
            method_info = resolve_method(func_name, source_files)
            if method_info:
                methods_under_test.append(MethodUnderTest(**method_info))
            else:
                # Ensure we have default values for optional fields
                methods_under_test.append(
                    MethodUnderTest(
                        name=func_name,
                        body="",  # Empty string instead of None
                        file_path="",  # Empty string instead of None
                        line_number=0,  # Default to 0 instead of None
                    )
                )
        else:
            logger.debug(f"Ignoring standard or third-party function: {func_name}")

    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Call):
            process_call(sub_node)
        elif isinstance(sub_node, ast.With):
            for item in sub_node.items:
                context_expr = getattr(item, "context_expr", None)
                if isinstance(context_expr, ast.Call):
                    process_call(context_expr)

    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call):
            process_call(decorator)
        else:
            decorator_name = get_full_func_name(decorator)
            if decorator_name and is_relevant_call(decorator_name):
                method_info = resolve_method(decorator_name, source_files)
                if method_info:
                    methods_under_test.append(MethodUnderTest(**method_info))
                else:
                    # Ensure we have default values for optional fields
                    methods_under_test.append(
                        MethodUnderTest(
                            name=decorator_name,
                            body="",  # Empty string instead of None
                            file_path="",  # Empty string instead of None
                            line_number=0,  # Default to 0 instead of None
                        )
                    )

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
        node, set(), standard_lib_names, third_party_lib_names, source_files
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


def collect_tests(directory: str, application_modules: Set[str]) -> TestCollection:
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
        with open(test_file, "r", encoding="utf-8") as file:
            file_content = file.read()
            try:
                tree = ast.parse(file_content, filename=str(test_file))
            except SyntaxError as e:
                logger.error(f"Failed to parse {test_file}: {e}")
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
    return test_collection


def dump_tests_to_json(test_collection: TestCollection, output_file: str):
    logger.info(f"Dumping {len(test_collection.tests)} tests to JSON: {output_file}")
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(test_collection.model_dump(), f, indent=2)
    logger.info(f"JSON dump completed: {output_file}")


# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@click.command()
@click.argument("repo_path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("output_path", type=click.Path(file_okay=True, dir_okay=False))
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Set the logging level",
)
def main(repo_path: str, output_path: str, log_level: str):
    """
    Collect unit tests from a repository and save them to a JSON file.

    REPO_PATH: Path to the repository containing the tests
    OUTPUT_PATH: Path to save the output JSON file
    """
    # Set the log level
    logging.getLogger().setLevel(log_level)

    logger.info(f"Starting test collection process for repository: {repo_path}")
    logger.info(f"Output will be saved to: {output_path}")

    tests_dir = os.path.join(repo_path, "tests")
    if not os.path.exists(tests_dir):
        logger.error(f"Tests directory not found: {tests_dir}")
        return

    collected_tests = collect_tests(tests_dir, set())
    logger.info(f"Collected {len(collected_tests.tests)} tests in total")

    logger.info("Starting to dump tests to JSON")
    dump_tests_to_json(collected_tests, output_path)
    logger.info("Finished dumping tests to JSON")

    logger.info("Test collection process completed")


if __name__ == "__main__":
    main()
