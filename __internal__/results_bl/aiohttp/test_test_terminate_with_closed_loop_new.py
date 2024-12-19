import asyncio
from unittest import mock
import pytest
from aiohttp import ClientRequest, ClientResponse
from yarl import URL

@pytest.fixture
def conn():
    return mock.Mock()

@pytest.mark.asyncio
async def test_close_method_with_active_writer(loop, conn):
    req = ClientRequest("get", URL("http://python.org"), loop=loop)
    writer = mock.Mock()
    req._writer = writer

    req.close()
    
    assert req._writer is None
    writer.close.assert_called_once()

@pytest.mark.asyncio
async def test_close_method_without_active_writer(loop, conn):
    req = ClientRequest("get", URL("http://python.org"), loop=loop)
    req._writer = None

    req.close()
    
    assert req._writer is None

@pytest.mark.asyncio
async def test_close_method_multiple_calls(loop, conn):
    req = ClientRequest("get", URL("http://python.org"), loop=loop)
    writer = mock.Mock()
    req._writer = writer

    req.close()
    req.close()
    
    assert req._writer is None
    writer.close.assert_called_once()