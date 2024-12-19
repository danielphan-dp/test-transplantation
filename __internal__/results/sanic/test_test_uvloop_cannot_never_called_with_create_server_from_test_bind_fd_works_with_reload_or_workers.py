import socket
import pytest
from sanic import Sanic
from sanic.helpers import get_port

@pytest.mark.asyncio
async def test_get_port_creates_socket():
    port = get_port()
    assert isinstance(port, int)
    assert 0 < port < 65536  # Valid port range

@pytest.mark.asyncio
async def test_get_port_multiple_calls():
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1  # Ensure different ports are returned

@pytest.mark.asyncio
async def test_get_port_socket_bind():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    assert port == get_port()  # Ensure get_port returns the bound port
    sock.close()