import asyncio
import gc
import pytest
from unittest.mock import Mock
from aiohttp.client_proto import ResponseHandler
from aiohttp.client_reqrep import ConnectionKey
from aiohttp.connector import BaseConnector, Connection

@pytest.fixture
def mock_connector():
    return Mock(spec=BaseConnector)

@pytest.fixture
def mock_protocol():
    return Mock(spec=ResponseHandler)

@pytest.fixture
def mock_key():
    return Mock(spec=ConnectionKey)

@pytest.fixture
def event_loop():
    return asyncio.new_event_loop()

def test_close_connection(mock_connector, mock_key, mock_protocol, event_loop):
    conn = Connection(mock_connector, mock_key, mock_protocol, event_loop)
    conn.close()
    assert conn._closed is True  # Assuming _closed is an attribute that indicates if the connection is closed

def test_close_multiple_times(mock_connector, mock_key, mock_protocol, event_loop):
    conn = Connection(mock_connector, mock_key, mock_protocol, event_loop)
    conn.close()
    conn.close()  # Closing again should not raise an error
    assert conn._closed is True

def test_close_with_active_requests(mock_connector, mock_key, mock_protocol, event_loop):
    conn = Connection(mock_connector, mock_key, mock_protocol, event_loop)
    conn._active_requests = [Mock()]  # Simulating active requests
    conn.close()
    assert conn._closed is True
    assert len(conn._active_requests) == 0  # Assuming it clears active requests on close

def test_close_with_gc(mock_connector, mock_key, mock_protocol, event_loop):
    conn = Connection(mock_connector, mock_key, mock_protocol, event_loop)
    conn.close()
    del conn
    gc.collect()  # Ensure that the connection is cleaned up properly after close
    assert gc.garbage == []  # Assuming no garbage collection issues after closing