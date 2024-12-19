import pytest
from unittest.mock import Mock
from sanic import Sanic
from sanic.app import stop

@pytest.fixture
def app():
    app_instance = Sanic("TestApp")
    app_instance.multiplexer = Mock()
    return app_instance

def test_stop_without_terminate(app):
    app.stop()
    app.multiplexer.terminate.assert_not_called()
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()

def test_stop_with_terminate(app):
    app.stop(terminate=True)
    app.multiplexer.terminate.assert_called_once()
    app.multiplexer.reset_mock()
    assert len(Sanic._app_registry) == 0
    Sanic._app_registry.clear()

def test_stop_unregister_false(app):
    app.stop(unregister=False)
    app.multiplexer.terminate.assert_called_once()
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()

def test_stop_multiple_calls(app):
    app.stop()
    app.stop()
    app.multiplexer.terminate.assert_not_called()
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()

def test_stop_with_edge_case(app):
    app.multiplexer.terminate.side_effect = Exception("Terminate failed")
    with pytest.raises(Exception, match="Terminate failed"):
        app.stop(terminate=True)
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()