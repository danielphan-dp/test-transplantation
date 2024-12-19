import asyncio
import pytest
from aiohttp import ClientSession

@pytest.fixture
async def session():
    async with ClientSession() as sess:
        yield sess

def test_close_session(session):
    session.close()
    assert session.closed is True

def test_close_multiple_times(session):
    session.close()
    session.close()
    assert session.closed is True

def test_close_with_active_requests(session):
    async def make_request():
        async with session.get('http://httpbin.org/get') as response:
            return await response.json()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(make_request())
    session.close()
    assert session.closed is True

def test_close_after_context_manager():
    async def test_context_manager():
        async with ClientSession() as sess:
            pass
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test_context_manager())
    # No assertion needed, just ensuring it doesn't raise an error

def test_close_without_opening(session):
    session.close()
    assert session.closed is True