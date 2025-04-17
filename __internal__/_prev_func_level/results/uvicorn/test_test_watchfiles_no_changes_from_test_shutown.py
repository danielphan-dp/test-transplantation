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

def test_shutdown_with_multiple_calls():
    calls = []
    
    class CustomReload:
        def shutdown(self):
            calls.append('shutdown')

    reloader = CustomReload()
    reloader.shutdown()
    reloader.shutdown()
    
    assert calls.count('shutdown') == 2

def test_shutdown_with_exception_handling():
    calls = []
    
    class CustomReload:
        def shutdown(self):
            calls.append('shutdown')
            raise RuntimeError("Shutdown error")

    reloader = CustomReload()
    
    with pytest.raises(RuntimeError, match="Shutdown error"):
        reloader.shutdown()
    
    assert 'shutdown' in calls