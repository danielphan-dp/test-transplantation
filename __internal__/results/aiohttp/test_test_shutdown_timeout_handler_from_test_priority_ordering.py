import asyncio
import socket
import pytest
from aiohttp import ClientSession, ClientTimeout, web

class TestShutdown:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    async def task_with_error(self) -> None:
        await asyncio.sleep(1)
        raise Exception("Task failed")

    async def task_with_delay(self) -> None:
        await asyncio.sleep(2)

    def run_app(self, sock: socket.socket, timeout: int, task: Callable[[], Coroutine[None, None, None]], extra_test: Optional[Callable[[ClientSession], Awaitable[None]]] = None) -> Tuple['asyncio.Task[None]', int]:
        # Implementation as provided in the original method
        ...

    async def test_run_app_with_error(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        t, connection_count = self.run_app(sock, 1, self.task_with_error)

        assert t.done()
        assert t.exception() is not None
        assert connection_count == 1

    async def test_run_app_with_delay(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        t, connection_count = self.run_app(sock, 1, self.task_with_delay)

        assert finished is False
        assert t.done()
        assert t.cancelled()
        assert connection_count == 1

    async def test_run_app_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket

        async def long_task() -> None:
            await asyncio.sleep(5)

        with pytest.raises(asyncio.TimeoutError):
            self.run_app(sock, 1, long_task)