import pytest
from unittest.mock import Mock
from sanic import Sanic
from sanic.exceptions import SanicException

def test_stop_without_terminate(app: Sanic):
    app.multiplexer = Mock()
    
    app.stop(unregister=False)
    
    app.multiplexer.terminate.assert_not_called()
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()

def test_stop_with_terminate(app: Sanic):
    app.multiplexer = Mock()
    
    app.stop(terminate=True)
    
    app.multiplexer.terminate.assert_called_once()
    assert len(Sanic._app_registry) == 0
    Sanic._app_registry.clear()

def test_stop_multiple_calls(app: Sanic):
    app.multiplexer = Mock()
    
    app.stop()
    app.stop()
    
    app.multiplexer.terminate.assert_called_once()
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()

def test_stop_with_exception(app: Sanic):
    app.multiplexer = Mock()
    app.multiplexer.terminate.side_effect = SanicException("Termination error")
    
    with pytest.raises(SanicException, match="Termination error"):
        app.stop(terminate=True)
    
    assert len(Sanic._app_registry) == 1
    Sanic._app_registry.clear()