import pytest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

@pytest.mark.parametrize('reloader_class', [BaseReload])
def test_shutdown_calls_shutdown_method(reloader_class):
    calls = []

    class CustomReload(reloader_class):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    assert 'shutdown' in calls

def test_shutdown_with_no_active_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    assert calls == ['shutdown']

def test_shutdown_with_mocked_process(os_mock: Mock):
    process = Mock()
    process.pid = 1234
    process.is_alive.return_value = True
    context = Mock()
    context.Process.return_value = process
    reloader = BaseReload(Config(app="tests.test_config:asgi_app", reload=True), target=None, sockets=[], context=context)

    reloader.shutdown()
    os_mock.kill.assert_called_once_with(1234, signal.SIGINT)