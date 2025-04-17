import asyncio
import gc
import pytest
from unittest import mock
from aiohttp import BaseConnector
from aiohttp.client_proto import ConnectionKey

@pytest.mark.skipif(
    sys.implementation.name != "cpython", reason="CPython GC is required for the test"
)
def test_close_with_active_connections(loop: asyncio.AbstractEventLoop, key: ConnectionKey) -> None:
    async def make_conn() -> BaseConnector:
        return BaseConnector()

    conn = loop.run_until_complete(make_conn())
    transp = create_mocked_conn(loop)
    conn._conns[key] = deque([(transp, 123)])

    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    conn.close()

    assert not conns_impl
    transp.close.assert_called_once()
    assert not exc_handler.called

@pytest.mark.skipif(
    sys.implementation.name != "cpython", reason="CPython GC is required for the test"
)
def test_close_with_no_active_connections(loop: asyncio.AbstractEventLoop) -> None:
    async def make_conn() -> BaseConnector:
        return BaseConnector()

    conn = loop.run_until_complete(make_conn())
    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    conn.close()

    assert not conns_impl
    assert not exc_handler.called

@pytest.mark.skipif(
    sys.implementation.name != "cpython", reason="CPython GC is required for the test"
)
def test_close_multiple_times(loop: asyncio.AbstractEventLoop, key: ConnectionKey) -> None:
    async def make_conn() -> BaseConnector:
        return BaseConnector()

    conn = loop.run_until_complete(make_conn())
    transp = create_mocked_conn(loop)
    conn._conns[key] = deque([(transp, 123)])

    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    conn.close()
    conn.close()

    assert not conns_impl
    transp.close.assert_called_once()
    assert not exc_handler.called

@pytest.mark.skipif(
    sys.implementation.name != "cpython", reason="CPython GC is required for the test"
)
def test_close_with_exception_handler(loop: asyncio.AbstractEventLoop, key: ConnectionKey) -> None:
    async def make_conn() -> BaseConnector:
        return BaseConnector()

    conn = loop.run_until_complete(make_conn())
    transp = create_mocked_conn(loop)
    conn._conns[key] = deque([(transp, 123)])

    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    conn.close()

    assert not conns_impl
    transp.close.assert_called_once()
    assert exc_handler.called

@pytest.mark.skipif(
    sys.implementation.name != "cpython", reason="CPython GC is required for the test"
)
def test_close_with_gc_collect(loop: asyncio.AbstractEventLoop, key: ConnectionKey) -> None:
    async def make_conn() -> BaseConnector:
        return BaseConnector()

    conn = loop.run_until_complete(make_conn())
    transp = create_mocked_conn(loop)
    conn._conns[key] = deque([(transp, 123)])

    conns_impl = conn._conns
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    conn.close()
    gc.collect()

    assert not conns_impl
    transp.close.assert_called_once()
    assert not exc_handler.called