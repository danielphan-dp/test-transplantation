import asyncio
import logging
from collections import Counter
from unittest.mock import Mock
import pytest
from sanic import Sanic
from conftest import get_port

@pytest.mark.asyncio
async def test_get_port_returns_valid_port():
    port = get_port()
    assert isinstance(port, int)
    assert 0 < port < 65536

@pytest.mark.asyncio
async def test_get_port_multiple_calls():
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1  # Ensure that multiple calls return different ports

@pytest.mark.asyncio
async def test_get_port_socket_bind_failure(monkeypatch):
    mock_socket = Mock()
    mock_socket.bind.side_effect = OSError("Bind failed")
    monkeypatch.setattr("socket.socket", lambda: mock_socket)

    with pytest.raises(OSError, match="Bind failed"):
        get_port()