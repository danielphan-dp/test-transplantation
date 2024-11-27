import ast
import json
import stdlib_list
import pkg_resources
from pathlib import Path
from typing import List, Optional, Set, Dict
import os
from tqdm import tqdm
import logging
import click

from pydantic import BaseModel, Field


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
    methods_under_test: List[Dict[str, str]] = Field(default_factory=list)


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
            assertions.append(ast.unparse(sub_node))
    return assertions


def extract_mocks(node: ast.FunctionDef) -> List[str]:
    mocks = []
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Attribute):
            if sub_node.func.attr in ["patch", "Mock", "MagicMock"]:
                mocks.append(ast.unparse(sub_node))
    return mocks


def extract_methods_under_test(
    node: ast.FunctionDef, 
    application_modules: Set[str], 
    standard_lib_names: Set[str],
    third_party_lib_names: Set[str],
    source_files: Dict[str, ast.Module]
) -> List[Dict[str, str]]:
    methods_under_test = []
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Call):
            func_name = get_full_func_name(sub_node.func)
            if func_name and not is_standard_or_third_party(func_name, standard_lib_names, third_party_lib_names):
                method_info = resolve_method(func_name, source_files)
                if method_info:
                    methods_under_test.append(method_info)
    return methods_under_test


def get_full_func_name(func) -> Optional[str]:
    if isinstance(func, ast.Name):
        return func.id
    elif isinstance(func, ast.Attribute):
        value = func.value
        attr = func.attr
        if isinstance(value, ast.Name):
            return f"{value.id}.{attr}"
        elif isinstance(value, ast.Attribute):
            parent = get_full_func_name(value)
            if parent:
                return f"{parent}.{attr}"
    return None


def is_standard_or_third_party(func_name: str, standard_lib_names: Set[str], third_party_lib_names: Set[str]) -> bool:
    module_name = func_name.split('.')[0]
    return module_name in standard_lib_names or module_name in third_party_lib_names


def get_standard_library_names() -> Set[str]:
    return set(stdlib_list.stdlib_list())


def get_third_party_library_names() -> Set[str]:
    return {pkg.key for pkg in pkg_resources.working_set}


def resolve_method(func_name: str, source_files: Dict[str, ast.Module]) -> Optional[Dict[str, str]]:
    parts = func_name.split('.')
    for file_path, tree in source_files.items():
        for node in ast.walk(tree):
            if len(parts) > 1 and isinstance(node, ast.ClassDef) and node.name == parts[-2]:
                for sub_node in node.body:
                    if isinstance(sub_node, ast.FunctionDef) and sub_node.name == parts[-1]:
                        return {
                            'name': func_name,
                            'body': ast.unparse(sub_node)
                        }
            elif isinstance(node, ast.FunctionDef) and node.name == parts[-1]:
                return {
                    'name': func_name,
                    'body': ast.unparse(node)
                }
    return None


def scan_source_files(directory: str) -> Dict[str, ast.Module]:
    source_files = {}
    all_files = list(Path(directory).rglob('*.py'))
    
    with tqdm(total=len(all_files), desc="Scanning source files", unit="file") as pbar:
        for file_path in all_files:
            pbar.set_postfix_str(f"Scanning: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_files[str(file_path)] = ast.parse(f.read())
            except Exception as e:
                logger.error(f"Error parsing file {file_path}: {str(e)}")
            pbar.update(1)
    
    logger.info(f"Scanned {len(source_files)} source files")
    return source_files


def collect_tests(directory: str, application_modules: Set[str]) -> TestCollection:
    logger.info(f"Starting test collection from directory: {directory}")
    test_collection = TestCollection()
    directory_path = Path(directory)

    logger.info("Gathering standard and third-party libraries")
    standard_lib_names = get_standard_library_names()
    third_party_lib_names = get_third_party_library_names()

    logger.info("Scanning source files")
    source_files = scan_source_files(directory)

    test_files = list(directory_path.rglob("test_*.py"))
    logger.info(f"Found {len(test_files)} test files")

    for test_file in tqdm(test_files, desc="Collecting tests", unit="file"):
        logger.info(f"Processing test file: {test_file}")
        with open(test_file, "r", encoding="utf-8") as file:
            file_content = file.read()
            tree = ast.parse(file_content, filename=str(test_file))

            imports = extract_imports(tree)
            setup_method = None
            teardown_method = None

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name == "setup_method":
                        setup_method = ast.get_source_segment(file_content, node)
                    elif node.name == "teardown_method":
                        teardown_method = ast.get_source_segment(file_content, node)

                    if node.name.startswith("test_"):
                        logger.debug(f"Found test method: {node.name}")
                        source_code = ast.get_source_segment(file_content, node)
                        docstring = ast.get_docstring(node)
                        decorators = [ast.unparse(d) for d in node.decorator_list]
                        arguments = [arg.arg for arg in node.args.args]
                        fixtures = extract_fixtures(node)
                        assertions = extract_assertions(node)
                        mocks = extract_mocks(node)
                        methods_under_test = extract_methods_under_test(
                            node, 
                            application_modules, 
                            standard_lib_names,
                            third_party_lib_names,
                            source_files
                        )

                        test_collection.tests.append(
                            TestCase(
                                name=node.name,
                                module=test_file.stem,
                                file_path=str(test_file),
                                line_number=node.lineno,
                                end_line_number=node.end_lineno if hasattr(node, "end_lineno") else node.lineno,
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
                                methods_under_test=methods_under_test
                            )
                        )
                elif isinstance(node, ast.ClassDef):
                    logger.debug(f"Found test class: {node.name}")
                    class_setup_method = next(
                        (
                            ast.get_source_segment(file_content, m)
                            for m in node.body
                            if isinstance(m, ast.FunctionDef) and m.name == "setup_method"
                        ),
                        None,
                    )
                    class_teardown_method = next(
                        (
                            ast.get_source_segment(file_content, m)
                            for m in node.body
                            if isinstance(m, ast.FunctionDef) and m.name == "teardown_method"
                        ),
                        None,
                    )

                    for sub_node in node.body:
                        if isinstance(sub_node, ast.FunctionDef) and sub_node.name.startswith("test_"):
                            source_code = ast.get_source_segment(file_content, sub_node)
                            docstring = ast.get_docstring(sub_node)
                            decorators = [ast.unparse(d) for d in sub_node.decorator_list]
                            arguments = [arg.arg for arg in sub_node.args.args]
                            fixtures = extract_fixtures(sub_node)
                            assertions = extract_assertions(sub_node)
                            mocks = extract_mocks(sub_node)
                            methods_under_test = extract_methods_under_test(
                                sub_node, 
                                application_modules, 
                                standard_lib_names,
                                third_party_lib_names,
                                source_files
                            )

                            test_collection.tests.append(
                                TestCase(
                                    name=sub_node.name,
                                    module=test_file.stem,
                                    class_name=node.name,
                                    file_path=str(test_file),
                                    line_number=sub_node.lineno,
                                    end_line_number=(
                                        sub_node.end_lineno if hasattr(sub_node, "end_lineno") else sub_node.lineno
                                    ),
                                    source_code=source_code,
                                    docstring=docstring,
                                    decorators=decorators,
                                    arguments=arguments,
                                    imports=imports,
                                    fixtures=fixtures,
                                    assertions=assertions,
                                    setup_method=class_setup_method,
                                    teardown_method=class_teardown_method,
                                    mocks=mocks,
                                    methods_under_test=methods_under_test
                                )
                            )

    logger.info(f"Collected {len(test_collection.tests)} tests in total")
    return test_collection


def dump_tests_to_json(test_collection: TestCollection, output_file: str):
    logger.info(f"Dumping {len(test_collection.tests)} tests to JSON: {output_file}")
    # Create the output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(test_collection.model_dump(), f, indent=2)
    logger.info(f"JSON dump completed: {output_file}")


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@click.command()
@click.argument('repo_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('output_path', type=click.Path(file_okay=True, dir_okay=False))
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']), default='INFO', help='Set the logging level')
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

    # Add empty set for application_modules
    collected_tests = collect_tests(tests_dir, set())
    dump_tests_to_json(collected_tests, output_path)
    logger.info(f"Collected {len(collected_tests.tests)} tests and saved to {output_path}")

    logger.info("Test collection process completed")

if __name__ == "__main__":
    main()
