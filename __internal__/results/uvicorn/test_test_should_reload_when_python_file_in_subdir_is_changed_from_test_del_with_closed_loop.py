import pytest
from unittest import mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_shutdown_method_calls_shutdown():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()

    assert 'shutdown' in calls

def test_shutdown_with_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()

    assert calls == ['shutdown']

def test_shutdown_with_mocked_connections():
    calls = []
    mock_connection = mock.Mock()

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            self.server_state.connections = [mock_connection]
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()

    mock_connection.shutdown.assert_called_once()
    assert calls == ['shutdown']