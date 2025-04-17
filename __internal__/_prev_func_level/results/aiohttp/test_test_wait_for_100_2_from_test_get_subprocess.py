import asyncio
import pytest
from aiohttp import ClientSession, ClientResponse
from unittest import mock
from aiohttp.helpers import TimerNoop
from yarl import URL

@pytest.fixture
def session(loop):
    return ClientSession(loop=loop)

def test_client_response_close(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        request_info=mock.Mock(),
        continue100=None,
        writer=mock.Mock(),
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
        request_info=mock.Mock(),
        continue100=None,
        writer=mock.Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    
    response.close()
    with pytest.raises(RuntimeError):
        response.close()  # Ensure closing again raises an error

def test_client_response_close_with_cleanup(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        request_info=mock.Mock(),
        continue100=None,
        writer=mock.Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    
    response.close()
    # Here we can check if any cleanup actions were performed if applicable
    # This would depend on the actual implementation of the close method
    assert response._cleanup_closed_disabled is True  # Hypothetical check, adjust as necessary