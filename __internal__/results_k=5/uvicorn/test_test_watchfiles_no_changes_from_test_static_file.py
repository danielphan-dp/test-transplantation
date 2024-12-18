import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

calls = []

class CustomReload(BaseReload):
    def shutdown(self):
        calls.append('shutdown')

def test_reloader_shutdown():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])
    
    assert calls == []
    reloader.shutdown()
    assert calls == ['shutdown']

def test_reloader_shutdown_multiple_calls():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    reloader.shutdown()
    assert calls == ['shutdown', 'shutdown']

def test_reloader_shutdown_with_sockets():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[sock])

    assert sock.fileno() != -1
    reloader.shutdown()
    assert sock.fileno() == -1

def test_reloader_shutdown_no_sockets():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=None)

    reloader.shutdown()
    assert calls == ['shutdown']