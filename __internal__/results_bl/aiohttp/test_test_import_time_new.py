import os
import platform
import sys
from unittest import mock
import pytest
from aiohttp import ClientResponse, URL
from aiohttp.web import Response
from aiohttp import ClientConnectionError

@pytest.mark.internal
@pytest.mark.dev_mode
@pytest.mark.skipif(not sys.platform.startswith('linux') or platform.python_implementation() == 'PyPy', reason='Timing is more reliable on Linux')
def test_run_with_valid_connection(pytester):
    conn = mock.Mock()
    response = ClientResponse('get', URL('http://def-cl-resp.org'), request_info=mock.Mock(), writer=mock.Mock(), continue100=None, timer=mock.Mock(), traces=[], loop=mock.Mock(), session=mock.Mock())
    response._closed = False
    response._connection = conn
    assert response._connection == conn

@pytest.mark.internal
@pytest.mark.dev_mode
@pytest.mark.skipif(not sys.platform.startswith('linux') or platform.python_implementation() == 'PyPy', reason='Timing is more reliable on Linux')
def test_run_with_closed_connection(pytester):
    conn = mock.Mock()
    response = ClientResponse('get', URL('http://def-cl-resp.org'), request_info=mock.Mock(), writer=mock.Mock(), continue100=None, timer=mock.Mock(), traces=[], loop=mock.Mock(), session=mock.Mock())
    response._closed = True
    response._connection = conn
    assert response._closed is True

@pytest.mark.internal
@pytest.mark.dev_mode
@pytest.mark.skipif(not sys.platform.startswith('linux') or platform.python_implementation() == 'PyPy', reason='Timing is more reliable on Linux')
def test_run_with_connection_error(pytester):
    conn = mock.Mock(side_effect=ClientConnectionError)
    with pytest.raises(ClientConnectionError):
        response = ClientResponse('get', URL('http://def-cl-resp.org'), request_info=mock.Mock(), writer=mock.Mock(), continue100=None, timer=mock.Mock(), traces=[], loop=mock.Mock(), session=mock.Mock())
        response._connection = conn
        response._connection()  # Trigger the connection error