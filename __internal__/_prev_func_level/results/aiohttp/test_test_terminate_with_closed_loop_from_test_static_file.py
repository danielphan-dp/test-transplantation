import asyncio
from unittest import mock
import pytest
from aiohttp import ClientRequest, ClientResponse, BaseConnector

@pytest.mark.asyncio
async def test_close_method(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    writer = mock.Mock()
    req._writer = writer

    assert req._writer is not None

    req.close()
    
    assert req._writer is None
    assert writer.cancel.called

    # Test closing an already closed request
    req.close()
    assert req._writer is None

    # Test if close method can be called multiple times without error
    try:
        req.close()
    except Exception as e:
        pytest.fail(f"close() raised an exception: {e}")

    # Test if the response is closed properly
    resp = ClientResponse("GET", req.url, loop=loop)
    resp._writer = writer
    resp.close()
    assert resp._writer is None
    assert writer.cancel.called

    # Ensure that the connection is terminated
    req.terminate()
    assert req._writer is None
    assert not writer.cancel.called