import socket
import pytest
from sanic import Sanic
from conftest import get_port

@pytest.fixture
def app():
    return Sanic("TestApp")

def test_get_port_creates_socket(app):
    port = get_port()
    assert isinstance(port, int)
    assert 0 < port < 65536

def test_get_port_multiple_calls(app):
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1  # Ensure multiple calls return different ports

def test_get_port_socket_bound(app):
    port = get_port()
    sock = socket.socket()
    sock.bind(('', port))
    assert sock.getsockname()[1] == port
    sock.close()