import pytest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

@pytest.mark.parametrize('reloader_class', [BaseReload])
def test_shutdown_method_calls_shutdown(reloader_class):
    calls = []

    class CustomReload(reloader_class):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()
    
    assert 'shutdown' in calls

def test_shutdown_with_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()

    assert calls == ['shutdown']

def test_shutdown_with_active_connections():
    calls = []
    mock_connection = Mock()

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            self.server_state.connections.add(mock_connection)

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()

    assert calls == ['shutdown']
    mock_connection.shutdown.assert_called_once()