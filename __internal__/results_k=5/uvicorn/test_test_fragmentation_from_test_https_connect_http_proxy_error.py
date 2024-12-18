import socket
import threading
import time
import pytest
from uvicorn.config import Config
from uvicorn.server import Server

def test_shutdown(unused_tcp_port: int):
    calls: list[str] = []

    class CustomServer(Server):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    app = lambda scope, receive, send: None  # Dummy ASGI app

    config = Config(app=app, port=unused_tcp_port)
    server = CustomServer(config=config)
    t = threading.Thread(target=server.run)
    t.daemon = True
    t.start()
    time.sleep(1)  # wait for server to start

    server.should_exit = True
    t.join()

    assert 'shutdown' in calls

def test_shutdown_no_connections(unused_tcp_port: int):
    calls: list[str] = []

    class CustomServer(Server):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    app = lambda scope, receive, send: None  # Dummy ASGI app

    config = Config(app=app, port=unused_tcp_port)
    server = CustomServer(config=config)
    t = threading.Thread(target=server.run)
    t.daemon = True
    t.start()
    time.sleep(1)  # wait for server to start

    server.should_exit = True
    t.join()

    assert 'shutdown' in calls

def test_shutdown_with_active_connections(unused_tcp_port: int):
    calls: list[str] = []

    class CustomServer(Server):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    app = lambda scope, receive, send: None  # Dummy ASGI app

    config = Config(app=app, port=unused_tcp_port)
    server = CustomServer(config=config)
    t = threading.Thread(target=server.run)
    t.daemon = True
    t.start()
    time.sleep(1)  # wait for server to start

    # Simulate an active connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", unused_tcp_port))

    server.should_exit = True
    t.join()

    assert 'shutdown' in calls
    sock.close()