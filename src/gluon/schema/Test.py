from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TestStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    FLAKY = "flaky"


class TestAssertion(BaseModel):
    line_number: int
    assertion_type: str
    expected_value: Any
    actual_value: Any
    message: Optional[str]
    stack_trace: Optional[str]


class TestParameter(BaseModel):
    name: str
    type: str
    default_value: Optional[Any]


class TestFunction(BaseModel):
    name: str
    source_code: str
    line_number: int
    end_line_number: int
    assertions: List[TestAssertion]
    parameters: List[TestParameter]
    docstring: Optional[str]
    dependencies: List[str] = Field(default_factory=list)
    execution_time: Optional[float]
    status: TestStatus
    error_message: Optional[str]
    fixtures: List[str] = Field(default_factory=list)
    mocks: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    retry_count: int = 0
    timeout: Optional[float]
    async_test: bool = False
    parameterized: bool = False
    parameterized_values: Optional[List[Any]]


class TestClass(BaseModel):
    name: str
    methods: List[TestFunction]
    line_number: int
    end_line_number: int
    docstring: Optional[str]
    base_classes: List[str] = Field(default_factory=list)
    class_fixtures: List[str] = Field(default_factory=list)
    class_variables: Dict[str, Any] = Field(default_factory=dict)
    inner_classes: List["TestClass"] = Field(default_factory=list)


class CodeMetrics(BaseModel):
    lines_of_code: int
    cyclomatic_complexity: Optional[float]
    maintainability_index: Optional[float]
    cognitive_complexity: Optional[float]
    halstead_metrics: Optional[Dict[str, float]]


class TestFile(BaseModel):
    file_path: str
    imports: List[str]
    test_functions: List[TestFunction]
    test_classes: List[TestClass]
    coverage: Optional[float]
    code_metrics: CodeMetrics
    last_modified: datetime
    author: str
    git_blame: Dict[str, List[str]]  # Map of line numbers to commit hashes
    dependencies: List[str]
    encoding: str
    shebang: Optional[str]
    module_docstring: Optional[str]


class EnvironmentInfo(BaseModel):
    os: str
    python_version: str
    cpu_info: str
    memory_info: str
    environment_variables: Dict[str, str]


class TestSuite(BaseModel):
    repo_url: str
    branch: str
    commit_hash: str
    files: List[TestFile]
    total_coverage: float
    total_execution_time: float
    static_analysis: Dict[str, Any] = Field(default_factory=dict)
    environment: EnvironmentInfo
    dependencies: Dict[str, str] = Field(default_factory=dict)
    ci_cd_status: Optional[str]
    test_framework: str
    test_runner_version: str
    parallel_execution: bool
    random_seed: Optional[int]
    test_discovery_pattern: str
    ignored_paths: List[str]
    custom_markers: Dict[str, str]
    plugins: List[str]
    start_time: datetime
    end_time: datetime
    test_count: Dict[str, int]  # e.g., {"total": 100, "passed": 90, "failed": 5, "skipped": 5}
    flaky_tests: List[str]
    slow_tests: List[str]
    code_style_violations: Dict[str, List[str]]
