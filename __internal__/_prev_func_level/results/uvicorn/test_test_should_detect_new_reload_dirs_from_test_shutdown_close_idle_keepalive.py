import pytest
import socket
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_shutdown_method_calls_shutdown():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    
    assert "shutdown" in calls

def test_shutdown_closes_sockets_on_shutdown():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = BaseReload(config, target=None, sockets=[sock])
    
    assert sock.fileno() != -1
    reloader.shutdown()
    assert sock.fileno() == -1

def test_shutdown_multiple_calls():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    reloader.shutdown()

    assert calls.count("shutdown") == 2

def test_shutdown_with_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=None)

    reloader.shutdown()

    assert "shutdown" in calls