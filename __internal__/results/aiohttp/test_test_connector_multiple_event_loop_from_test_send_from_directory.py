import asyncio
import pytest
from unittest import mock
from aiohttp import TCPConnector

@pytest.mark.asyncio
async def test_connector_close_method() -> None:
    """Test the close method of TCPConnector."""

    conn = TCPConnector()
    assert not conn._closed  # Ensure the connector is initially open

    # Mock the cleanup method to simulate closing behavior
    with mock.patch.object(conn, '_cleanup_closed', autospec=True) as mock_cleanup:
        conn.close()
        assert conn._closed  # Ensure the connector is marked as closed
        mock_cleanup.assert_called_once()  # Ensure cleanup was called

    # Test that calling close again does not raise an error
    conn.close()  # Should not raise an error

    # Test that the connector can be reopened
    conn = TCPConnector()
    assert not conn._closed  # Ensure the connector is open again

@pytest.mark.asyncio
async def test_connector_close_with_active_connections() -> None:
    """Test the close method with active connections."""

    conn = TCPConnector()
    # Simulate an active connection
    req = mock.Mock()
    conn._conns[req] = mock.Mock()  # Add a mock connection

    conn.close()
    assert conn._closed  # Ensure the connector is marked as closed
    assert req not in conn._conns  # Ensure active connections are cleaned up

@pytest.mark.asyncio
async def test_connector_close_multiple_times() -> None:
    """Test closing the connector multiple times."""

    conn = TCPConnector()
    conn.close()
    assert conn._closed  # Ensure the connector is closed

    # Closing again should not raise an error
    conn.close()  # Should not raise an error

@pytest.mark.asyncio
async def test_connector_close_with_exception_handling() -> None:
    """Test the close method with exception handling."""

    conn = TCPConnector()
    with mock.patch.object(conn, '_cleanup_closed', side_effect=Exception("Cleanup failed")):
        with pytest.raises(Exception, match="Cleanup failed"):
            conn.close()  # Ensure exception is raised during cleanup

    assert conn._closed  # Ensure the connector is still marked as closed after exception