import asyncio
import gc
from collections import deque
from unittest import mock
import pytest
import aiohttp
from aiohttp.client_proto import ResponseHandler
from aiohttp.connector import ConnectionKey

@pytest.mark.skipif(sys.implementation.name != 'cpython', reason='CPython GC is required for the test')
def test_del_with_open_connections(loop: asyncio.AbstractEventLoop, key: ConnectionKey) -> None:
    async def make_conn() -> aiohttp.BaseConnector:
        return aiohttp.BaseConnector()

    conn = loop.run_until_complete(make_conn())
    transp = create_mocked_conn(loop)
    conn._conns[key] = deque([(transp, 123)])

    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()

    assert not conns_impl
    assert not transp.close.called
    assert exc_handler.called

def test_del_with_multiple_connections(loop: asyncio.AbstractEventLoop) -> None:
    async def make_conn() -> aiohttp.BaseConnector:
        return aiohttp.BaseConnector()

    conn = loop.run_until_complete(make_conn())
    key1 = ConnectionKey("localhost", 80, False, True, None, None, None)
    key2 = ConnectionKey("localhost", 81, False, True, None, None, None)
    transp1 = create_mocked_conn(loop)
    transp2 = create_mocked_conn(loop)
    conn._conns[key1] = deque([(transp1, 123)])
    conn._conns[key2] = deque([(transp2, 456)])

    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()

    assert not conns_impl
    assert not transp1.close.called
    assert not transp2.close.called
    assert exc_handler.called

def test_del_with_no_connections(loop: asyncio.AbstractEventLoop) -> None:
    async def make_conn() -> aiohttp.BaseConnector:
        return aiohttp.BaseConnector()

    conn = loop.run_until_complete(make_conn())
    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()

    assert not conns_impl
    assert exc_handler.called

def test_del_with_closed_connection(loop: asyncio.AbstractEventLoop, key: ConnectionKey) -> None:
    async def make_conn() -> aiohttp.BaseConnector:
        return aiohttp.BaseConnector()

    conn = loop.run_until_complete(make_conn())
    transp = create_mocked_conn(loop)
    transp.closed.set_result(None)
    conn._conns[key] = deque([(transp, 123)])

    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()

    assert not conns_impl
    assert transp.close.called
    assert exc_handler.called