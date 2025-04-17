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

def test_load_env_var_sets_value():
    key = "TEST_KEY"
    value = "TEST_VALUE"
    with load_env_var(key, value):
        assert os.environ[key] == value
    assert key not in os.environ

def test_load_env_var_restores_previous_value():
    key = "TEST_KEY"
    original_value = "ORIGINAL_VALUE"
    os.environ[key] = original_value
    new_value = "NEW_VALUE"
    with load_env_var(key, new_value):
        assert os.environ[key] == new_value
    assert os.environ[key] == original_value

def test_load_env_var_multiple_keys():
    key1 = "KEY1"
    value1 = "VALUE1"
    key2 = "KEY2"
    value2 = "VALUE2"
    with load_env_var(key1, value1), load_env_var(key2, value2):
        assert os.environ[key1] == value1
        assert os.environ[key2] == value2
    assert key1 not in os.environ
    assert key2 not in os.environ

def test_set_app_via_environment_variable():
    app_path = "tests.test_cli:App"
    with load_env_var("UVICORN_APP", app_path):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(uvicorn.main, "run") as mock_run:
            result = runner.invoke(cli)
            args, _ = mock_run.call_args
            assert result.exit_code == 0
            assert args == (app_path,)

def test_load_env_var_invalid_key():
    key = ""
    value = "VALUE"
    with pytest.raises(KeyError):
        with load_env_var(key, value):
            pass

def test_load_env_var_empty_value():
    key = "EMPTY_VALUE_KEY"
    value = ""
    with load_env_var(key, value):
        assert os.environ[key] == value
    assert key not in os.environ