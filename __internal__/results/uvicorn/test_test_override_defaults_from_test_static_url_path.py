import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_reloader_shutdown():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=lambda: None, sockets=[])

    reloader.shutdown()
    
    assert "shutdown" in calls

def test_reloader_shutdown_with_sockets():
    calls = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=lambda: None, sockets=[sock])
    
    assert sock.fileno() != -1
    reloader.shutdown()
    assert sock.fileno() == -1
    assert "shutdown" in calls

def test_reloader_shutdown_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=lambda: None, sockets=None)

    reloader.shutdown()
    
    assert "shutdown" in calls

def test_reloader_shutdown_multiple_calls():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=lambda: None, sockets=[])

    reloader.shutdown()
    reloader.shutdown()
    
    assert calls.count("shutdown") == 2