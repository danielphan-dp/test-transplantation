import asyncio
import pytest
from unittest.mock import MagicMock
from aiohttp.connector import Connection

@pytest.mark.asyncio
async def test_close_method():
    connector = MagicMock()
    key = MagicMock()
    protocol = MagicMock()
    loop = asyncio.get_event_loop()
    
    conn = Connection(connector, key, protocol, loop)
    
    # Ensure the connection is not closed initially
    assert not conn.closed
    
    # Call the close method
    conn.close()
    
    # Verify that the connection is marked as closed
    assert conn.closed

@pytest.mark.asyncio
async def test_close_method_multiple_calls():
    connector = MagicMock()
    key = MagicMock()
    protocol = MagicMock()
    loop = asyncio.get_event_loop()
    
    conn = Connection(connector, key, protocol, loop)
    
    # Close the connection for the first time
    conn.close()
    assert conn.closed
    
    # Call close again and ensure it does not raise an error
    conn.close()
    assert conn.closed

@pytest.mark.asyncio
async def test_close_method_with_cleanup():
    connector = MagicMock()
    key = MagicMock()
    protocol = MagicMock()
    loop = asyncio.get_event_loop()
    
    conn = Connection(connector, key, protocol, loop)
    
    # Mock the cleanup method
    conn._cleanup_closed = MagicMock()
    
    # Close the connection
    conn.close()
    
    # Ensure cleanup is called
    conn._cleanup_closed.assert_called_once()