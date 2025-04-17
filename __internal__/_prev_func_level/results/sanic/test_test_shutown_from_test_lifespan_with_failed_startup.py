import pytest
from unittest.mock import Mock, patch
from sanic import Sanic

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@patch('sanic.worker.process.os')
def test_shutdown(os_mock, app):
    app.after_server_start(shutdown)
    app.stop()
    os_mock.kill.assert_called_once()

@patch('sanic.worker.process.os')
def test_shutdown_when_not_alive(os_mock, app):
    process = Mock()
    process.is_alive.return_value = False
    os_mock.kill.side_effect = Exception("Process not alive")
    
    with pytest.raises(Exception, match="Process not alive"):
        app.after_server_start(shutdown)
        app.stop()

@patch('sanic.worker.process.os')
def test_shutdown_multiple_calls(os_mock, app):
    app.after_server_start(shutdown)
    app.stop()
    app.stop()
    assert os_mock.kill.call_count == 1

@patch('sanic.worker.process.os')
def test_shutdown_with_custom_signal(os_mock, app):
    custom_signal = 15  # Custom signal for testing
    app.after_server_start(shutdown)
    app.stop()
    os_mock.kill.assert_called_once_with(app.pid, custom_signal)