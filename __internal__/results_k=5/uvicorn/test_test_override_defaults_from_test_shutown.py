import pytest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_shutdown_method():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    assert 'shutdown' in calls

def test_shutdown_with_no_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    assert calls == ['shutdown']

def test_shutdown_with_active_connections():
    calls = []
    mock_connection = Mock()

    class CustomReload(BaseReload):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.server_state.connections = [mock_connection]

        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    mock_connection.shutdown.assert_called_once()
    assert 'shutdown' in calls

def test_shutdown_multiple_times():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    reloader.shutdown()
    assert calls.count('shutdown') == 2