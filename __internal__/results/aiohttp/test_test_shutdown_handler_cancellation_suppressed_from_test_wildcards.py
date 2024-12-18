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
        actions = []
        t = None

        async def test() -> None:
            async def test_resp(sess: ClientSession) -> None:
                with pytest.raises(asyncio.TimeoutError):
                    async with sess.get(f"http://127.0.0.1:{port}/", timeout=ClientTimeout(total=0.1)) as resp:
                        assert await resp.text() == "FOO"
                actions.append("TIMEOUT")

            async with ClientSession() as sess:
                t = asyncio.create_task(test_resp(sess))
                await asyncio.sleep(0.5)
                actions.append("PRESTOP")
                async with sess.get(f"http://127.0.0.1:{port}/stop"):
                    pass
                actions.append("STOPPING")
                await t

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal t
            t = asyncio.create_task(test())
            yield
            await t

        async def handler(request: web.Request) -> web.Response:
            await asyncio.sleep(5)
            return web.Response(text="FOO")

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get("/", handler)
        app.router.add_get("/stop", self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=2)
        assert t is not None
        assert t.exception() is None
        assert actions == ["TIMEOUT", "PRESTOP", "STOPPING"]

    async def test_run_app_success(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        actions = []
        t = None

        async def test() -> None:
            async def test_resp(sess: ClientSession) -> None:
                async with sess.get(f"http://127.0.0.1:{port}/") as resp:
                    assert await resp.text() == "FOO"
                actions.append("SUCCESS")

            async with ClientSession() as sess:
                t = asyncio.create_task(test_resp(sess))
                await asyncio.sleep(0.5)
                actions.append("PRESTOP")
                async with sess.get(f"http://127.0.0.1:{port}/stop"):
                    pass
                actions.append("STOPPING")
                await t

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal t
            t = asyncio.create_task(test())
            yield
            await t

        async def handler(request: web.Request) -> web.Response:
            return web.Response(text="FOO")

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get("/", handler)
        app.router.add_get("/stop", self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=2)
        assert t is not None
        assert t.exception() is None
        assert actions == ["SUCCESS", "PRESTOP", "STOPPING"]