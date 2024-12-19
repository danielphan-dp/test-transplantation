import os
import pytest
from sanic.exceptions import SanicException

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

def test_reset_environment_variable():
    os.environ['SANIC_MOTD_OUTPUT'] = 'Test Output'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_environment_variable_not_set():
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_custom_exception_with_reset(exception_app):
    class TeaError(SanicException):
        message = "Tempest in a teapot"
        status_code = 418

    exception_app.router.reset()

    @exception_app.get("/tempest")
    def tempest(_):
        raise TeaError

    _, response = exception_app.test_client.get("/tempest", debug=True)
    assert response.status == 418
    assert b"Tempest in a teapot" in response.body

def test_custom_exception_with_reset_no_env(exception_app):
    class CoffeeError(SanicException):
        message = "A storm in a coffee cup"
        status_code = 500

    exception_app.router.reset()

    @exception_app.get("/coffee")
    def coffee(_):
        raise CoffeeError

    _, response = exception_app.test_client.get("/coffee", debug=True)
    assert response.status == 500
    assert b"A storm in a coffee cup" in response.body