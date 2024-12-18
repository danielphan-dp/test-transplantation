import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_shutdown_method_calls_shutdown():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    
    assert 'shutdown' in calls

def test_shutdown_with_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    
    assert calls == ['shutdown']

def test_shutdown_with_existing_connections():
    calls = []
    connections = []

    class MockConnection:
        def shutdown(self):
            calls.append('connection_shutdown')

    connections.append(MockConnection())

    class CustomReload(BaseReload):
        def __init__(self, *args, connections=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.server_state.connections = connections

        def shutdown(self):
            for connection in self.server_state.connections:
                connection.shutdown()
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    
    assert 'connection_shutdown' in calls
    assert 'shutdown' in calls

def test_shutdown_no_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    
    assert calls == ['shutdown']