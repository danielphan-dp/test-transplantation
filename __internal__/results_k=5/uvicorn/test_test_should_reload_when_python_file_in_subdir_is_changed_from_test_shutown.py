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
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()

    assert 'shutdown' in calls

def test_shutdown_with_no_active_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()

    assert calls == ['shutdown']

def test_shutdown_closes_sockets_on_shutdown():
    sock = Mock()
    sock.fileno.return_value = 1
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            sock.fileno.return_value = -1

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[sock])

    reloader.shutdown()

    assert sock.fileno() == -1
    assert 'shutdown' in calls

def test_shutdown_when_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()

    assert calls == ['shutdown']