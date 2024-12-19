import asyncio
import pytest
from unittest import mock
from aiohttp import ClientSession, ClientResponse
from aiohttp.helpers import TimerNoop
from yarl import URL

@pytest.fixture
def session(loop):
    return ClientSession(loop=loop)

def test_close_multiple_calls(loop, session):
    response = ClientResponse(
        "get",
        URL("http://example.com"),
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
    assert response._closed is True
    assert response._connection is None
    response.close()  # Calling close again should not raise an error

def test_close_with_no_connection(loop, session):
    response = ClientResponse(
        "get",
        URL("http://example.com"),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = False
    response._connection = None
    response.close()
    assert response._closed is True
    assert response._connection is None

def test_close_already_closed(loop, session):
    response = ClientResponse(
        "get",
        URL("http://example.com"),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = True
    response.close()  # Should not raise an error when already closed
    assert response._closed is True

def test_close_with_active_connection(loop, session):
    response = ClientResponse(
        "get",
        URL("http://example.com"),
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
    assert response._closed is True
    assert response._connection is None

def test_close_with_exception_handling(loop, session):
    response = ClientResponse(
        "get",
        URL("http://example.com"),
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
    response._connection.close = mock.Mock(side_effect=Exception("Connection error"))
    response.close()  # Should handle exception without crashing
    assert response._closed is True
    assert response._connection is None