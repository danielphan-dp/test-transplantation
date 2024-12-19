import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def patched_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

async def mock_task():
    await asyncio.sleep(0.1)

async def extra_test(sess):
    response = await sess.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_extra_test(patched_loop):
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    timeout = 5

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        result = run_app(sock, timeout, mock_task, extra_test)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], asyncio.Task)
        assert isinstance(result[1], int)

    assert patched_loop.is_closed()

def test_run_app_timeout(patched_loop):
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    timeout = 0.1

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, mock_task)

    assert patched_loop.is_closed()

def test_run_app_connection_error(patched_loop):
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    timeout = 5

    async def failing_task():
        raise ClientConnectorError

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        with pytest.raises(ClientConnectorError):
            run_app(sock, timeout, failing_task)

    assert patched_loop.is_closed()