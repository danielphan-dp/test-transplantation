import os
import pytest

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.mark.parametrize('protocol', [3, 4])
def test_reset_environment_variable(app, protocol):
    os.environ['SANIC_MOTD_OUTPUT'] = 'Test Output'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_no_key(app):
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_with_key(app):
    os.environ['SANIC_MOTD_OUTPUT'] = 'Another Test Output'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_multiple_calls(app):
    os.environ['SANIC_MOTD_OUTPUT'] = 'First Output'
    reset()
    os.environ['SANIC_MOTD_OUTPUT'] = 'Second Output'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_no_effect_on_other_vars(app):
    os.environ['OTHER_VAR'] = 'Some Value'
    reset()
    assert os.environ['OTHER_VAR'] == 'Some Value'