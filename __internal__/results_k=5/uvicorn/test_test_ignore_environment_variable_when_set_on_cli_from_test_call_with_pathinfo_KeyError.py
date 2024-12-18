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

def test_load_env_var_sets_environment_variable():
    with load_env_var("TEST_ENV_VAR", "test_value"):
        assert os.environ["TEST_ENV_VAR"] == "test_value"

def test_load_env_var_restores_environment_variable():
    os.environ["TEST_ENV_VAR"] = "original_value"
    with load_env_var("TEST_ENV_VAR", "test_value"):
        pass
    assert os.environ["TEST_ENV_VAR"] == "original_value"

def test_ignore_environment_variable_when_set_on_cli():
    with load_env_var("UVICORN_HTTP", "h11"):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(main, "run") as mock_run:
            runner.invoke(cli, ["tests.test_cli:App", "--http=httptools"])
            _, kwargs = mock_run.call_args
            assert kwargs["http"] == "httptools"

def test_load_env_var_with_empty_key():
    with pytest.raises(KeyError):
        with load_env_var("", "value"):
            pass

def test_load_env_var_with_empty_value():
    with load_env_var("TEST_ENV_VAR", ""):
        assert os.environ["TEST_ENV_VAR"] == ""

def test_load_env_var_with_nonexistent_key():
    with load_env_var("NON_EXISTENT_KEY", "value"):
        assert os.environ["NON_EXISTENT_KEY"] == "value"
    assert "NON_EXISTENT_KEY" not in os.environ