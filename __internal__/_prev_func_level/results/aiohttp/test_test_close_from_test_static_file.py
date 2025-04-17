import asyncio
import pytest
from unittest import mock
from aiohttp import ClientSession, ClientResponse
from aiohttp.helpers import TimerNoop
from aiohttp.connector import Connection
from yarl import URL

@pytest.fixture
def session(loop):
    return ClientSession(loop=loop)

def test_close_connection_is_none(loop, session):
    response = ClientResponse(
        "get",
        URL("http://test-close-connection.org"),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = False
    response._connection = mock.Mock()
    response.close()
    assert response._connection is None

def test_close_multiple_calls(loop, session):
    response = ClientResponse(
        "get",
        URL("http://test-close-multiple.org"),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = False
    response._connection = mock.Mock()
    response.close()
    response.close()  # Calling close again should not raise an error
    assert response._connection is None

def test_close_with_no_connection(loop, session):
    response = ClientResponse(
        "get",
        URL("http://test-close-no-connection.org"),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = False
    response._connection = None  # Simulating no connection
    response.close()
    assert response._connection is None

def test_close_after_already_closed(loop, session):
    response = ClientResponse(
        "get",
        URL("http://test-close-already-closed.org"),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = True
    response.close()  # Should not raise an error
    assert response._connection is None

def test_close_with_exception_handling(loop, session):
    response = ClientResponse(
        "get",
        URL("http://test-close-exception.org"),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = False
    response._connection = mock.Mock()
    response._connection.close.side_effect = Exception("Connection error")
    with pytest.raises(Exception):
        response.close()  # Should raise an exception due to connection close error
    assert response._connection is not None  # Connection should still be there until explicitly closed