import asyncio
import pytest
from aiohttp import ClientSession

@pytest.fixture
async def session(loop):
    async with ClientSession() as sess:
        yield sess

def test_close_session(loop, session):
    conn = session.connector
    assert conn is not None
    assert not conn.closed
    loop.run_until_complete(session.close())
    assert session.closed
    assert conn.closed

def test_close_already_closed_session(loop, session):
    conn = session.connector
    assert conn is not None
    assert not conn.closed
    loop.run_until_complete(session.close())
    assert session.closed
    assert conn.closed
    loop.run_until_complete(session.close())  # Closing again should not raise an error

def test_close_with_detach(loop, session):
    conn = session.connector
    assert conn is not None
    assert not conn.closed
    session.detach()
    assert session.connector is None
    assert session.closed
    assert not conn.closed
    loop.run_until_complete(conn.close())  # Ensure connection can still be closed after detach

def test_close_multiple_sessions(loop):
    async def create_and_close_session():
        async with ClientSession() as sess:
            conn = sess.connector
            assert conn is not None
            assert not conn.closed
            await sess.close()
            assert sess.closed
            assert conn.closed

    loop.run_until_complete(asyncio.gather(create_and_close_session(), create_and_close_session()))