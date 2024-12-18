import asyncio
import pytest
from unittest import mock
from aiohttp import ClientSession, ClientResponse
from aiohttp.helpers import TimerNoop
from yarl import URL

@pytest.mark.asyncio
async def test_close_edge_cases(loop: asyncio.AbstractEventLoop, session: ClientSession) -> None:
    response = ClientResponse(
        "get",
        URL("http://test-close.org"),
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
    
    # First close should set the connection to None
    response.close()
    assert response._connection is None
    
    # Closing again should not raise an error
    response.close()
    
    # Check if closed state is maintained
    assert response._closed is True

    # Attempt to access connection after closing
    with pytest.raises(AttributeError):
        _ = response._connection

    # Ensure that calling close multiple times does not affect the state
    response.close()
    assert response._closed is True

    # Check if the response can be closed without any connection
    response._connection = None
    response.close()
    assert response._closed is True