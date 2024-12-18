import os
import contextlib
import pytest
from click.testing import CliRunner
from unittest import mock
from uvicorn.main import main as cli

@pytest.mark.parametrize('http_protocol', ['h11', 'httptools', 'invalid_protocol'])
def test_env_variables_with_invalid_protocol(http_protocol):
    with load_env_var("UVICORN_HTTP", http_protocol):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(main, "run") as mock_run:
            result = runner.invoke(cli, ["tests.test_cli:App"])
            if http_protocol == 'invalid_protocol':
                assert result.exit_code != 0
            else:
                assert result.exit_code == 0
                _, kwargs = mock_run.call_args
                assert kwargs["http"] == http_protocol

def test_env_variable_cleanup():
    key = "TEST_ENV_VAR"
    value = "test_value"
    with load_env_var(key, value):
        assert os.environ[key] == value
    assert key not in os.environ

def test_multiple_env_variables():
    with load_env_var("UVICORN_HTTP", "h11"), load_env_var("UVICORN_PORT", "8000"):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(main, "run") as mock_run:
            runner.invoke(cli, ["tests.test_cli:App"])
            _, kwargs = mock_run.call_args
            assert kwargs["http"] == "h11"
            assert kwargs["port"] == 8000