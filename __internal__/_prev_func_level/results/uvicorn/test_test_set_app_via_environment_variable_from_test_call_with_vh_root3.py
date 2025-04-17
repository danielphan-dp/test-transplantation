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

def test_load_env_var_restores_old_value():
    os.environ["TEST_KEY"] = "OLD_VALUE"
    with load_env_var("TEST_KEY", "NEW_VALUE"):
        assert os.environ["TEST_KEY"] == "NEW_VALUE"
    assert os.environ["TEST_KEY"] == "OLD_VALUE"

def test_load_env_var_clears_environment():
    os.environ["TEST_KEY"] = "VALUE"
    with load_env_var("TEST_KEY", "NEW_VALUE"):
        assert "TEST_KEY" in os.environ
    assert "TEST_KEY" not in os.environ

def test_set_app_via_environment_variable_with_invalid_app():
    invalid_app_path = "invalid.path:App"
    runner = CliRunner(env=os.environ)
    with load_env_var("UVICORN_APP", invalid_app_path):
        with mock.patch.object(main, "run") as mock_run:
            result = runner.invoke(cli)
            assert result.exit_code != 0
            mock_run.assert_not_called()

def test_set_app_via_environment_variable_with_empty_app():
    empty_app_path = ""
    runner = CliRunner(env=os.environ)
    with load_env_var("UVICORN_APP", empty_app_path):
        with mock.patch.object(main, "run") as mock_run:
            result = runner.invoke(cli)
            assert result.exit_code != 0
            mock_run.assert_not_called()