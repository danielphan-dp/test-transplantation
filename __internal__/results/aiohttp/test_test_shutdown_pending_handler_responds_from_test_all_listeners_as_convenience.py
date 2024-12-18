import asyncio
import socket
from aiohttp import ClientSession, ClientTimeout, web
import pytest

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    async def test_run_app_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        finished = False
        t = None

        async def test() -> None:
            async with ClientSession() as sess:
                with pytest.raises(asyncio.TimeoutError):
                    await sess.get(f"http://127.0.0.1:{port}/", timeout=ClientTimeout(total=0.1))

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal t
            t = asyncio.create_task(test())
            yield
            await t

        async def handler(request: web.Request) -> web.Response:
            nonlocal finished
            await asyncio.sleep(2)
            finished = True
            return web.Response(text="FOO")

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get("/", handler)
        app.router.add_get("/stop", self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=5)
        assert t is not None
        assert t.exception() is None
        assert finished is True

    async def test_run_app_connection_count(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        num_connections = -1
        t = None

        async def task() -> None:
            await asyncio.sleep(1)

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal t
            t = asyncio.create_task(task())
            yield
            await t

        async def handler(request: web.Request) -> web.Response:
            return web.Response(text="FOO")

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get("/", handler)
        app.router.add_get("/stop", self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=5)
        assert t is not None
        assert t.exception() is None
        assert num_connections == 0  # Expecting no connections after shutdown

    async def test_run_app_extra_test(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        finished = False
        t = None

        async def extra_test(sess: ClientSession) -> None:
            async with sess.get(f"http://127.0.0.1:{port}/") as resp:
                assert await resp.text() == "FOO"

        async def test() -> None:
            await asyncio.sleep(1)
            async with ClientSession() as sess:
                await extra_test(sess)

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal t
            t = asyncio.create_task(test())
            yield
            await t

        async def handler(request: web.Request) -> web.Response:
            nonlocal finished
            await asyncio.sleep(1)
            finished = True
            return web.Response(text="FOO")

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get("/", handler)
        app.router.add_get("/stop", self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=5)
        assert t is not None
        assert t.exception() is None
        assert finished is True