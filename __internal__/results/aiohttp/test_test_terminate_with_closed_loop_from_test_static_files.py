import asyncio
from unittest import mock
import pytest
from aiohttp import ClientRequest, ClientResponse, BaseConnector

@pytest.mark.asyncio
async def test_close_method_with_active_connections(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    writer = mock.Mock()
    req._writer = writer

    await req.send(conn)
    assert req._writer is not None

    req.close()
    assert req._writer is None
    assert writer.cancel.called

@pytest.mark.asyncio
async def test_close_method_without_active_connections(loop: asyncio.AbstractEventLoop) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    req._writer = None

    req.close()
    assert req._writer is None

@pytest.mark.asyncio
async def test_close_method_multiple_calls(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    writer = mock.Mock()
    req._writer = writer

    await req.send(conn)
    assert req._writer is not None

    req.close()
    assert req._writer is None

    req.close()  # Call close again
    assert req._writer is None
    assert writer.cancel.called

@pytest.mark.asyncio
async def test_close_method_with_response(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    writer = mock.Mock()
    req._writer = writer
    resp = await req.send(conn)

    assert resp is not None
    req.close()
    assert req._writer is None
    assert resp._writer is None
    assert writer.cancel.called

@pytest.mark.asyncio
async def test_close_method_with_exception_handling(loop: asyncio.AbstractEventLoop, conn: mock.Mock) -> None:
    req = ClientRequest("get", "http://python.org", loop=loop)
    writer = mock.Mock()
    req._writer = writer

    with mock.patch.object(req, "close", side_effect=Exception("Close failed")):
        with pytest.raises(Exception, match="Close failed"):
            req.close()

    assert req._writer is not None
    req.close()
    assert req._writer is None
    assert writer.cancel.called