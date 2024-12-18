import asyncio
import pytest
from unittest.mock import MagicMock
from aiohttp import ClientSession

@pytest.fixture
def mock_session():
    return MagicMock(spec=ClientSession)

def test_close_method_closes_session(mock_session):
    mock_session.close = MagicMock()
    mock_session.close()
    mock_session.close.assert_called_once()

def test_close_method_when_already_closed(mock_session):
    mock_session.closed = True
    mock_session.close()
    assert mock_session.close.call_count == 0

def test_close_method_with_active_connections(mock_session):
    mock_session.closed = False
    mock_session._conns = {'conn1': MagicMock(), 'conn2': MagicMock()}
    mock_session.close()
    for conn in mock_session._conns.values():
        conn.close.assert_called_once()