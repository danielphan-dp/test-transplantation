import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

calls = []

class CustomReload(BaseReload):
    def shutdown(self):
        calls.append("shutdown")
        super().shutdown()

def test_reloader_shutdown():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])
    
    reloader.shutdown()
    
    assert "shutdown" in calls

def test_reloader_shutdown_multiple_calls():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    reloader.shutdown()

    assert calls.count("shutdown") == 2

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
    
    assert "shutdown" in calls

def test_reloader_shutdown_edge_case():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])
    
    # Simulate an edge case where shutdown is called without any prior startup
    reloader.shutdown()
    
    assert "shutdown" in calls
    assert len(calls) == 1  # Ensure it only records one shutdown call