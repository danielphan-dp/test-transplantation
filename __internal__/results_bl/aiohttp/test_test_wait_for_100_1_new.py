import asyncio
import pytest
from unittest import mock
from aiohttp import ClientSession, ClientResponse
from aiohttp.helpers import TimerNoop
from yarl import URL

@pytest.fixture
def session(loop):
    return ClientSession(loop=loop)

def test_close_response(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        continue100=loop.create_future(),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response.close()
    assert response._continue.done()  # Ensure that the future is done after close

def test_close_multiple_times(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        continue100=loop.create_future(),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response.close()
    with pytest.raises(RuntimeError):  # Expect an error when closing again
        response.close()

def test_close_with_no_continue(loop, session):
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        continue100=None,
        request_info=mock.Mock(),
        writer=mock.Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response.close()
    assert response._continue is None  # Ensure _continue remains None after close

def test_close_response_with_active_future(loop, session):
    future = loop.create_future()
    response = ClientResponse(
        "get",
        URL("http://python.org"),
        continue100=future,
        request_info=mock.Mock(),
        writer=mock.Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response.close()
    assert future.done()  # Ensure that the active future is marked as done after close