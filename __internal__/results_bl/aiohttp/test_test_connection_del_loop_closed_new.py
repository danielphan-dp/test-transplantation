import asyncio
import gc
from unittest import mock
import pytest
from aiohttp.connector import Connection

def test_connection_close(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)

    conn.close()

    assert not connector._release.called

def test_connection_close_twice(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)

    conn.close()
    conn.close()

    assert not connector._release.called

def test_connection_close_with_exception(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)

    connector._release.side_effect = Exception("Release failed")
    
    with pytest.raises(Exception):
        conn.close()

    assert connector._release.called

def test_connection_close_after_del(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)

    del conn
    gc.collect()

    assert not connector._release.called

def test_connection_close_with_resource_warning(loop: asyncio.AbstractEventLoop) -> None:
    connector = mock.Mock()
    key = mock.Mock()
    protocol = mock.Mock()
    conn = Connection(connector, key, protocol, loop=loop)

    with pytest.warns(ResourceWarning):
        conn.close()

    assert not connector._release.called