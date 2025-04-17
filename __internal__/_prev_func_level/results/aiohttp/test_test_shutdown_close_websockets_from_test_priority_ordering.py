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

    @pytest.mark.asyncio
    async def test_run_app_with_extra_test(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        timeout = 5
        num_connections = -1

        async def run_app(sock: socket.socket, timeout: int, task: Callable[[], Coroutine[None, None, None]], extra_test: Optional[Callable[[ClientSession], Awaitable[None]]]=None) -> Tuple['asyncio.Task[None]', int]:
            port = sock.getsockname()[1]
            t = asyncio.create_task(task())
            app = web.Application()
            app.router.add_get('/', lambda request: web.Response(text='FOO'))
            app.router.add_get('/stop', self.stop)
            web.run_app(app, sock=sock, shutdown_timeout=timeout)
            return t, num_connections

        t, num_connections = await run_app(sock, timeout, self.task, self.extra_test)
        assert t is not None
        assert num_connections == -1

    @pytest.mark.asyncio
    async def test_run_app_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        timeout = 1

        async def task() -> None:
            await asyncio.sleep(2)

        async def test() -> None:
            async with ClientSession() as sess:
                with pytest.raises(asyncio.TimeoutError):
                    await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/', timeout=ClientTimeout(total=0.5))

        await run_app(sock, timeout, task)
        await test()