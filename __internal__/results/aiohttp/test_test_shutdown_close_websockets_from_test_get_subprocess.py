import asyncio
import contextlib
import socket
import time
import pytest
from aiohttp import web

class TestCloseMethod:
    async def test_close_method_not_called_twice(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        app = web.Application()
        closed = False

        async def close_handler(request: web.Request) -> web.Response:
            nonlocal closed
            closed = True
            return web.Response(text="Closed")

        app.router.add_get("/close", close_handler)

        async with web.AppRunner(app) as runner:
            await runner.setup()
            site = web.TCPSite(runner, '127.0.0.1', port)
            await site.start()

            start = time.time()
            async with asyncio.ClientSession() as sess:
                await sess.get(f"http://127.0.0.1:{port}/close")
            
            assert time.time() - start < 5
            assert closed

    async def test_close_method_with_no_active_connections(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        app = web.Application()
        closed = False

        async def close_handler(request: web.Request) -> web.Response:
            nonlocal closed
            closed = True
            return web.Response(text="Closed")

        app.router.add_get("/close", close_handler)

        async with web.AppRunner(app) as runner:
            await runner.setup()
            site = web.TCPSite(runner, '127.0.0.1', port)
            await site.start()

            start = time.time()
            async with asyncio.ClientSession() as sess:
                await sess.get(f"http://127.0.0.1:{port}/close")
            
            assert time.time() - start < 5
            assert closed

    async def test_close_method_with_active_connections(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        app = web.Application()
        connections_closed = 0

        async def close_handler(request: web.Request) -> web.Response:
            nonlocal connections_closed
            connections_closed += 1
            return web.Response(text="Closed")

        app.router.add_get("/close", close_handler)

        async with web.AppRunner(app) as runner:
            await runner.setup()
            site = web.TCPSite(runner, '127.0.0.1', port)
            await site.start()

            async with asyncio.ClientSession() as sess:
                await asyncio.gather(
                    sess.get(f"http://127.0.0.1:{port}/close"),
                    sess.get(f"http://127.0.0.1:{port}/close")
                )
            
            assert connections_closed == 2

    async def test_close_method_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        app = web.Application()
        closed = False

        async def close_handler(request: web.Request) -> web.Response:
            await asyncio.sleep(2)  # Simulate delay
            nonlocal closed
            closed = True
            return web.Response(text="Closed")

        app.router.add_get("/close", close_handler)

        async with web.AppRunner(app) as runner:
            await runner.setup()
            site = web.TCPSite(runner, '127.0.0.1', port)
            await site.start()

            start = time.time()
            async with asyncio.ClientSession() as sess:
                await sess.get(f"http://127.0.0.1:{port}/close")
            
            assert time.time() - start >= 2
            assert closed