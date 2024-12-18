import asyncio
import socket
from aiohttp import ClientSession, ClientTimeout, web
import pytest

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    def run_app(self, sock: socket.socket, timeout: int, task: Callable[[], Coroutine[None, None, None]], extra_test: Optional[Callable[[ClientSession], Awaitable[None]]] = None) -> Tuple['asyncio.Task[None]', int]:
        # Implementation as provided in the original method
        pass

    async def test_shutdown_new_conn_rejected(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(9)
            finished = True

        async def test(sess: ClientSession) -> None:
            await asyncio.sleep(1)
            with pytest.raises(ClientConnectorError):
                async with ClientSession() as new_sess:
                    async with new_sess.get(f"http://127.0.0.1:{port}/"):
                        pass
            assert finished is False

        t, connection_count = self.run_app(sock, 10, task, test)

        assert finished is True
        assert t.done()
        assert connection_count == 0

    async def test_connection_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(5)
            finished = True

        async def test(sess: ClientSession) -> None:
            await asyncio.sleep(1)
            with pytest.raises(asyncio.TimeoutError):
                async with sess.get(f"http://127.0.0.1:{port}/", timeout=ClientTimeout(total=0.1)):
                    pass
            assert finished is False

        t, connection_count = self.run_app(sock, 10, task, test)

        assert finished is True
        assert t.done()
        assert connection_count == 0

    async def test_multiple_connections(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(3)
            finished = True

        async def test(sess: ClientSession) -> None:
            await asyncio.sleep(1)
            for _ in range(3):
                async with sess.get(f"http://127.0.0.1:{port}/"):
                    pass
            assert finished is False

        t, connection_count = self.run_app(sock, 10, task, test)

        assert finished is True
        assert t.done()
        assert connection_count == 3

    async def test_server_stops_properly(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        async def test(sess: ClientSession) -> None:
            await asyncio.sleep(1)
            async with sess.get(f"http://127.0.0.1:{port}/stop"):
                pass
            assert finished is False

        t, connection_count = self.run_app(sock, 10, task, test)

        assert finished is True
        assert t.done()
        assert connection_count == 0