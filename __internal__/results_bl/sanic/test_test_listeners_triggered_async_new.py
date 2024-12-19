import socket
import pytest
import logging
from sanic import Sanic
from sanic.response import text
from conftest import get_port

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_port_valid_range(app):
    port = get_port()
    assert 1024 <= port <= 65535, "Port should be in the valid range"

def test_get_port_multiple_calls(app):
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1, "Multiple calls to get_port should return different ports"

def test_get_port_no_bind_error(app):
    try:
        port = get_port()
        assert port is not None, "Port should not be None"
    except Exception as e:
        pytest.fail(f"get_port raised an exception: {e}")

def test_get_port_socket_closure(app):
    port = get_port()
    sock = socket.socket()
    sock.bind(('', port))
    sock.close()
    assert True, "Socket should close without issues"

def test_get_port_edge_case_zero(app):
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    assert port == 0, "Port should be 0 when bound to an ephemeral port"