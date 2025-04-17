import os
import sys
import pytest
from unittest import mock
from aiohttp import ClientResponse, ClientSession
from aiohttp.helpers import TimerNoop
from aiohttp.web import URL
from aiohttp.test_utils import TestClient

@pytest.mark.internal
@pytest.mark.dev_mode
@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Timing is more reliable on Linux')
def test_run_with_connection(pytester):
    """Test the run method with a mocked connection."""
    loop = mock.Mock()
    session = mock.Mock(spec=ClientSession)
    conn = mock.Mock()

    response = ClientResponse(
        'get',
        URL('http://def-cl-resp.org'),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = False
    response._connection = conn

    assert response._connection is conn
    assert not response._closed

    response.close()
    assert response._closed

    # Test edge case: calling close multiple times
    response.close()
    assert response._closed

    # Test with a different connection
    new_conn = mock.Mock()
    response._connection = new_conn
    assert response._connection is new_conn

    # Ensure the response is properly closed
    response.close()
    assert response._connection is None

@pytest.mark.internal
@pytest.mark.dev_mode
@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Timing is more reliable on Linux')
def test_run_with_invalid_connection(pytester):
    """Test the run method with an invalid connection."""
    loop = mock.Mock()
    session = mock.Mock(spec=ClientSession)
    conn = None  # Simulating an invalid connection

    with pytest.raises(TypeError):
        response = ClientResponse(
            'get',
            URL('http://def-cl-resp.org'),
            request_info=mock.Mock(),
            writer=mock.Mock(),
            continue100=None,
            timer=TimerNoop(),
            traces=[],
            loop=loop,
            session=session,
        )
        response._connection = conn
        response.close()  # This should raise an error due to invalid connection

@pytest.mark.internal
@pytest.mark.dev_mode
@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Timing is more reliable on Linux')
def test_run_with_closed_response(pytester):
    """Test the run method with a closed response."""
    loop = mock.Mock()
    session = mock.Mock(spec=ClientSession)
    conn = mock.Mock()

    response = ClientResponse(
        'get',
        URL('http://def-cl-resp.org'),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session,
    )
    response._closed = True
    response._connection = conn

    assert response._closed
    with pytest.raises(RuntimeError):
        response.close()  # Should raise an error since it's already closed