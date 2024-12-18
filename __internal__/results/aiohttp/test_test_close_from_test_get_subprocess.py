import asyncio
import pytest
from unittest import mock
from aiohttp import ClientSession, ClientResponse
from aiohttp.helpers import TimerNoop
from aiohttp.client_reqrep import RequestInfo
from aiohttp.connector import Connection
from yarl import URL

@pytest.mark.asyncio
async def test_close_edge_cases(loop: asyncio.AbstractEventLoop, session: ClientSession) -> None:
    response = ClientResponse(
        "get",
        URL("http://test-close.org"),
        request_info=RequestInfo("GET", URL("http://test-close.org")),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    
    response._closed = False
    response._connection = mock.Mock()
    
    # First close should set connection to None
    response.close()
    assert response._connection is None
    
    # Closing again should not raise an error
    response.close()
    
    # Check if closed state is maintained
    assert response._closed is True

    # Test if calling close on an already closed response does not affect state
    response.close()
    assert response._closed is True

    # Test if the connection is still None after multiple closes
    assert response._connection is None

    # Test if the response can be closed after being marked as closed
    response._closed = False
    response.close()
    assert response._connection is None
    assert response._closed is True