import asyncio
import pytest
from unittest import mock
from aiohttp import TCPConnector

@pytest.mark.asyncio
async def test_connector_close_method() -> None:
    """Test the close method of TCPConnector."""

    connector = TCPConnector()
    
    # Mock the internal cleanup method to track if it was called
    with mock.patch.object(connector, '_cleanup_closed', autospec=True) as mock_cleanup:
        connector.close()
        mock_cleanup.assert_called_once()

    # Ensure that the connector is marked as closed
    assert connector._closed is True

    # Test closing an already closed connector
    with mock.patch.object(connector, '_cleanup_closed', autospec=True) as mock_cleanup:
        connector.close()
        mock_cleanup.assert_called_once()  # Should not call cleanup again

    # Test if the close method can be called multiple times without error
    try:
        connector.close()
    except Exception as e:
        pytest.fail(f"close() raised an exception: {e}")

    # Test if the connector can be used after being closed
    with pytest.raises(RuntimeError, match="Connector is closed"):
        await connector.connect(mock.Mock(), [], mock.Mock())  # Attempt to connect after close

@pytest.mark.asyncio
async def test_connector_close_with_multiple_loops() -> None:
    """Test the close method of TCPConnector with multiple event loops."""

    async def close_connector() -> None:
        connector = TCPConnector()
        connector.close()

    loop1 = asyncio.new_event_loop()
    loop2 = asyncio.new_event_loop()
    
    try:
        await loop1.run_until_complete(close_connector())
        await loop2.run_until_complete(close_connector())
    finally:
        loop1.close()
        loop2.close()