import asyncio
import contextlib
import pytest
from aiohttp import TCPConnector, ClientSession

@pytest.mark.asyncio
async def test_connector_close() -> None:
    connector = TCPConnector()
    await connector.close()  # Test closing the connector without any active sessions

    # Ensure that closing the connector does not raise an error
    try:
        await connector.close()
    except Exception as e:
        pytest.fail(f"Closing connector raised an exception: {e}")

@pytest.mark.asyncio
async def test_connector_close_with_active_session(loop: asyncio.AbstractEventLoop) -> None:
    connector = TCPConnector()
    
    async def make_sess() -> ClientSession:
        return ClientSession(connector=connector)

    session = await make_sess()
    
    await session.close()  # Close the session first
    await connector.close()  # Then close the connector

    # Ensure that closing the connector after session is closed does not raise an error
    try:
        await connector.close()
    except Exception as e:
        pytest.fail(f"Closing connector after session raised an exception: {e}")

@pytest.mark.asyncio
async def test_connector_close_multiple_times(loop: asyncio.AbstractEventLoop) -> None:
    connector = TCPConnector()
    
    await connector.close()  # First close should succeed
    await connector.close()  # Second close should also succeed without error

    # Ensure that closing the connector multiple times does not raise an error
    try:
        await connector.close()
    except Exception as e:
        pytest.fail(f"Closing connector multiple times raised an exception: {e}")