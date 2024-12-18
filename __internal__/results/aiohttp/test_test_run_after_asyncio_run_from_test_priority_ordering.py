import asyncio
import socket
from typing import Callable, Coroutine, Optional, Tuple
import pytest
from aiohttp import web, ClientSession, ClientTimeout
from unittest import mock

class TestRunApp:
    async def dummy_task(self) -> None:
        await asyncio.sleep(0.1)

    async def extra_test(self, session: ClientSession) -> None:
        response = await session.get('http://127.0.0.1:8080/')
        assert response.status == 200

    @pytest.fixture
    def unused_port_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        yield sock
        sock.close()

    def test_run_app_with_extra_test(self, unused_port_socket) -> None:
        sock = unused_port_socket
        timeout = 5

        async def stop_handler(request: web.Request) -> web.Response:
            return web.Response(text='Stopped')

        app = web.Application()
        app.router.add_get('/stop', stop_handler)

        with mock.patch('aiohttp.web_runner.Server'):
            task, num_connections = web.run_app(app, sock=sock, shutdown_timeout=timeout)

        assert task is not None
        assert num_connections == 0

    def test_run_app_timeout(self, unused_port_socket) -> None:
        sock = unused_port_socket
        timeout = 1

        async def long_running_task() -> None:
            await asyncio.sleep(2)

        app = web.Application()
        app.router.add_get('/', lambda request: web.Response(text='FOO'))

        with mock.patch('aiohttp.web_runner.Server'):
            with pytest.raises(asyncio.TimeoutError):
                web.run_app(app, sock=sock, shutdown_timeout=timeout)

    def test_run_app_no_connections(self, unused_port_socket) -> None:
        sock = unused_port_socket
        timeout = 5

        async def immediate_task() -> None:
            return

        app = web.Application()
        app.router.add_get('/', lambda request: web.Response(text='FOO'))

        with mock.patch('aiohttp.web_runner.Server'):
            task, num_connections = web.run_app(app, sock=sock, shutdown_timeout=timeout)

        assert task is not None
        assert num_connections == 0

    def test_run_app_with_client_timeout(self, unused_port_socket) -> None:
        sock = unused_port_socket
        timeout = 1

        async def delayed_task() -> None:
            await asyncio.sleep(2)

        app = web.Application()
        app.router.add_get('/', lambda request: web.Response(text='FOO'))

        with mock.patch('aiohttp.web_runner.Server'):
            async with ClientSession() as session:
                with pytest.raises(asyncio.TimeoutError):
                    await session.get(f'http://127.0.0.1:{sock.getsockname()[1]}/', timeout=ClientTimeout(total=0.5))