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

@pytest.mark.parametrize('http_protocol', ['h11', 'httptools', 'invalid_protocol'])
def test_env_variables_with_invalid_protocol(http_protocol: str):
    with load_env_var("UVICORN_HTTP", http_protocol):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(main, "run") as mock_run:
            result = runner.invoke(cli, ["tests.test_cli:App"])
            if http_protocol in ['h11', 'httptools']:
                assert result.exit_code == 0
                _, kwargs = mock_run.call_args
                assert kwargs["http"] == http_protocol
            else:
                assert result.exit_code != 0
                assert "Invalid HTTP protocol" in result.output

def test_env_var_persistence():
    with load_env_var("TEST_VAR", "test_value"):
        assert os.environ["TEST_VAR"] == "test_value"
    assert "TEST_VAR" not in os.environ

def test_multiple_env_vars():
    with load_env_var("VAR1", "value1"), load_env_var("VAR2", "value2"):
        assert os.environ["VAR1"] == "value1"
        assert os.environ["VAR2"] == "value2"
    assert "VAR1" not in os.environ
    assert "VAR2" not in os.environ