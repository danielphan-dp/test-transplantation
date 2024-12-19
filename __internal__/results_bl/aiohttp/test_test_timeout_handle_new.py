import asyncio
from unittest import mock
import pytest
from aiohttp.helpers import TimeoutHandle

def test_timeout_handle_close_empty(loop: asyncio.AbstractEventLoop) -> None:
    handle = TimeoutHandle(loop, 10.2)
    handle.close()
    assert not handle._callbacks

def test_timeout_handle_close_with_callback(loop: asyncio.AbstractEventLoop) -> None:
    handle = TimeoutHandle(loop, 10.2)
    cb = mock.Mock()
    handle.register(cb)
    handle.close()
    assert cb not in handle._callbacks

def test_timeout_handle_multiple_callbacks(loop: asyncio.AbstractEventLoop) -> None:
    handle = TimeoutHandle(loop, 10.2)
    cb1 = mock.Mock()
    cb2 = mock.Mock()
    handle.register(cb1)
    handle.register(cb2)
    handle.close()
    assert cb1 not in handle._callbacks
    assert cb2 not in handle._callbacks

def test_timeout_handle_no_callbacks(loop: asyncio.AbstractEventLoop) -> None:
    handle = TimeoutHandle(loop, 10.2)
    handle.close()
    assert handle._callbacks == []