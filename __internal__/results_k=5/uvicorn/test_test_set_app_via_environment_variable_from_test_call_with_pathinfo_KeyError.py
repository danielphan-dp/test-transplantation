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

def test_load_env_var_sets_environment_variable():
    key = "TEST_ENV_VAR"
    value = "test_value"
    with load_env_var(key, value):
        assert os.environ[key] == value

def test_load_env_var_restores_environment_variable():
    key = "TEST_ENV_VAR"
    original_value = os.environ.get(key)
    value = "test_value"
    with load_env_var(key, value):
        pass
    assert os.environ.get(key) == original_value

def test_load_env_var_multiple_contexts():
    key1 = "TEST_ENV_VAR1"
    value1 = "test_value1"
    key2 = "TEST_ENV_VAR2"
    value2 = "test_value2"
    with load_env_var(key1, value1), load_env_var(key2, value2):
        assert os.environ[key1] == value1
        assert os.environ[key2] == value2

def test_set_app_via_environment_variable_with_invalid_app():
    app_path = "invalid.app.path"
    runner = CliRunner(env=os.environ)
    with mock.patch.object(uvicorn.main, "run") as mock_run:
        result = runner.invoke(cli)
        assert result.exit_code != 0
        mock_run.assert_not_called()