import os
import contextlib
import pytest
from unittest import mock
from click.testing import CliRunner
from uvicorn import main

@pytest.mark.parametrize('http_protocol', ['h11', 'httptools'])
def test_env_variables(http_protocol: str):
    with load_env_var("UVICORN_HTTP", http_protocol):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(main, "run") as mock_run:
            runner.invoke(cli, ["tests.test_cli:App"])
            _, kwargs = mock_run.call_args
            assert kwargs["http"] == http_protocol

def test_load_env_var_clears_environment():
    key = "TEST_KEY"
    value = "TEST_VALUE"
    old_value = os.environ.get(key)
    
    with load_env_var(key, value):
        assert os.environ[key] == value

    assert os.environ.get(key) == old_value

def test_load_env_var_multiple_calls():
    key = "MULTI_TEST_KEY"
    value1 = "VALUE1"
    value2 = "VALUE2"
    
    with load_env_var(key, value1):
        assert os.environ[key] == value1
        
    with load_env_var(key, value2):
        assert os.environ[key] == value2

def test_load_env_var_empty_key():
    with pytest.raises(KeyError):
        with load_env_var("", "value"):
            pass

def test_load_env_var_empty_value():
    key = "EMPTY_VALUE_KEY"
    with load_env_var(key, ""):
        assert os.environ[key] == ""