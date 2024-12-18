import os
import pytest
from click.testing import CliRunner
from unittest import mock
from uvicorn.main import main as cli
from uvicorn import load_env_var

@pytest.mark.parametrize('http_protocol', ['h11', 'httptools'])
def test_env_variables(http_protocol: str):
    with load_env_var("UVICORN_HTTP", http_protocol):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(main, "run") as mock_run:
            result = runner.invoke(cli, ["tests.test_cli:App"])
            assert result.exit_code == 0
            _, kwargs = mock_run.call_args
            assert kwargs["http"] == http_protocol

def test_load_env_var_clears_environment():
    key = "TEST_KEY"
    value = "TEST_VALUE"
    assert key not in os.environ
    with load_env_var(key, value):
        assert os.environ[key] == value
    assert key not in os.environ

def test_load_env_var_preserves_existing_environment():
    key = "EXISTING_KEY"
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

def test_load_env_var_empty_key_value():
    key = ""
    value = ""
    with load_env_var(key, value):
        assert os.environ[key] == value
    assert key not in os.environ

def test_load_env_var_invalid_key():
    key = None
    value = "VALUE"
    with pytest.raises(TypeError):
        with load_env_var(key, value):
            pass