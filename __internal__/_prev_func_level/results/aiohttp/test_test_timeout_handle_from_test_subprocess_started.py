import asyncio
import pytest
from unittest import mock
from aiohttp import ClientSession

@pytest.fixture
def session(loop: asyncio.AbstractEventLoop):
    return ClientSession(loop=loop)

def test_close_session(session: ClientSession) -> None:
    assert not session.closed
    session.close()
    assert session.closed

def test_close_multiple_times(session: ClientSession) -> None:
    session.close()
    session.close()  # Closing again should not raise an error
    assert session.closed

def test_close_with_callbacks(session: ClientSession) -> None:
    cb = mock.Mock()
    session._callbacks.append((cb, None))
    session.close()
    assert not session._callbacks
    cb.assert_not_called()  # Ensure callback is not called after close

def test_close_with_active_requests(session: ClientSession) -> None:
    async def make_request():
        async with session.get('http://httpbin.org/get') as response:
            return await response.json()

    task = loop.create_task(make_request())
    session.close()
    with pytest.raises(RuntimeError):
        loop.run_until_complete(task)  # Ensure it raises an error when trying to use closed session

def test_close_does_not_affect_new_session(loop: asyncio.AbstractEventLoop) -> None:
    session1 = ClientSession(loop=loop)
    session1.close()
    session2 = ClientSession(loop=loop)
    assert not session2.closed
    session2.close()