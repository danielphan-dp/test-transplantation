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
        request_info=mock.Mock(),
        continue100=None,
        writer=mock.Mock(),
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response.close()
    assert response._continue is None

def test_close_multiple_times(loop, session):
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
        response.close()

def test_close_with_active_request(loop, session):
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
    response._continue = mock.Mock()
    response.close()
    assert response._continue is None

def test_close_after_read(loop, session):
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
    response.read = mock.Mock(return_value=b'content')
    response.read()
    response.close()
    assert response._continue is None