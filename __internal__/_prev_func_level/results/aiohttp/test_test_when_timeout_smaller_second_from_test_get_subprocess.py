import asyncio
import pytest
from aiohttp import ClientSession

@pytest.fixture
async def session():
    async with ClientSession() as session:
        yield session

def test_close_session(session: ClientSession) -> None:
    assert session is not None
    assert not session.closed
    session.close()
    assert session.closed

def test_close_multiple_times(session: ClientSession) -> None:
    session.close()
    assert session.closed
    session.close()  # Closing again should not raise an error
    assert session.closed

def test_close_with_timeout(loop: asyncio.AbstractEventLoop) -> None:
    timeout = 0.1
    session = ClientSession()
    assert session is not None
    session.close()
    assert session.closed

    # Simulate a timeout scenario
    async def close_with_timeout():
        await asyncio.sleep(timeout)
        session.close()

    loop.run_until_complete(close_with_timeout())
    assert session.closed

def test_close_session_context_manager() -> None:
    async with ClientSession() as session:
        assert session is not None
        assert not session.closed
    assert session.closed

def test_close_session_after_request(session: ClientSession) -> None:
    async def fetch():
        async with session.get('http://httpbin.org/get') as response:
            assert response.status == 200

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch())
    session.close()
    assert session.closed