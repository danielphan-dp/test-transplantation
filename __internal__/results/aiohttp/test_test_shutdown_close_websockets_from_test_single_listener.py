import asyncio
import socket
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    async def task(self) -> None:
        await asyncio.sleep(1)

    async def extra_test(self, session: ClientSession) -> None:
        response = await session.get('http://127.0.0.1:8080/')
        assert response.status == 200

    @pytest.mark.parametrize("timeout", [0.1, 0.5])
    async def test_run_app_with_timeout(self, unused_port_socket: socket.socket, timeout: float) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        num_connections = -1
        t = None

        async def handler(request: web.Request) -> web.Response:
            nonlocal t
            t = asyncio.create_task(self.task())
            await t
            return web.Response(text='FOO')

        app = web.Application()
        app.router.add_get('/', handler)
        app.router.add_get('/stop', self.stop)

        start = time.time()
        with pytest.raises(asyncio.TimeoutError):
            await self.run_app(sock, timeout, self.task, self.extra_test)
        assert time.time() - start < 5
        assert t is not None

    async def run_app(self, sock: socket.socket, timeout: int, task: Callable[[], Coroutine[None, None, None]], extra_test: Optional[Callable[[ClientSession], Awaitable[None]]]=None) -> Tuple['asyncio.Task[None]', int]:
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
                    except ClientConnectorError:
                        await asyncio.sleep(0.5)
                    else:
                        break
                async with sess.get(f'http://127.0.0.1:{port}/stop'):
                    pass
                if extra_test:
                    await extra_test(sess)

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal test_task
            test_task = asyncio.create_task(test())
            yield
            await test_task

        app.cleanup_ctx.append(run_test)
        web.run_app(app, sock=sock, shutdown_timeout=timeout)
        assert test_task is not None
        assert test_task.exception() is None
        assert t is not None
        return (t, num_connections)