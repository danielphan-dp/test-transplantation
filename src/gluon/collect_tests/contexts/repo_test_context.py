from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
import ast
import configparser
from collections import Counter
from typing import List, Set, Iterator, Dict


@dataclass
class RepoTestContext:
    """Core repository testing context"""

    # Test framework and configuration
    test_framework: str  # 'pytest', 'unittest', etc.
    test_configs: Dict[str, any]  # pytest.ini, conftest.py settings

    # Project structure
    test_directory_pattern: str  # Where tests are located
    test_file_pattern: str  # How test files are named (test_*.py, *_test.py)

    # Common patterns
    fixture_patterns: Dict[str, List[str]]  # Common fixtures and their usage patterns
    assertion_patterns: Dict[str, List[str]]  # Common assertion patterns
    mock_patterns: Dict[str, List[str]]  # Common mocking patterns

    # Style conventions
    naming_conventions: Dict[str, str]  # Test naming conventions
    formatting_rules: Dict[str, str]  # Code formatting rules

    # Common imports and dependencies
    common_test_imports: Set[str]  # Frequently used test imports
    common_fixtures: Set[str]  # Commonly used fixtures

    # New fields to match analyze_unit_tests.py capabilities
    test_metrics: Dict[str, Any] = field(
        default_factory=lambda: {
            "total_tests": 0,
            "successful_tests": 0,
            "failed_tests": 0,
            "test_complexity": {
                "simple": 0,  # 0-2 assertions
                "moderate": 0,  # 3-5 assertions
                "complex": 0,  # 6+ assertions
            },
            "coverage_metrics": {
                "methods_with_multiple_tests": 0,
                "untested_methods": 0,
                "average_tests_per_method": 0.0,
            },
            "test_isolation": {
                "fully_isolated": 0,
                "partially_isolated": 0,
                "no_isolation": 0,
            },
        }
    )

    # Method coverage tracking
    method_test_coverage: Dict[str, List[str]] = field(default_factory=dict)  # method -> list of testing functions
    method_call_frequency: Counter = field(default_factory=Counter)  # Tracks how often methods are called

    # Test execution statistics
    test_execution_times: Dict[str, float] = field(default_factory=dict)
    test_memory_usage: Dict[str, float] = field(default_factory=dict)


class RepoContextExtractor:
    """Extracts repository-wide testing context"""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def extract_repo_context(self) -> RepoTestContext:
        """Extract comprehensive repository testing context"""
        return RepoTestContext(
            test_framework=self._detect_test_framework(),
            test_configs=self._extract_test_configs(),
            test_directory_pattern=self._detect_test_directory_pattern(),
            test_file_pattern=self._detect_test_file_pattern(),
            fixture_patterns=self._analyze_fixture_patterns(),
            assertion_patterns=self._analyze_assertion_patterns(),
            mock_patterns=self._analyze_mock_patterns(),
            naming_conventions=self._extract_naming_conventions(),
            formatting_rules=self._extract_formatting_rules(),
            common_test_imports=self._analyze_common_imports(),
            common_fixtures=self._analyze_common_fixtures(),
        )

    def _detect_test_framework(self) -> str:
        """Detect the testing framework used in the repository"""
        # Check for pytest.ini
        if (self.repo_path / "pytest.ini").exists():
            return "pytest"
        # Check for unittest patterns
        if self._scan_for_unittest_patterns():
            return "unittest"
        return "pytest"  # Default to pytest

    def _extract_test_configs(self) -> Dict[str, any]:
        """Extract test configuration from pytest.ini, conftest.py, etc."""
        configs = {}

        # Check pytest.ini
        pytest_ini = self.repo_path / "pytest.ini"
        if pytest_ini.exists():
            configs["pytest_ini"] = self._parse_pytest_ini(pytest_ini)

        # Check conftest.py files
        for conftest in self.repo_path.rglob("conftest.py"):
            configs.setdefault("conftest", []).append(self._parse_conftest(conftest))

        # Check setup.cfg/pyproject.toml for test settings
        if (self.repo_path / "setup.cfg").exists():
            configs["setup_cfg"] = self._parse_setup_cfg()

        return configs

    def _analyze_fixture_patterns(self) -> Dict[str, List[str]]:
        """Analyze common fixture patterns in the repository"""
        patterns = {}
        fixture_usages = []

        # Scan all test files for fixture usage
        for test_file in self._find_test_files():
            fixtures = self._extract_fixtures_from_file(test_file)
            fixture_usages.extend(fixtures)

        # Group fixtures by pattern
        for fixture in fixture_usages:
            pattern_key = self._categorize_fixture_pattern(fixture)
            patterns.setdefault(pattern_key, []).append(fixture)

        return patterns

    def _analyze_assertion_patterns(self) -> Dict[str, List[str]]:
        """Analyze common assertion patterns in tests"""
        patterns = {}

        for test_file in self._find_test_files():
            assertions = self._extract_assertions_from_file(test_file)
            for assertion in assertions:
                pattern_key = self._categorize_assertion_pattern(assertion)
                patterns.setdefault(pattern_key, []).append(assertion)

        return patterns

    def _extract_naming_conventions(self) -> Dict[str, str]:
        """Extract test naming conventions"""
        conventions = {
            "test_prefix": "test_",  # Default
            "test_suffix": "",
            "class_prefix": "Test",
            "class_suffix": "",
        }

        # Analyze existing test names to detect patterns
        test_names = []
        for test_file in self._find_test_files():
            test_names.extend(self._extract_test_names(test_file))

        if test_names:
            conventions.update(self._analyze_naming_patterns(test_names))

        return conventions

    def _analyze_common_imports(self) -> Set[str]:
        """Analyze commonly used imports in tests"""
        import_counts = {}

        for test_file in self._find_test_files():
            imports = self._extract_imports_from_file(test_file)
            for imp in imports:
                import_counts[imp] = import_counts.get(imp, 0) + 1

        # Return imports used in more than 20% of test files
        threshold = len(list(self._find_test_files())) * 0.2
        return {imp for imp, count in import_counts.items() if count >= threshold}

    def _find_test_files(self) -> Iterator[Path]:
        """Find all test files in the repository"""
        test_patterns = ["test_*.py", "*_test.py"]
        test_files = set()

        for pattern in test_patterns:
            test_files.update(self.repo_path.rglob(pattern))

        # Also check explicit test directories
        test_dirs = ["tests", "test"]
        for test_dir in test_dirs:
            test_dir_path = self.repo_path / test_dir
            if test_dir_path.exists():
                test_files.update(test_dir_path.rglob("*.py"))

        return iter(sorted(test_files))

    def _parse_pytest_ini(self, ini_path: Path) -> Dict[str, any]:
        """Parse pytest.ini configuration"""
        config = configparser.ConfigParser()
        config.read(str(ini_path))

        pytest_config = {}
        if "pytest" in config:
            pytest_config.update(dict(config["pytest"]))

        return pytest_config

    def _parse_conftest(self, conftest_path: Path) -> Dict[str, any]:
        """Parse conftest.py to extract fixtures and configuration"""
        with open(conftest_path, "r") as f:
            tree = ast.parse(f.read())

        fixtures = []
        configs = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Look for fixtures
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call):
                        if isinstance(decorator.func, ast.Name) and decorator.func.id == "fixture":
                            fixtures.append(
                                {
                                    "name": node.name,
                                    "docstring": ast.get_docstring(node),
                                    "params": [arg.arg for arg in node.args.args],
                                }
                            )

            # Look for pytest configuration variables
            elif isinstance(node, ast.Assign):
                if isinstance(node.targets[0], ast.Name):
                    if node.targets[0].id.startswith("pytest_"):
                        configs[node.targets[0].id] = ast.unparse(node.value)

        return {"fixtures": fixtures, "configs": configs, "path": str(conftest_path)}

    def _extract_fixtures_from_file(self, file_path: Path) -> List[Dict[str, any]]:
        """Extract fixtures and their usage from a test file"""
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        fixtures = []

        for node in ast.walk(tree):
            # Find fixture definitions
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call):
                        if isinstance(decorator.func, ast.Name) and decorator.func.id == "fixture":
                            fixtures.append(
                                {"name": node.name, "type": "definition", "docstring": ast.get_docstring(node)}
                            )

            # Find fixture usage in test functions
            elif isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                for arg in node.args.args:
                    fixtures.append({"name": arg.arg, "type": "usage", "test_function": node.name})

        return fixtures

    def _extract_assertions_from_file(self, file_path: Path) -> List[Dict[str, any]]:
        """Extract assertion patterns from a test file"""
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        assertions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                assertions.append({"type": "assert", "pattern": ast.unparse(node)})
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr.startswith("assert"):
                    assertions.append({"type": "pytest", "pattern": ast.unparse(node)})

        return assertions

    def _analyze_naming_patterns(self, test_names: List[str]) -> Dict[str, str]:
        """Analyze test naming patterns to detect conventions"""
        conventions = {}

        # Analyze test function prefixes
        prefixes = Counter(name[: name.index("_")] for name in test_names if "_" in name)
        if prefixes:
            conventions["test_prefix"] = prefixes.most_common(1)[0][0]

        # Analyze test class patterns
        class_patterns = [name for name in test_names if name.startswith("Test") or name.endswith("Test")]
        if class_patterns:
            if any(name.startswith("Test") for name in class_patterns):
                conventions["class_prefix"] = "Test"
            if any(name.endswith("Test") for name in class_patterns):
                conventions["class_suffix"] = "Test"

        return conventions

    def _extract_imports_from_file(self, file_path: Path) -> Set[str]:
        """Extract imports from a test file"""
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        imports = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    imports.add(f"{module}.{name.name}")

        return imports

    def _scan_for_unittest_patterns(self) -> bool:
        """Check if the repository uses unittest patterns"""
        for test_file in self._find_test_files():
            with open(test_file, "r") as f:
                content = f.read()
                if "unittest.TestCase" in content or "from unittest import TestCase" in content:
                    return True
        return False

    def _detect_test_directory_pattern(self) -> str:
        """Detect the main test directory pattern"""
        test_dirs = Counter()

        for test_file in self._find_test_files():
            parts = test_file.parts
            for part in parts:
                if part.lower() in ["test", "tests"]:
                    test_dirs[part] += 1

        return test_dirs.most_common(1)[0][0] if test_dirs else "tests"

    def _detect_test_file_pattern(self) -> str:
        """Detect the most common test file naming pattern"""
        patterns = Counter()

        for test_file in self._find_test_files():
            if test_file.name.startswith("test_"):
                patterns["test_*.py"] += 1
            elif test_file.name.endswith("_test.py"):
                patterns["*_test.py"] += 1

        return patterns.most_common(1)[0][0] if patterns else "test_*.py"
