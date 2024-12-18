import asyncio
import contextlib
import pytest
from aiohttp import TCPConnector, ClientSession

@pytest.mark.asyncio
async def test_connector_close() -> None:
    connector = TCPConnector()
    assert not connector._closed

    await connector.close()
    assert connector._closed

@pytest.mark.asyncio
async def test_connector_close_multiple_times() -> None:
    connector = TCPConnector()
    await connector.close()
    assert connector._closed

    await connector.close()  # Closing again should not raise an error
    assert connector._closed

@pytest.mark.asyncio
async def test_connector_close_with_active_session(loop: asyncio.AbstractEventLoop) -> None:
    connector = TCPConnector()
    session = ClientSession(connector=connector)

    await session.close()
    await connector.close()
    assert connector._closed

@pytest.mark.asyncio
async def test_connector_close_with_exception_handling() -> None:
    connector = TCPConnector()
    await connector.close()

    with pytest.raises(RuntimeError, match="Cannot close a closed connector"):
        await connector.close()  # Attempting to close again should raise an error

@pytest.mark.asyncio
async def test_connector_close_with_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    another_loop = asyncio.new_event_loop()
    with contextlib.closing(another_loop):
        connector = another_loop.run_until_complete(TCPConnector())
        await connector.close()
        assert connector._closed
        another_loop.run_until_complete(connector.close())  # Should not raise an error