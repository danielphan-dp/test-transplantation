import os
import pytest

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.mark.parametrize('protocol', [3, 4])
def test_reset_environment_variable(app, protocol, port):
    os.environ['SANIC_MOTD_OUTPUT'] = 'Test Output'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

@pytest.mark.parametrize('protocol', [3, 4])
def test_reset_environment_variable_not_set(app, protocol, port):
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

@pytest.mark.parametrize('protocol', [3, 4])
def test_reset_multiple_calls(app, protocol, port):
    os.environ['SANIC_MOTD_OUTPUT'] = 'Test Output'
    reset()
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

@pytest.mark.parametrize('protocol', [3, 4])
def test_reset_with_other_env_variables(app, protocol, port):
    os.environ['OTHER_VAR'] = 'Other Value'
    os.environ['SANIC_MOTD_OUTPUT'] = 'Test Output'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ
    assert os.environ['OTHER_VAR'] == 'Other Value'