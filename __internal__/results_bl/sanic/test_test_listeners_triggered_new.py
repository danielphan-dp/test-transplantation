import socket
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.server import get_port

def test_get_port():
    # Test that get_port returns a valid port number
    port = get_port()
    assert isinstance(port, int)
    assert 0 < port < 65536

def test_get_port_multiple_calls():
    # Test that multiple calls to get_port return different port numbers
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1

def test_get_port_socket_bind():
    # Test that the socket can bind to the port returned by get_port
    port = get_port()
    sock = socket.socket()
    try:
        sock.bind(('', port))
    except OSError:
        pytest.fail("Socket could not bind to the port returned by get_port")
    finally:
        sock.close()