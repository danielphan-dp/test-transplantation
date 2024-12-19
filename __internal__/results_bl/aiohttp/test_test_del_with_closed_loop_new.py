import asyncio
import gc
import pytest
from unittest import mock
from aiohttp import BaseConnector
from aiohttp.client_proto import ConnectionKey

@pytest.mark.skipif(sys.implementation.name != 'cpython', reason='CPython GC is required for the test')
def test_close_method(loop: asyncio.AbstractEventLoop, key: ConnectionKey) -> None:
    async def make_conn() -> BaseConnector:
        return BaseConnector()

    conn = loop.run_until_complete(make_conn())
    conn.close()

    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()

    assert conn._conns == {}
    assert not conn._closed
    assert conn._loop.is_closed()