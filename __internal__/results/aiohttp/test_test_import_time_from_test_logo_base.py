import os
import sys
import pytest
from unittest import mock
from aiohttp import ClientResponse, ClientSession
from aiohttp.helpers import TimerNoop
from aiohttp.web import URL
from aiohttp.test_utils import make_mocked_request

@pytest.mark.internal
@pytest.mark.dev_mode
@pytest.mark.skipif(not sys.platform.startswith('linux') or platform.python_implementation() == 'PyPy', reason='Timing is more reliable on Linux')
def test_run_with_connection(pytester):
    """Test the run method with a mocked connection."""
    conn = mock.Mock()
    loop = mock.Mock()
    session = mock.Mock(spec=ClientSession)
    
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

def test_run_with_invalid_connection(pytester):
    """Test the run method with an invalid connection."""
    conn = None
    loop = mock.Mock()
    session = mock.Mock(spec=ClientSession)
    
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
        response.close()