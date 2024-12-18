import asyncio
import logging
import socket
from typing import Callable, Coroutine, Optional, Tuple
from unittest import mock
import pytest
from aiohttp import ClientSession, ClientTimeout, web

@pytest.fixture
def unused_port_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    yield sock
    sock.close()

async def sample_task() -> None:
    await asyncio.sleep(0.1)

async def extra_test_function(session: ClientSession) -> None:
    response = await session.get('http://127.0.0.1:0/')
    assert response.status == 200

@pytest.mark.asyncio
async def test_run_app_with_extra_test(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 5
    num_connections = -1
    t = None

    async def handler(request: web.Request) -> web.Response:
        nonlocal t
        t = asyncio.create_task(sample_task())
        await t
        return web.Response(text='FOO')

    app = web.Application()
    app.router.add_get('/', handler)
    app.router.add_get('/stop', lambda request: web.Response())

    with mock.patch('aiohttp.web_runner.Server'):
        await asyncio.get_event_loop().run_in_executor(None, lambda: web.run_app(app, sock=sock, shutdown_timeout=timeout))

    async with ClientSession() as sess:
        await extra_test_function(sess)

    assert t is not None
    assert t.exception() is None
    assert num_connections == -1  # Adjust based on expected behavior