import asyncio
import pytest
from unittest.mock import Mock
from aiohttp import ClientSession, ClientResponse
from aiohttp.helpers import TimerNoop
from aiohttp.client_reqrep import RequestInfo
from aiohttp.connector import Connection
from yarl import URL

@pytest.fixture
def session(loop):
    return ClientSession(loop=loop)

def test_client_response_close(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        request_info=RequestInfo("GET", URL("http://python.org")),
        continue100=None,
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
        request_info=RequestInfo("GET", URL("http://python.org")),
        continue100=None,
        writer=Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    
    response.close()
    assert response.closed
    response.close()  # Closing again should not raise an error

def test_client_response_close_with_cleanup(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        request_info=RequestInfo("GET", URL("http://python.org")),
        continue100=None,
        writer=Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    
    response.close()
    # Here we could check if any cleanup actions were performed, if applicable
    assert response.closed

def test_client_response_close_no_double_close_error(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        request_info=RequestInfo("GET", URL("http://python.org")),
        continue100=None,
        writer=Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    
    response.close()
    try:
        response.close()  # Should not raise an error
    except Exception as e:
        pytest.fail(f"Closing response twice raised an exception: {e}")