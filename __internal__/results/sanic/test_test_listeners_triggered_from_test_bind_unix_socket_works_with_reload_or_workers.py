import socket
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.server import get_port

def test_get_port():
    app = Sanic("test_app")

    # Test that get_port returns a valid port number
    port = get_port()
    assert isinstance(port, int)
    assert 0 < port < 65536  # Valid port range

    # Test that get_port can be called multiple times and returns different ports
    port1 = get_port()
    port2 = get_port()
    assert port1 != port2

    # Test that the socket can be created and bound to the port
    sock = socket.socket()
    sock.bind(('', port))
    assert sock.getsockname()[1] == port
    sock.close()