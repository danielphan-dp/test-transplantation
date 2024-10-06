import ast
import json
from pathlib import Path
from typing import List, Optional

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


def collect_tests(directory: str) -> TestCollection:
    test_collection = TestCollection()
    directory_path = Path(directory)

    for test_file in directory_path.rglob("test_*.py"):
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
                        source_code = ast.get_source_segment(file_content, node)
                        docstring = ast.get_docstring(node)
                        decorators = [ast.unparse(d) for d in node.decorator_list]
                        arguments = [arg.arg for arg in node.args.args]
                        fixtures = extract_fixtures(node)
                        assertions = extract_assertions(node)
                        mocks = extract_mocks(node)

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
                            )
                        )
                elif isinstance(node, ast.ClassDef):
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
                                )
                            )

    return test_collection


def dump_tests_to_json(test_collection: TestCollection, output_file: str):
    with open(output_file, "w") as f:
        json.dump(test_collection.model_dump(), f, indent=2)


if __name__ == "__main__":
    # Repos for API development
    repo_paths = [
        "./__internal__/data/flask",
        "./__internal__/data/fastapi",
        "./__internal__/data/gunicorn",
        "./__internal__/data/pyramid",
        "./__internal__/data/connexion",
    ]

    for repo_path in repo_paths:
        tests_dir = f"{repo_path}/tests"
        repo_name = Path(repo_path).name
        output_json = f"./__internal__/collected_tests/collected_tests__{repo_name}.json"

        collected_tests = collect_tests(tests_dir)
        dump_tests_to_json(collected_tests, output_json)
        print(f"Collected {len(collected_tests.tests)} tests and saved to {output_json}")
