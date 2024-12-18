import asyncio
import pytest
from aiohttp import ClientSession

@pytest.fixture
async def session(loop):
    async with ClientSession() as session:
        yield session

def test_close_session(loop, session):
    conn = session.connector
    assert conn is not None
    assert not conn.closed
    session.close()
    assert session.closed
    assert conn.closed

def test_close_already_closed_session(loop, session):
    session.close()
    assert session.closed
    conn = session.connector
    assert conn is not None
    assert conn.closed

def test_close_with_active_requests(loop, session):
    async def make_request():
        async with session.get('http://httpbin.org/get') as response:
            return await response.json()

    task = loop.create_task(make_request())
    loop.run_until_complete(asyncio.sleep(0.1))  # Allow request to start
    session.close()
    assert session.closed
    with pytest.raises(RuntimeError):
        loop.run_until_complete(task)

def test_close_multiple_times(loop, session):
    session.close()
    assert session.closed
    session.close()  # Closing again should not raise an error
    assert session.closed

def test_close_with_detach(loop, session):
    conn = session.connector
    assert conn is not None
    session.detach()
    assert session.connector is None
    session.close()
    assert session.closed
    assert not conn.closed