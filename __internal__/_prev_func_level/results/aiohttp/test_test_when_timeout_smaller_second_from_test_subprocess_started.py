import asyncio
import pytest
from unittest.mock import MagicMock
from aiohttp import ClientSession

@pytest.fixture
def session():
    return ClientSession()

def test_close_session_not_closed(session):
    assert not session.closed
    session.close()
    assert session.closed

def test_close_session_already_closed(session):
    session.close()
    assert session.closed
    with pytest.raises(RuntimeError):
        session.close()

def test_close_session_multiple_calls(session):
    session.close()
    session.close()  # Should not raise an error

def test_close_session_with_mock():
    mock_session = MagicMock(spec=ClientSession)
    mock_session.closed = False
    mock_session.close()
    assert mock_session.closed is True
    mock_session.close.assert_called_once()