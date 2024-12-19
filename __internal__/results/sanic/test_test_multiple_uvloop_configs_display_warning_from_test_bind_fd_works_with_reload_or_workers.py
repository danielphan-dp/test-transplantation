import socket
import pytest
from sanic import Sanic
from sanic.helpers import get_port

@pytest.mark.asyncio
async def test_get_port_creates_socket():
    port = get_port()
    sock = socket.socket()
    sock.bind(('', port))
    assert sock.getsockname()[1] == port
    sock.close()

@pytest.mark.asyncio
async def test_get_port_returns_different_ports():
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1

@pytest.mark.asyncio
async def test_get_port_socket_is_open():
    port = get_port()
    sock = socket.socket()
    sock.bind(('', port))
    sock.listen(1)
    assert sock.getsockname()[1] == port
    sock.close()