import asyncio
import gc
from unittest.mock import Mock
import pytest
from aiohttp.client_proto import ResponseHandler
from aiohttp.client_reqrep import ConnectionKey
from aiohttp.connector import BaseConnector, Connection

def test_close_no_callbacks(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    # No exceptions should be raised and no callbacks should be called

def test_close_with_callbacks(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    notified = False

    def callback() -> None:
        nonlocal notified
        notified = True

    conn.add_callback(callback)
    conn.close()
    assert notified

def test_close_multiple_callbacks(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    notified1 = False
    notified2 = False

    def callback1() -> None:
        nonlocal notified1
        notified1 = True

    def callback2() -> None:
        nonlocal notified2
        notified2 = True

    conn.add_callback(callback1)
    conn.add_callback(callback2)
    conn.close()
    assert notified1
    assert notified2

def test_close_exception_in_callback(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    notified = False

    def callback() -> None:
        raise Exception("Callback exception")

    conn.add_callback(callback)
    
    with pytest.raises(Exception):
        conn.close()  # Ensure that the exception is raised when closing

def test_close_after_already_closed(connector: BaseConnector, key: ConnectionKey, protocol: ResponseHandler, loop: asyncio.AbstractEventLoop) -> None:
    conn = Connection(connector, key, protocol, loop)
    conn.close()
    # Closing again should not raise an error
    conn.close()