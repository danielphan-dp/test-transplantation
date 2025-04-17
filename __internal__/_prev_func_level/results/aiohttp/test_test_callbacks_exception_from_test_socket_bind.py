import asyncio
import pytest
from unittest.mock import MagicMock
from aiohttp.connector import Connection

@pytest.mark.asyncio
async def test_close_method(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.closed = False

    # Test normal close
    conn.close()
    assert conn.closed

    # Test double close
    conn.close()
    assert conn.closed

    # Test close with callbacks
    notified = False

    def cb() -> None:
        nonlocal notified
        notified = True

    conn.add_callback(cb)
    conn.close()
    assert notified

    # Test close when already closed
    conn.closed = True
    conn.close()
    assert conn.closed

    # Test close with mock
    mock_connector = MagicMock()
    conn = Connection(mock_connector, key, protocol, loop)
    conn.close()
    mock_connector.close.assert_called_once()