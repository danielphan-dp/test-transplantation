import asyncio
import gc
from typing import Any
from unittest.mock import Mock
import pytest
from aiohttp.client_proto import ResponseHandler
from aiohttp.client_reqrep import ConnectionKey
from aiohttp.connector import BaseConnector, Connection

def test_close_without_callbacks(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    # No callbacks should be notified, so we can check for side effects if any

def test_close_with_multiple_callbacks(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    notified_count = 0

    def cb() -> None:
        nonlocal notified_count
        notified_count += 1

    conn.add_callback(cb)
    conn.add_callback(cb)
    conn.close()
    assert notified_count == 2

def test_close_with_no_callbacks(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    # Ensure no exceptions are raised and state is clean

def test_close_after_already_closed(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    conn.close()  # Closing again should not raise an error

def test_close_with_mocked_callback(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    mock_callback = Mock()
    conn.add_callback(mock_callback)
    conn.close()
    mock_callback.assert_called_once()