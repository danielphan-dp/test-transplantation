import socket
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.server import get_port

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_port_creates_socket(app):
    port = get_port()
    assert isinstance(port, int)
    assert 0 < port < 65536

def test_get_port_multiple_calls(app):
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1  # Ensure different ports are returned

def test_get_port_socket_bound(app):
    port = get_port()
    sock = socket.socket()
    sock.bind(('', port))
    assert sock.getsockname()[1] == port
    sock.close()

def test_get_port_invalid_socket(app):
    with pytest.raises(OSError):
        sock = socket.socket()
        sock.bind(('', -1))  # Invalid port
        sock.close()