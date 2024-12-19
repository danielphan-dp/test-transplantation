import asyncio
import logging
import socket
from unittest import mock
import pytest
from aiohttp import ClientSession, ClientTimeout, web, ClientConnectorError

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

def test_run_app_with_extra_test_function(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 5

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='FOO'))
    app.router.add_get('/stop', lambda request: web.Response(text='STOP'))

    with mock.patch('aiohttp.web_runner.Server'):
        task, num_connections = run_app(sock, timeout, mock_task, extra_test=extra_test_function)

    assert num_connections == 0
    assert task is not None
    assert task.exception() is None

def test_run_app_with_timeout_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    async def failing_task():
        await asyncio.sleep(2)

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='FOO'))
    app.router.add_get('/stop', lambda request: web.Response(text='STOP'))

    with mock.patch('aiohttp.web_runner.Server'):
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, failing_task)

def test_run_app_with_client_connector_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 5

    async def task_with_connector_error():
        raise ClientConnectorError

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='FOO'))
    app.router.add_get('/stop', lambda request: web.Response(text='STOP'))

    with mock.patch('aiohttp.web_runner.Server'):
        task, num_connections = run_app(sock, timeout, task_with_connector_error)

    assert num_connections == 0
    assert task.exception() is not None
    assert isinstance(task.exception(), ClientConnectorError)