import asyncio
import pytest
from unittest.mock import Mock
from aiohttp.connector import Connection

@pytest.mark.asyncio
async def test_close_notifies_callbacks(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    notified = False

    def cb() -> None:
        nonlocal notified
        notified = True

    conn.add_callback(cb)
    conn.close()
    assert notified

@pytest.mark.asyncio
async def test_close_does_not_notify_if_already_closed(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    notified = False

    def cb() -> None:
        nonlocal notified
        notified = True

    conn.add_callback(cb)
    conn.close()
    notified_before = notified
    conn.close()
    assert notified_before == notified

@pytest.mark.asyncio
async def test_close_with_mocked_callback(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    mock_callback = Mock()
    conn.add_callback(mock_callback)
    conn.close()
    mock_callback.assert_called_once()