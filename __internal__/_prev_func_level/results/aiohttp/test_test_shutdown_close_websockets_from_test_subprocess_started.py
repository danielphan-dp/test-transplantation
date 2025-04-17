import asyncio
import contextlib
import socket
import time
import pytest
from aiohttp import web

class TestCloseMethod:
    async def test_close_method(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        app = web.Application()
        closed = False

        async def close_handler(request: web.Request) -> web.Response:
            nonlocal closed
            closed = True
            return web.Response(text="Closed")

        app.router.add_get("/close", close_handler)

        async def test_close() -> None:
            async with ClientSession() as sess:
                await sess.get(f"http://127.0.0.1:{port}/close")

        async def run_test(app: web.Application) -> None:
            t = asyncio.create_task(test_close())
            yield
            t.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await t

        app.cleanup_ctx.append(run_test)
        start = time.time()
        web.run_app(app, sock=sock, shutdown_timeout=10)
        assert time.time() - start < 5
        assert closed

    async def test_close_method_already_closed(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        app = web.Application()
        closed = True

        async def close_handler(request: web.Request) -> web.Response:
            nonlocal closed
            if closed:
                return web.Response(text="Already closed", status=400)
            closed = True
            return web.Response(text="Closed")

        app.router.add_get("/close", close_handler)

        async def test_close() -> None:
            async with ClientSession() as sess:
                response = await sess.get(f"http://127.0.0.1:{port}/close")
                assert response.status == 400

        async def run_test(app: web.Application) -> None:
            t = asyncio.create_task(test_close())
            yield
            t.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await t

        app.cleanup_ctx.append(run_test)
        start = time.time()
        web.run_app(app, sock=sock, shutdown_timeout=10)
        assert time.time() - start < 5
        assert closed