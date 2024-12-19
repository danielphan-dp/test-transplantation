import asyncio
import pytest
from unittest.mock import Mock, patch
from sanic import Sanic

app = Sanic("TestApp")

@app.after_server_start
def shutdown(*_):
    app.stop()

@pytest.fixture
def os_mock():
    with patch('sanic.worker.process.os') as mock:
        yield mock

def test_shutdown_triggers_app_stop(os_mock):
    shutdown_called = False

    @app.listener('after_server_stop')
    def after_stop_listener(*args):
        nonlocal shutdown_called
        shutdown_called = True

    app.run()

    assert not shutdown_called
    shutdown()
    assert shutdown_called

def test_shutdown_no_active_process(os_mock):
    process = Mock()
    process.is_alive.return_value = False
    context = Mock()
    context.Process.return_value = process
    manager = WorkerManager(1, fake_serve, {}, context, (Mock(), Mock()), {})
    
    with pytest.raises(ServerKilled):
        manager.shutdown()
    
    os_mock.kill.assert_not_called()