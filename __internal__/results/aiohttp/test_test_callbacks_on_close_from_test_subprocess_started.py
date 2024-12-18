import asyncio
import pytest
from unittest.mock import Mock
from aiohttp.connector import Connection

@pytest.mark.asyncio
async def test_close_not_called_twice(connector, key, protocol, loop):
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    assert conn.closed
    with pytest.raises(RuntimeError):
        conn.close()

@pytest.mark.asyncio
async def test_close_with_callbacks(connector, key, protocol, loop):
    conn = Connection(connector, key, protocol, loop)
    notified = False

    def cb() -> None:
        nonlocal notified
        notified = True

    conn.add_callback(cb)
    conn.close()
    assert notified

@pytest.mark.asyncio
async def test_close_cleanup(connector, key, protocol, loop):
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    assert conn._cleanup_closed_transports == []

@pytest.mark.asyncio
async def test_close_with_active_connections(connector, key, protocol, loop):
    conn = Connection(connector, key, protocol, loop)
    conn._conns = {1: Mock(), 2: Mock()}
    conn.close()
    assert conn._conns == {}
    assert conn.closed

@pytest.mark.asyncio
async def test_close_no_active_connections(connector, key, protocol, loop):
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    assert conn._conns == {}
    assert conn.closed