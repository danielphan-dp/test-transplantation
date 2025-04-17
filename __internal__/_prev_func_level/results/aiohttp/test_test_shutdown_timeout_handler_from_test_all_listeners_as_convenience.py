import asyncio
import socket
import pytest
from aiohttp import ClientSession, ClientTimeout, web

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    def run_app(self, sock: socket.socket, timeout: int, task: Callable[[], Coroutine[None, None, None]], extra_test: Optional[Callable[[ClientSession], Awaitable[None]]] = None) -> Tuple['asyncio.Task[None]', int]:
        # Implementation as provided in the original method
        pass

    async def long_running_task(self) -> None:
        await asyncio.sleep(5)

    async def short_running_task(self) -> None:
        await asyncio.sleep(1)

    async def extra_test_function(self, session: ClientSession) -> None:
        response = await session.get('http://127.0.0.1:8080/')
        assert response.status == 200

    def test_run_app_with_long_task(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(5)
            finished = True

        t, connection_count = self.run_app(sock, 1, task)

        assert finished is False
        assert t.done()
        assert t.cancelled()
        assert connection_count == 1

    def test_run_app_with_short_task(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(1)
            finished = True

        t, connection_count = self.run_app(sock, 1, task)

        assert finished is True
        assert t.done()
        assert t.exception() is None
        assert connection_count == 1

    def test_run_app_with_extra_test(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(1)
            finished = True

        t, connection_count = self.run_app(sock, 1, task, extra_test=self.extra_test_function)

        assert finished is True
        assert t.done()
        assert t.exception() is None
        assert connection_count == 1

    def test_run_app_with_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        with pytest.raises(asyncio.TimeoutError):
            self.run_app(sock, 1, task)

    def test_run_app_with_no_connections(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket

        async def task() -> None:
            await asyncio.sleep(0.1)

        t, connection_count = self.run_app(sock, 1, task)

        assert connection_count == 0
        assert t.done()
        assert t.exception() is None