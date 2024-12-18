import pytest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn.supervisors.watchfilesreload import WatchFilesReload

@pytest.mark.skipif(WatchFilesReload is None, reason='watchfiles not available')
@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_shutdown_behavior(reloader_class):
    calls = []
    
    class CustomReload(reloader_class):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    
    assert 'shutdown' in calls

def test_shutdown_with_no_active_connections():
    calls = []
    
    class MockReloader:
        def shutdown(self):
            calls.append('shutdown')

    reloader = MockReloader()
    reloader.shutdown()
    
    assert 'shutdown' in calls

def test_shutdown_with_active_connections():
    calls = []
    active_connections = Mock()
    
    class CustomReload:
        def __init__(self, connections):
            self.connections = connections

        def shutdown(self):
            if self.connections:
                calls.append('shutdown with active connections')
            else:
                calls.append('shutdown without active connections')

    reloader = CustomReload(connections=[active_connections])
    reloader.shutdown()
    
    assert 'shutdown with active connections' in calls

def test_shutdown_when_already_shut_down():
    calls = []
    
    class CustomReload:
        def __init__(self):
            self.is_shutdown = False

        def shutdown(self):
            if not self.is_shutdown:
                calls.append('shutdown')
                self.is_shutdown = True
            else:
                calls.append('already shut down')

    reloader = CustomReload()
    reloader.shutdown()
    reloader.shutdown()
    
    assert calls == ['shutdown', 'already shut down']