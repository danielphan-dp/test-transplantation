import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def patched_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

async def mock_task():
    await asyncio.sleep(0.1)

async def extra_test(sess):
    response = await sess.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_extra_test(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    timeout = 5
    app = web.Application()
    
    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task = mock.create_autospec(mock_task)
        result = run_app(sock, timeout, task, extra_test=extra_test)
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], asyncio.Task)
        assert isinstance(result[1], int)

def test_run_app_with_timeout_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    timeout = 0.1
    app = web.Application()
    
    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task = mock.create_autospec(mock_task)
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, task)

def test_run_app_with_client_connector_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    timeout = 5
    app = web.Application()
    
    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task = mock.create_autospec(mock_task)
        with mock.patch('aiohttp.ClientSession.get', side_effect=ClientConnectorError):
            result = run_app(sock, timeout, task)
            assert result is not None

def test_run_app_no_connections(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    timeout = 5
    app = web.Application()
    
    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task = mock.create_autospec(mock_task)
        result = run_app(sock, timeout, task)
        assert result[1] == 0  # No connections should be recorded