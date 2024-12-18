import contextlib
import os
from collections.abc import Iterator
from unittest import mock
import pytest
from click.testing import CliRunner
import uvicorn
from uvicorn.main import main as cli

@contextlib.contextmanager
def load_env_var(key: str, value: str) -> Iterator[None]:
    old_environ = dict(os.environ)
    os.environ[key] = value
    yield
    os.environ.clear()
    os.environ.update(old_environ)

def test_load_env_var_resets_environment():
    with load_env_var("TEST_VAR", "test_value"):
        assert os.environ["TEST_VAR"] == "test_value"
    assert "TEST_VAR" not in os.environ

def test_load_env_var_multiple_calls():
    with load_env_var("TEST_VAR", "value1"):
        assert os.environ["TEST_VAR"] == "value1"
        with load_env_var("TEST_VAR", "value2"):
            assert os.environ["TEST_VAR"] == "value2"
        assert os.environ["TEST_VAR"] == "value1"
    assert "TEST_VAR" not in os.environ

def test_ignore_environment_variable_when_set_on_cli():
    with load_env_var("UVICORN_HTTP", "h11"):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(uvicorn.main, "run") as mock_run:
            runner.invoke(cli, ["tests.test_cli:App", "--http=httptools"])
            _, kwargs = mock_run.call_args
            assert kwargs["http"] == "httptools"

def test_load_env_var_with_existing_key():
    os.environ["EXISTING_VAR"] = "original_value"
    with load_env_var("EXISTING_VAR", "new_value"):
        assert os.environ["EXISTING_VAR"] == "new_value"
    assert os.environ["EXISTING_VAR"] == "original_value"