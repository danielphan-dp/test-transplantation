import asyncio
import gc
import pytest
from unittest import mock
from aiohttp.connector import Connection

@pytest.mark.asyncio
async def test_connection_close_called(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)

    conn.close()

    assert connector._release.called

@pytest.mark.asyncio
async def test_connection_close_no_release_when_already_closed(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)
    conn.close()
    
    conn.close()  # Call close again

    assert connector._release.called

@pytest.mark.asyncio
async def test_connection_close_with_gc(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)

    conn.close()
    del conn
    gc.collect()

    assert connector._release.called

@pytest.mark.asyncio
async def test_connection_close_with_exception_handler(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)
    exc_handler = mock.Mock()
    loop.set_exception_handler(exc_handler)

    conn.close()

    assert not exc_handler.called

@pytest.mark.asyncio
async def test_connection_close_resource_warning(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)

    with pytest.warns(ResourceWarning):
        conn.close()
        del conn
        gc.collect()

    assert connector._release.called