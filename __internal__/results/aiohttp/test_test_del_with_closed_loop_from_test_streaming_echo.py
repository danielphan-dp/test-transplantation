import asyncio
import gc
from collections import deque
from unittest import mock
import pytest
import aiohttp
from aiohttp.client_proto import ResponseHandler
from aiohttp.client_reqrep import ConnectionKey

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

    # Additional assertions to check if the connection was properly cleaned up
    assert conn._conns.get(key) is None
    assert exc_handler.call_count == 1

@pytest.mark.skipif(sys.implementation.name != 'cpython', reason='CPython GC is required for the test')
def test_del_with_multiple_keys(loop: asyncio.AbstractEventLoop) -> None:
    async def make_conn() -> aiohttp.BaseConnector:
        return aiohttp.BaseConnector()

    conn = loop.run_until_complete(make_conn())
    keys = [ConnectionKey("localhost", 80, False, True, None, None, None) for _ in range(3)]
    for key in keys:
        transp = create_mocked_conn(loop)
        conn._conns[key] = deque([(transp, 123)])

    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()

    assert not conns_impl
    assert all(not transp.close.called for key in keys)
    assert exc_handler.called

@pytest.mark.skipif(sys.implementation.name != 'cpython', reason='CPython GC is required for the test')
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
    assert exc_handler.call_count == 1