import pytest
from unittest.mock import Mock
from sanic import Sanic

@pytest.fixture
def app():
    app = Sanic("test_app")
    app.multiplexer = Mock()
    return app

def test_stop_no_terminate(app):
    app.stop()
    app.multiplexer.terminate.assert_not_called()
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()

def test_stop_unregister_false(app):
    app.stop(unregister=False)
    app.multiplexer.terminate.assert_called_once()
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()

def test_stop_with_terminate(app):
    app.stop(terminate=True)
    app.multiplexer.terminate.assert_called_once()
    assert len(Sanic._app_registry) == 0
    Sanic._app_registry.clear()

def test_stop_multiple_calls(app):
    app.stop()
    app.stop()
    app.multiplexer.terminate.assert_not_called()
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()

def test_stop_with_invalid_argument(app):
    with pytest.raises(TypeError):
        app.stop(invalid_arg=True)