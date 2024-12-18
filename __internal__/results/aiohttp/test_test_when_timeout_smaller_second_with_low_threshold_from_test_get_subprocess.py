import asyncio
import pytest
from aiohttp import ClientSession

@pytest.fixture
async def session(loop):
    async with ClientSession() as session:
        yield session

def test_close_session(session):
    assert session is not None
    assert not session.closed
    session.close()
    assert session.closed

def test_close_session_multiple_times(session):
    session.close()
    assert session.closed
    session.close()  # Closing again should not raise an error
    assert session.closed

def test_close_session_with_timeout(loop):
    timeout = 0.1
    timer = loop.time() + timeout

    session.close()
    assert session.closed
    assert isinstance(timer, float)  # Ensure timer is a float
    assert timer >= loop.time()  # Ensure timer is in the future

def test_close_session_with_active_requests(session):
    async def make_request():
        async with session.get('http://httpbin.org/get') as response:
            return await response.json()

    loop.run_until_complete(make_request())
    assert not session.closed
    session.close()
    assert session.closed

def test_close_session_with_exception_handling(session):
    session.close()
    try:
        session.get('http://httpbin.org/get')  # Should raise an error
    except Exception as e:
        assert isinstance(e, RuntimeError)  # Check for the expected exception type
    assert session.closed