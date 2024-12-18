import os
import contextlib
import pytest
from click.testing import CliRunner
from unittest import mock
from uvicorn.main import main as cli

@contextlib.contextmanager
def load_env_var(key: str, value: str) -> Iterator[None]:
    old_environ = dict(os.environ)
    os.environ[key] = value
    yield
    os.environ.clear()
    os.environ.update(old_environ)

def test_load_env_var_sets_variable():
    with load_env_var("TEST_VAR", "test_value"):
        assert os.environ["TEST_VAR"] == "test_value"

def test_load_env_var_clears_variable():
    with load_env_var("TEST_VAR", "test_value"):
        pass
    assert "TEST_VAR" not in os.environ

def test_load_env_var_restores_previous_value():
    os.environ["TEST_VAR"] = "original_value"
    with load_env_var("TEST_VAR", "test_value"):
        assert os.environ["TEST_VAR"] == "test_value"
    assert os.environ["TEST_VAR"] == "original_value"

def test_ignore_environment_variable_when_set_on_cli():
    with load_env_var("UVICORN_HTTP", "h11"):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(main, "run") as mock_run:
            runner.invoke(cli, ["tests.test_cli:App", "--http=httptools"])
            _, kwargs = mock_run.call_args
            assert kwargs["http"] == "httptools"

def test_load_env_var_multiple_contexts():
    with load_env_var("VAR1", "value1"):
        with load_env_var("VAR2", "value2"):
            assert os.environ["VAR1"] == "value1"
            assert os.environ["VAR2"] == "value2"
    assert "VAR1" not in os.environ
    assert "VAR2" not in os.environ