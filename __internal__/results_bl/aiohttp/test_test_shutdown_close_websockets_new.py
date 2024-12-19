import asyncio
import contextlib
import socket
import time
import unittest
from aiohttp import web

class TestWebAppCloseMethod(unittest.TestCase):

    async def ws_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    async def close_websockets(self, app):
        for ws in app['ws']:
            await ws.close()

    async def run_test(self, app):
        async with web.ClientSession() as sess:
            async with sess.ws_connect("http://127.0.0.1:8080/ws") as ws:
                await sess.get("http://127.0.0.1:8080/stop")
                await ws.receive()

    def test_close_method(self):
        sock = socket.socket()
        app = web.Application()
        app['ws'] = set()
        app.router.add_get("/ws", self.ws_handler)
        app.on_shutdown.append(self.close_websockets)

        start = time.time()
        web.run_app(app, sock=sock, shutdown_timeout=10)
        assert time.time() - start < 5

    def test_close_websockets_no_connections(self):
        sock = socket.socket()
        app = web.Application()
        app['ws'] = set()
        app.on_shutdown.append(self.close_websockets)

        start = time.time()
        web.run_app(app, sock=sock, shutdown_timeout=10)
        assert time.time() - start < 5

    def test_close_websockets_with_connections(self):
        sock = socket.socket()
        app = web.Application()
        app['ws'] = set()
        app.router.add_get("/ws", self.ws_handler)
        app.on_shutdown.append(self.close_websockets)

        async def simulate_connection():
            async with web.ClientSession() as sess:
                async with sess.ws_connect("http://127.0.0.1:8080/ws") as ws:
                    await ws.send_str("Hello")
                    await ws.close()

        asyncio.run(simulate_connection())

        start = time.time()
        web.run_app(app, sock=sock, shutdown_timeout=10)
        assert time.time() - start < 5

    def test_close_method_with_error(self):
        sock = socket.socket()
        app = web.Application()
        app['ws'] = set()
        app.router.add_get("/ws", self.ws_handler)
        app.on_shutdown.append(self.close_websockets)

        async def simulate_error():
            raise Exception("Simulated error")

        with self.assertRaises(Exception):
            asyncio.run(simulate_error())

        start = time.time()
        web.run_app(app, sock=sock, shutdown_timeout=10)
        assert time.time() - start < 5