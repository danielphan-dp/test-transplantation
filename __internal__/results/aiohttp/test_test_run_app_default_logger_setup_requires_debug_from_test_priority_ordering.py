import asyncio
import logging
import socket
from typing import Callable, Coroutine, Optional, Tuple
from unittest import mock
import pytest
from aiohttp import ClientSession, ClientTimeout, web

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    async def test_run_app_with_timeout(self, patched_loop: asyncio.AbstractEventLoop) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        sock.listen(1)
        timeout = 1

        async def task():
            await asyncio.sleep(0.5)

        app = web.Application()
        app.router.add_get('/stop', self.stop)

        with mock.patch('aiohttp.web_runner.Server'):
            t, num_connections = await self.run_app(sock, timeout, task)

        assert t is not None
        assert num_connections == 0

    async def test_run_app_with_extra_test(self, patched_loop: asyncio.AbstractEventLoop) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        sock.listen(1)
        timeout = 1

        async def task():
            await asyncio.sleep(0.5)

        async def extra_test(sess: ClientSession) -> None:
            response = await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/')
            assert response.status == 200

        app = web.Application()
        app.router.add_get('/stop', self.stop)

        with mock.patch('aiohttp.web_runner.Server'):
            t, num_connections = await self.run_app(sock, timeout, task, extra_test)

        assert t is not None
        assert num_connections == 0

    async def run_app(self, sock: socket.socket, timeout: int, task: Callable[[], Coroutine[None, None, None]], extra_test: Optional[Callable[[ClientSession], Coroutine[None, None]]] = None) -> Tuple[asyncio.Task[None], int]:
        num_connections = -1
        t = test_task = None
        port = sock.getsockname()[1]

        class DictRecordClear(dict):
            def clear(self) -> None:
                nonlocal num_connections
                num_connections = len(self)
                super().clear()

        class ServerWithRecordClear(web.Server):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._connections = DictRecordClear()

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
                if extra_test:
                    await extra_test(sess)

        async def run_test(app: web.Application) -> None:
            nonlocal test_task
            test_task = asyncio.create_task(test())
            yield
            await test_task

        async def handler(request: web.Request) -> web.Response:
            nonlocal t
            t = asyncio.create_task(task())
            await t
            return web.Response(text='FOO')

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get('/', handler)
        app.router.add_get('/stop', self.stop)

        with mock.patch('aiohttp.web_runner.Server', ServerWithRecordClear):
            web.run_app(app, sock=sock, shutdown_timeout=timeout)

        assert test_task is not None
        assert test_task.exception() is None
        assert t is not None
        return (t, num_connections)