import asyncio
from unittest import mock
import pytest
from aiohttp import ClientRequest, ClientResponse

@pytest.mark.asyncio
async def test_close_method_with_active_writer(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    writer = mock.Mock()
    req._writer = writer

    req.close()
    
    assert req._writer is None
    assert writer.close.called

@pytest.mark.asyncio
async def test_close_method_when_already_closed(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    req._writer = None

    req.close()
    
    assert req._writer is None

@pytest.mark.asyncio
async def test_close_method_with_no_writer(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    req._writer = None

    req.close()
    
    assert req._writer is None

@pytest.mark.asyncio
async def test_close_method_with_multiple_calls(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    writer = mock.Mock()
    req._writer = writer

    req.close()
    req.close()
    
    assert req._writer is None
    assert writer.close.called

@pytest.mark.asyncio
async def test_close_method_with_response(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    writer = mock.Mock()
    req._writer = writer
    resp = ClientResponse("GET", req.url, loop=loop)
    req._response = resp

    req.close()
    
    assert req._writer is None
    assert resp._writer is None
    assert writer.close.called