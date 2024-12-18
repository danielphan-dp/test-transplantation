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

def test_load_env_var_sets_value():
    with load_env_var("TEST_KEY", "TEST_VALUE"):
        assert os.environ["TEST_KEY"] == "TEST_VALUE"

def test_load_env_var_cleans_up():
    with load_env_var("TEST_KEY", "TEST_VALUE"):
        pass
    assert "TEST_KEY" not in os.environ

def test_load_env_var_multiple_keys():
    with load_env_var("KEY1", "VALUE1"), load_env_var("KEY2", "VALUE2"):
        assert os.environ["KEY1"] == "VALUE1"
        assert os.environ["KEY2"] == "VALUE2"

def test_set_app_via_environment_variable_with_invalid_app():
    invalid_app_path = "invalid.path:App"
    runner = CliRunner(env=os.environ)
    with load_env_var("UVICORN_APP", invalid_app_path):
        result = runner.invoke(cli)
        assert result.exit_code != 0

def test_set_app_via_environment_variable_with_empty_app():
    empty_app_path = ""
    runner = CliRunner(env=os.environ)
    with load_env_var("UVICORN_APP", empty_app_path):
        result = runner.invoke(cli)
        assert result.exit_code != 0

def test_set_app_via_environment_variable_with_special_characters():
    app_path = "tests.test_cli:App@123"
    runner = CliRunner(env=os.environ)
    with load_env_var("UVICORN_APP", app_path):
        with mock.patch.object(main, "run") as mock_run:
            result = runner.invoke(cli)
            args, _ = mock_run.call_args
            assert result.exit_code == 0
            assert args == (app_path,)