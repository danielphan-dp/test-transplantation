import asyncio
import gc
import pytest
from unittest import mock
from aiohttp import BaseConnector
from aiohttp.client_reqrep import ConnectionKey

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
    transp.close.assert_called_with()
    assert exc_handler.called

def test_close_with_no_active_connections(loop: asyncio.AbstractEventLoop) -> None:
    async def make_conn() -> BaseConnector:
        return BaseConnector()

    conn = loop.run_until_complete(make_conn())
    conns_impl = conn._conns

    conn.close()

    assert not conns_impl
    assert not conn._cleanup_closed_transports

def test_close_twice(loop: asyncio.AbstractEventLoop, key: ConnectionKey) -> None:
    async def make_conn() -> BaseConnector:
        return BaseConnector()

    conn = loop.run_until_complete(make_conn())
    transp = create_mocked_conn(loop)
    conn._conns[key] = deque([(transp, 123)])

    conn.close()
    conn.close()  # Closing again should not raise an error

    assert not conn._conns
    transp.close.assert_called_with()