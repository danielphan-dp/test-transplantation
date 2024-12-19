import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def patched_loop(mocker):
    return mocker.patch('asyncio.get_event_loop', return_value=asyncio.new_event_loop())

async def mock_task():
    await asyncio.sleep(0.1)

async def extra_test(sess):
    response = await sess.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_extra_test(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='FOO'))
    app.router.add_get('/stop', lambda request: web.Response(text='STOP'))

    task, num_connections = run_app(sock, timeout=5, task=mock_task, extra_test=extra_test)

    assert num_connections == 0
    assert task is not None
    assert task.exception() is None

def test_run_app_timeout(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)

    async def timeout_task():
        await asyncio.sleep(2)

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout=1, task=timeout_task)

def test_run_app_no_connections(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)

    task, num_connections = run_app(sock, timeout=5, task=mock_task)

    assert num_connections == 0
    assert task is not None
    assert task.exception() is None

def test_run_app_with_client_connector_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)

    async def failing_task():
        raise ClientConnectorError

    with pytest.raises(ClientConnectorError):
        run_app(sock, timeout=5, task=failing_task)