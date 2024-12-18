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
    os.environ['SANIC_MOTD_OUTPUT'] = 'test_value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_no_key(app):
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_with_key(app):
    os.environ['SANIC_MOTD_OUTPUT'] = 'another_value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_multiple_calls(app):
    os.environ['SANIC_MOTD_OUTPUT'] = 'value1'
    reset()
    os.environ['SANIC_MOTD_OUTPUT'] = 'value2'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_no_effect_on_other_vars(app):
    os.environ['OTHER_VAR'] = 'value'
    reset()
    assert os.environ['OTHER_VAR'] == 'value'