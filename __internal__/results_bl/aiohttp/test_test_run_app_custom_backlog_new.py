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

def test_run_app_with_timeout(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 0.5

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        task, num_connections = run_app(sock, timeout, mock_task, extra_test)

    assert num_connections >= 0
    assert task is not None
    assert task.done()
    assert task.exception() is None

def test_run_app_with_client_connector_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 0.5

    async def failing_task():
        raise ClientConnectorError

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        with pytest.raises(ClientConnectorError):
            run_app(sock, timeout, failing_task)

def test_run_app_with_no_extra_test(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 0.5

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        task, num_connections = run_app(sock, timeout, mock_task)

    assert num_connections >= 0
    assert task is not None
    assert task.done()
    assert task.exception() is None