import os
import pytest

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

def test_reset_environment_variable():
    os.environ['SANIC_MOTD_OUTPUT'] = 'test_value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_not_set():
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_multiple_resets():
    os.environ['SANIC_MOTD_OUTPUT'] = 'test_value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ
    reset()  # Call reset again to ensure no error occurs
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_with_other_env_variables():
    os.environ['SANIC_MOTD_OUTPUT'] = 'test_value'
    os.environ['OTHER_VAR'] = 'other_value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ
    assert os.environ['OTHER_VAR'] == 'other_value'  # Ensure other variables are unaffected