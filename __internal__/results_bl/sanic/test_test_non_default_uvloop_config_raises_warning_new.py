import socket
import pytest
from sanic import Sanic
from conftest import get_port

def test_get_port_returns_valid_port():
    port = get_port()
    assert isinstance(port, int)
    assert 0 < port < 65536

def test_get_port_multiple_calls_return_different_ports():
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1

def test_get_port_socket_is_bound():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    assert port == get_port()
    sock.close()

def test_get_port_raises_exception_on_socket_error(monkeypatch):
    def mock_bind(*args, **kwargs):
        raise socket.error("Socket error")
    
    monkeypatch.setattr(socket.socket, 'bind', mock_bind)
    with pytest.raises(socket.error):
        get_port()