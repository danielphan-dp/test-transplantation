import asyncio
from unittest import mock
import pytest
from aiohttp import ClientRequest, ClientResponse, BaseConnector
from yarl import URL

@pytest.mark.asyncio
async def test_close_method_with_active_writer(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", URL("http://python.org"), loop=loop)
    writer = mock.Mock()
    req._writer = writer

    req.close()
    
    assert req._writer is None
    assert writer.close.called

@pytest.mark.asyncio
async def test_close_method_without_active_writer(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", URL("http://python.org"), loop=loop)
    req._writer = None

    req.close()
    
    assert req._writer is None

@pytest.mark.asyncio
async def test_close_method_multiple_calls(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", URL("http://python.org"), loop=loop)
    writer = mock.Mock()
    req._writer = writer

    req.close()
    req.close()  # Call close again

    assert req._writer is None
    assert writer.close.called

@pytest.mark.asyncio
async def test_close_method_with_response(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", URL("http://python.org"), loop=loop)
    resp = ClientResponse("GET", URL("http://python.org"), loop=loop)
    req._writer = mock.Mock()
    req._response = resp

    req.close()

    assert req._response is None
    assert req._writer is None
    assert req._writer.close.called

@pytest.mark.asyncio
async def test_close_method_with_exception_handling(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", URL("http://python.org"), loop=loop)
    req._writer = mock.Mock(side_effect=Exception("Writer error"))

    with pytest.raises(Exception, match="Writer error"):
        req.close()