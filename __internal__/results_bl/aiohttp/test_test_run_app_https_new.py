import asyncio
import socket
import ssl
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

async def extra_test_function(session):
    response = await session.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_extra_test(patched_loop):
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 5

    app = web.Application()

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.PropertyMock) as mock_server:
        result = run_app(sock, timeout, mock_task, extra_test=extra_test_function)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], asyncio.Task)
        assert isinstance(result[1], int)

def test_run_app_timeout(patched_loop):
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 0.1

    app = web.Application()

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.PropertyMock):
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, mock_task)

def test_run_app_connection_error(patched_loop):
    sock = socket.socket()
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 5

    app = web.Application()

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.PropertyMock):
        with pytest.raises(ClientConnectorError):
            run_app(sock, timeout, mock_task)