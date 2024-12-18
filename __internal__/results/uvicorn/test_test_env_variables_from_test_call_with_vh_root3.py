import os
import pytest
from click.testing import CliRunner
from unittest import mock
from uvicorn.main import main as cli
from uvicorn import load_env_var

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

def test_env_var_persistence():
    key = "TEST_KEY"
    value = "TEST_VALUE"
    with load_env_var(key, value):
        assert os.environ[key] == value
    assert key not in os.environ

def test_multiple_env_var_load():
    with load_env_var("VAR1", "value1"), load_env_var("VAR2", "value2"):
        assert os.environ["VAR1"] == "value1"
        assert os.environ["VAR2"] == "value2"
    assert "VAR1" not in os.environ
    assert "VAR2" not in os.environ