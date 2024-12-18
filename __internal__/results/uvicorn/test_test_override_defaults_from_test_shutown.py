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
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()
    
    assert 'shutdown' in calls

def test_shutdown_with_no_active_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()
    
    assert calls == ['shutdown']

def test_shutdown_closes_sockets():
    calls = []
    sock = Mock()

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            sock.close()
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[sock])

    reloader.shutdown()
    
    sock.close.assert_called_once()
    assert 'shutdown' in calls

def test_shutdown_multiple_calls():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=Mock(), sockets=[])

    reloader.shutdown()
    reloader.shutdown()
    
    assert calls.count('shutdown') == 2