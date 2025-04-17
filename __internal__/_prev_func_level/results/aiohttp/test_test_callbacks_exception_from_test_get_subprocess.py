import asyncio
import pytest
from unittest.mock import Mock
from aiohttp.connector import Connection

@pytest.mark.asyncio
async def test_close_method(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.closed = False

    conn.close()
    assert conn.closed

    # Test closing an already closed connection
    conn.close()
    assert conn.closed

    # Test if cleanup is called
    conn._cleanup_closed = Mock()
    conn.close()
    conn._cleanup_closed.assert_called_once()