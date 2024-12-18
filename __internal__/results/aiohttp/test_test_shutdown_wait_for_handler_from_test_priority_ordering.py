import asyncio
import socket
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

class TestShutdown:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    async def task_with_error(self) -> None:
        await asyncio.sleep(1)
        raise Exception("Task failed")

    async def task_with_delay(self) -> None:
        await asyncio.sleep(2)

    def run_app(self, sock: socket.socket, timeout: int, task: Callable[[], Coroutine[None, None, None]]) -> Tuple['asyncio.Task[None]', int]:
        # Implementation as provided in the original method
        ...

    async def test_run_app_with_error(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        with pytest.raises(Exception, match="Task failed"):
            await self.run_app(sock, 3, self.task_with_error)

    async def test_run_app_with_delay(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        t, connection_count = await self.run_app(sock, 3, task)

        assert finished is True
        assert t.done()
        assert not t.cancelled()
        assert connection_count == 0

    async def test_run_app_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(5)
            finished = True

        with pytest.raises(asyncio.TimeoutError):
            await self.run_app(sock, 1, task)

    async def test_run_app_client_connector_error(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        t, connection_count = await self.run_app(sock, 3, task)

        assert finished is True
        assert t.done()
        assert not t.cancelled()
        assert connection_count == 0

        async with ClientSession() as sess:
            with pytest.raises(ClientConnectorError):
                await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/nonexistent')