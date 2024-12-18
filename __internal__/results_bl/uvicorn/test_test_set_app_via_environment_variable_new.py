import os
import contextlib
import pytest
from unittest import mock
from click.testing import CliRunner
from uvicorn.main import run as main
from your_module import cli  # Adjust the import based on your project structure

def test_load_env_var_sets_environment_variable():
    key = "TEST_KEY"
    value = "TEST_VALUE"
    with load_env_var(key, value):
        assert os.environ[key] == value

def test_load_env_var_restores_environment_variable():
    key = "RESTORE_KEY"
    original_value = "ORIGINAL_VALUE"
    os.environ[key] = original_value
    new_value = "NEW_VALUE"
    with load_env_var(key, new_value):
        assert os.environ[key] == new_value
    assert os.environ[key] == original_value

def test_load_env_var_clears_environment_variable():
    key = "CLEAR_KEY"
    with load_env_var(key, "SOME_VALUE"):
        assert key in os.environ
    assert key not in os.environ

def test_load_env_var_multiple_contexts():
    key1 = "MULTI_KEY1"
    value1 = "VALUE1"
    key2 = "MULTI_KEY2"
    value2 = "VALUE2"
    with load_env_var(key1, value1), load_env_var(key2, value2):
        assert os.environ[key1] == value1
        assert os.environ[key2] == value2

def test_load_env_var_empty_key_value():
    with pytest.raises(KeyError):
        with load_env_var("", "VALUE"):
            pass
    with pytest.raises(KeyError):
        with load_env_var("KEY", ""):
            pass

def test_load_env_var_invalid_key():
    invalid_key = "INVALID_KEY"
    with load_env_var(invalid_key, "VALUE"):
        runner = CliRunner(env=os.environ)
        with mock.patch.object(main, "run") as mock_run:
            result = runner.invoke(cli)
            args, _ = mock_run.call_args
            assert result.exit_code == 0
            assert args == (invalid_key,)