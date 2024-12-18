import asyncio
import contextlib
import pytest
from aiohttp import TCPConnector, ClientSession

@pytest.mark.asyncio
async def test_connector_close() -> None:
    connector = TCPConnector()
    assert not connector._closed  # Ensure connector is initially open

    await connector.close()  # Close the connector
    assert connector._closed  # Check if the connector is closed

    with pytest.raises(RuntimeError, match="Connector is closed"):
        await connector.close()  # Attempt to close again should raise an error

@pytest.mark.asyncio
async def test_connector_close_with_active_sessions(loop: asyncio.AbstractEventLoop) -> None:
    connector = TCPConnector()
    session = ClientSession(connector=connector)

    await connector.close()  # Close the connector
    assert connector._closed  # Ensure the connector is closed

    with pytest.raises(RuntimeError, match="Session and connector have to use same event loop"):
        await session.close()  # Attempt to close session after connector is closed

    await session.__aexit__(None, None, None)  # Ensure session cleanup is handled

@pytest.mark.asyncio
async def test_connector_close_multiple_times() -> None:
    connector = TCPConnector()
    await connector.close()  # First close should succeed
    assert connector._closed

    await connector.close()  # Second close should not raise an error
    assert connector._closed  # Still should be closed

@pytest.mark.asyncio
async def test_connector_close_with_pending_requests() -> None:
    connector = TCPConnector()
    
    async def make_request():
        async with ClientSession(connector=connector) as session:
            async with session.get('http://example.com') as response:
                return await response.text()

    task = asyncio.create_task(make_request())
    await asyncio.sleep(0.1)  # Allow the request to start

    await connector.close()  # Close the connector while request is pending
    assert connector._closed  # Ensure the connector is closed

    with pytest.raises(RuntimeError, match="Connector is closed"):
        await task  # Ensure the pending request raises an error when completed