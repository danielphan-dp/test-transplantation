import asyncio
import contextlib
import socket
from aiohttp import ClientSession, ClientTimeout, web
import pytest

class TestRunApp:
    async def extra_test(self, sess: ClientSession) -> None:
        response = await sess.get('http://127.0.0.1:8080/')
        assert response.status == 200
        text = await response.text()
        assert text == 'FOO'

    def test_run_app_with_extra_test(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        t = None

        async def task() -> None:
            await asyncio.sleep(1)

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal t
            t = asyncio.create_task(self.extra_test(sess))
            yield
            t.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await t

        async def handler(request: web.Request) -> web.Response:
            nonlocal t
            t = asyncio.create_task(task())
            await t
            return web.Response(text='FOO')

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get('/', handler)
        app.router.add_get('/stop', self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=10)
        assert t is not None
        assert t.cancelled()

    def test_run_app_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        t = None

        async def task() -> None:
            await asyncio.sleep(2)

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal t
            t = asyncio.create_task(task())
            yield
            t.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await t

        async def handler(request: web.Request) -> web.Response:
            nonlocal t
            t = asyncio.create_task(task())
            await t
            return web.Response(text='FOO')

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get('/', handler)
        app.router.add_get('/stop', self.stop)

        with pytest.raises(asyncio.TimeoutError):
            web.run_app(app, sock=sock, shutdown_timeout=0.1)

    def test_run_app_connection_error(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        t = None

        async def task() -> None:
            await asyncio.sleep(1)

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal t
            t = asyncio.create_task(task())
            yield
            t.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await t

        async def handler(request: web.Request) -> web.Response:
            nonlocal t
            t = asyncio.create_task(task())
            await t
            return web.Response(text='FOO')

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get('/', handler)
        app.router.add_get('/stop', self.stop)

        with pytest.raises(ClientConnectorError):
            async with ClientSession() as sess:
                await sess.get(f'http://127.0.0.1:{port}/nonexistent')