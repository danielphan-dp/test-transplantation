import socket
import pytest

def test_get_port_creates_socket():
    port = get_port()
    sock = socket.socket()
    sock.bind(('', port))
    assert isinstance(sock, socket.socket)
    assert sock.getsockname()[1] == port
    sock.close()

def test_get_port_returns_different_ports():
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1  # Ensure that multiple calls return different ports

def test_get_port_socket_is_bound():
    port = get_port()
    sock = socket.socket()
    sock.bind(('', port))
    assert sock.getsockname()[1] == port
    sock.close()

def test_get_port_raises_exception_on_bind_failure():
    sock = socket.socket()
    sock.bind(('', 0))  # Bind to an available port first
    port = sock.getsockname()[1]
    sock.close()
    
    with pytest.raises(OSError):
        sock.bind(('', port))  # Attempt to bind to the same port again

def test_get_port_socket_family():
    port = get_port()
    sock = socket.socket()
    sock.bind(('', port))
    assert sock.family in (socket.AF_INET, socket.AF_INET6)
    sock.close()