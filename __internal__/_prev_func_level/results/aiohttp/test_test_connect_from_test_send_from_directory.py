import asyncio
import pytest
from aiohttp import ClientSession

@pytest.mark.asyncio
async def test_close_connector():
    connector = ClientSession().connector
    await connector.close()
    assert connector._closed is True

@pytest.mark.asyncio
async def test_close_multiple_times():
    connector = ClientSession().connector
    await connector.close()
    await connector.close()  # Closing again should not raise an error
    assert connector._closed is True

@pytest.mark.asyncio
async def test_close_with_active_connections():
    connector = ClientSession().connector
    # Simulate an active connection
    connector._conns = {1: 'active_connection'}
    await connector.close()
    assert connector._closed is True
    assert not connector._conns  # Ensure connections are cleaned up

@pytest.mark.asyncio
async def test_close_with_no_connections():
    connector = ClientSession().connector
    await connector.close()
    assert connector._closed is True
    assert not connector._conns  # Ensure no connections remain

@pytest.mark.asyncio
async def test_close_with_cleanup_disabled():
    connector = ClientSession().connector
    connector._cleanup_closed_disabled = True
    await connector.close()
    assert connector._closed is True
    assert connector._cleanup_closed_transports == []  # No cleanup should occur

@pytest.mark.asyncio
async def test_close_warning_on_unclosed_connector():
    connector = ClientSession().connector
    await connector.close()
    with pytest.warns(ResourceWarning, match="Unclosed connector"):
        await connector.close()  # Should trigger a warning on second close