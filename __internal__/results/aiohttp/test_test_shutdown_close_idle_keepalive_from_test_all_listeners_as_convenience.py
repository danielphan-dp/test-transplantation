import asyncio
import contextlib
import socket
import pytest
from aiohttp import ClientSession, ClientTimeout, web

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    async def task(self) -> None:
        await asyncio.sleep(1)

    async def extra_test(self, session: ClientSession) -> None:
        response = await session.get("http://127.0.0.1:8080/")
        assert response.status == 200

    async def run_app(self, sock: socket.socket, timeout: int) -> None:
        num_connections = -1
        t = test_task = None
        port = sock.getsockname()[1]

        async def test() -> None:
            await asyncio.sleep(0.5)
            async with ClientSession() as sess:
                for _ in range(5):
                    try:
                        with pytest.raises(asyncio.TimeoutError):
                            async with sess.get(f'http://127.0.0.1:{port}/', timeout=ClientTimeout(total=0.1)):
                                pass
                    except Exception:
                        await asyncio.sleep(0.5)
                    else:
                        break
                async with sess.get(f'http://127.0.0.1:{port}/stop'):
                    pass
                await self.extra_test(sess)

        async def run_test(app: web.Application) -> None:
            nonlocal test_task
            test_task = asyncio.create_task(test())
            yield
            await test_task

        async def handler(request: web.Request) -> web.Response:
            nonlocal t
            t = asyncio.create_task(self.task())
            await t
            return web.Response(text='FOO')

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get('/', handler)
        app.router.add_get('/stop', self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=timeout)
        assert test_task is not None
        assert test_task.exception() is None
        assert t is not None

    @pytest.mark.asyncio
    async def test_run_app_with_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        await self.run_app(sock, timeout=10)

    @pytest.mark.asyncio
    async def test_run_app_with_extra_test(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        await self.run_app(sock, timeout=10)