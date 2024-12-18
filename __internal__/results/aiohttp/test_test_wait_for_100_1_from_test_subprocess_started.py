import asyncio
import pytest
from unittest.mock import Mock
from aiohttp import ClientSession, ClientResponse
from aiohttp.helpers import TimerNoop
from yarl import URL

@pytest.fixture
def session(loop):
    return ClientSession(loop=loop)

def test_client_response_close(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        continue100=loop.create_future(),
        request_info=Mock(),
        writer=Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    
    assert not response.closed
    response.close()
    assert response.closed

def test_client_response_close_twice(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        continue100=loop.create_future(),
        request_info=Mock(),
        writer=Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    
    response.close()
    with pytest.raises(RuntimeError, match="Cannot close a closed response"):
        response.close()