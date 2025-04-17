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
    
    # Ensure the response is not closed initially
    assert not response.closed
    
    # Close the response
    response.close()
    
    # Verify that the response is closed
    assert response.closed

def test_client_response_close_multiple_calls(loop, session):
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
    assert response.closed
    
    # Call close again and ensure no errors occur
    response.close()
    assert response.closed

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
    
    # Simulate some operation before closing
    assert response._continue is None
    
    response.close()
    
    # Check if any cleanup actions are performed
    # This is a placeholder for actual cleanup verification
    assert response.closed  # Ensure it is closed after cleanup

def test_client_response_close_with_exception_handling(loop, session):
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
    
    try:
        response.close()
    except Exception as e:
        pytest.fail(f"Closing response raised an exception: {e}")
    
    assert response.closed