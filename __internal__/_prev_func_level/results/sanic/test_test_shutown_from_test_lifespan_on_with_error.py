import asyncio
import pytest
from sanic import Sanic
from unittest.mock import Mock, patch

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@patch('sanic.worker.process.os')
def test_shutdown_on_server_start(os_mock, app):
    @app.after_server_start
    def shutdown(*_):
        app.stop()

    process = Mock()
    process.pid = 1234
    process.is_alive.return_value = True
    context = Mock()
    context.Process.return_value = process

    loop = asyncio.new_event_loop()
    loop.run_until_complete(app.startup())
    loop.run_until_complete(app.shutdown())
    
    os_mock.kill.assert_called_once_with(1234, signal.SIGINT)

@patch('sanic.worker.process.os')
def test_shutdown_when_process_not_alive(os_mock, app):
    @app.after_server_start
    def shutdown(*_):
        app.stop()

    process = Mock()
    process.pid = 1234
    process.is_alive.return_value = False
    context = Mock()
    context.Process.return_value = process

    loop = asyncio.new_event_loop()
    loop.run_until_complete(app.startup())
    loop.run_until_complete(app.shutdown())
    
    os_mock.kill.assert_not_called()