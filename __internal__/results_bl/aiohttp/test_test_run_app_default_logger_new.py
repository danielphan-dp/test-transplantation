import asyncio
import logging
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

def test_run_app_with_extra_test(monkeypatch, patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 5

    app = web.Application()
    task = mock_task

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        t, num_connections = run_app(sock, timeout, task, extra_test=extra_test)

    assert num_connections >= 0
    assert t is not None

def test_run_app_timeout_error(monkeypatch, patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 0.1

    app = web.Application()
    task = mock_task

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, task)

def test_run_app_no_connections(monkeypatch, patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    timeout = 5

    app = web.Application()
    task = mock_task

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        t, num_connections = run_app(sock, timeout, task)

    assert num_connections == 0
    assert t is not None