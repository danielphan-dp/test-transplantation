import asyncio
import socket
from aiohttp import ClientSession, ClientConnectorError, ClientTimeout, web
import pytest

def test_run_app_connection_timeout(self, unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    port = sock.getsockname()[1]
    finished = False

    async def task() -> None:
        nonlocal finished
        await asyncio.sleep(5)
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

def test_run_app_no_connections(self, unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    port = sock.getsockname()[1]

    async def task() -> None:
        await asyncio.sleep(1)

    async def test(sess: ClientSession) -> None:
        await asyncio.sleep(0.5)
        async with sess.get(f"http://127.0.0.1:{port}/stop"):
            pass

    t, connection_count = self.run_app(sock, 10, task, test)

    assert t.done()
    assert connection_count == 0

def test_run_app_multiple_connections(self, unused_port_socket: socket.socket) -> None:
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