import asyncio
import socket
import pytest
from aiohttp import ClientSession, ClientTimeout, ClientConnectorError, web

class TestRunApp:
    async def test_run_app_with_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        t, connection_count = self.run_app(sock, 1, task)

        assert finished is False
        assert t.done()
        assert t.cancelled()
        assert connection_count == 1

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

        t, connection_count = self.run_app(sock, 1, task, extra_test)

        assert finished is True
        assert t.done()
        assert t.exception() is None
        assert connection_count == 1

    async def test_run_app_with_connection_error(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket

        async def task() -> None:
            await asyncio.sleep(1)

        with pytest.raises(ClientConnectorError):
            await self.run_app(sock, 1, task)

    async def test_run_app_with_zero_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        t, connection_count = self.run_app(sock, 0, task)

        assert finished is False
        assert t.done()
        assert t.cancelled()
        assert connection_count == 1

    async def test_run_app_with_multiple_connections(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        connection_count = 0

        async def task() -> None:
            nonlocal connection_count
            await asyncio.sleep(1)
            connection_count += 1

        t1, count1 = await self.run_app(sock, 1, task)
        t2, count2 = await self.run_app(sock, 1, task)

        assert count1 == 1
        assert count2 == 1
        assert t1.done()
        assert t2.done()