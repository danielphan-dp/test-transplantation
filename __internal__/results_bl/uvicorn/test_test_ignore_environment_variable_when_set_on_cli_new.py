import os
import contextlib
import pytest
from unittest import mock
from click.testing import CliRunner
from uvicorn import main

def test_load_env_var_sets_environment_variable():
    with load_env_var("TEST_VAR", "test_value"):
        assert os.environ["TEST_VAR"] == "test_value"

def test_load_env_var_clears_environment_variable():
    with load_env_var("TEST_VAR", "test_value"):
        pass
    assert "TEST_VAR" not in os.environ

def test_load_env_var_restores_old_environment():
    os.environ["OLD_VAR"] = "old_value"
    with load_env_var("NEW_VAR", "new_value"):
        assert os.environ["NEW_VAR"] == "new_value"
    assert os.environ["OLD_VAR"] == "old_value"

def test_load_env_var_multiple_contexts():
    with load_env_var("VAR1", "value1"):
        with load_env_var("VAR2", "value2"):
            assert os.environ["VAR1"] == "value1"
            assert os.environ["VAR2"] == "value2"
    assert "VAR1" not in os.environ
    assert "VAR2" not in os.environ

def test_load_env_var_with_existing_key():
    os.environ["EXISTING_VAR"] = "existing_value"
    with load_env_var("EXISTING_VAR", "new_value"):
        assert os.environ["EXISTING_VAR"] == "new_value"
    assert os.environ["EXISTING_VAR"] == "existing_value"