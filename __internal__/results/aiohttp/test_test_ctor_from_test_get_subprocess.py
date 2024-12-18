import asyncio
import pytest
from unittest.mock import Mock
from aiohttp.connector import Connection

@pytest.mark.asyncio
async def test_close_connection_not_closed(connector: Mock, key: Mock, protocol: Mock, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    assert conn.closed is True

@pytest.mark.asyncio
async def test_close_connection_already_closed(connector: Mock, key: Mock, protocol: Mock, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    with pytest.raises(RuntimeError, match="Connection is already closed"):
        conn.close()

@pytest.mark.asyncio
async def test_close_connection_with_cleanup(connector: Mock, key: Mock, protocol: Mock, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    assert conn._cleanup_closed_transports == []  # Assuming this is a property to check cleanup

@pytest.mark.asyncio
async def test_close_connection_with_active_requests(connector: Mock, key: Mock, protocol: Mock, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    # Simulate an active request
    conn._active_requests = [Mock()]
    conn.close()
    assert conn._active_requests == []  # Ensure active requests are cleared on close

@pytest.mark.asyncio
async def test_close_connection_twice(connector: Mock, key: Mock, protocol: Mock, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    conn.close()  # Closing again should not raise an error
    assert conn.closed is True