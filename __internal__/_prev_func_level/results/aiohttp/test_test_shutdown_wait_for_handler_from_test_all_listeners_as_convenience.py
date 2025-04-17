import asyncio
import socket
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    def run_app(self, sock: socket.socket, timeout: int, task: Callable[[], Coroutine[None, None, None]], extra_test: Optional[Callable[[ClientSession], Awaitable[None]]] = None) -> Tuple['asyncio.Task[None]', int]:
        # Implementation as provided in the original method
        pass

    async def test_run_app_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        with pytest.raises(asyncio.TimeoutError):
            await self.run_app(sock, 1, task)

    async def test_run_app_connection_count(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        connection_count = 0

        async def task() -> None:
            await asyncio.sleep(1)

        t, count = self.run_app(sock, 3, task)
        assert count == 0

    async def test_run_app_with_extra_test(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(1)
            finished = True

        async def extra_test(sess: ClientSession) -> None:
            response = await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/')
            assert response.status == 200

        t, connection_count = self.run_app(sock, 3, task, extra_test=extra_test)
        assert finished is True
        assert t.done()
        assert not t.cancelled()
        assert connection_count == 0

    async def test_run_app_connection_error(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket

        async def task() -> None:
            await asyncio.sleep(1)

        with pytest.raises(ClientConnectorError):
            await self.run_app(sock, 3, task)