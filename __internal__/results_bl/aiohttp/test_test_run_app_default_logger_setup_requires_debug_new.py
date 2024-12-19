import asyncio
import logging
import socket
from unittest import mock
import pytest
from aiohttp import ClientSession, ClientTimeout, web, ClientConnectorError

@pytest.mark.asyncio
async def test_run_app_with_timeout(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    async def dummy_task() -> None:
        await asyncio.sleep(0.5)

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='Hello, World!'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopped'))

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task, num_connections = await run_app(sock, timeout, dummy_task)

    assert num_connections == 0
    assert task is not None
    assert task.done()
    assert task.exception() is None

@pytest.mark.asyncio
async def test_run_app_with_client_timeout(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    async def dummy_task() -> None:
        await asyncio.sleep(0.5)

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='Hello, World!'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopped'))

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task, num_connections = await run_app(sock, timeout, dummy_task)

    async with ClientSession() as sess:
        with pytest.raises(asyncio.TimeoutError):
            await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/', timeout=0.1)

@pytest.mark.asyncio
async def test_run_app_with_extra_test(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    async def dummy_task() -> None:
        await asyncio.sleep(0.5)

    async def extra_test(sess: ClientSession) -> None:
        response = await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/')
        assert response.status == 200
        text = await response.text()
        assert text == 'Hello, World!'

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='Hello, World!'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopped'))

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task, num_connections = await run_app(sock, timeout, dummy_task, extra_test)

    assert num_connections == 0
    assert task is not None
    assert task.done()
    assert task.exception() is None