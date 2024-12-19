import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.mark.skip_if_no_unix_socks
async def test_run_app_http_unix_socket_timeout(patched_loop: asyncio.AbstractEventLoop, unix_sockname: str) -> None:
    app = web.Application()

    async def dummy_task():
        await asyncio.sleep(0.2)

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        sock = socket.socket(socket.AF_UNIX)
        sock.bind(unix_sockname)
        sock.listen()

        with pytest.raises(asyncio.TimeoutError):
            await app.run_app(sock, timeout=0.1, task=dummy_task)

        mock_server.assert_called_once()

@pytest.mark.skip_if_no_unix_socks
async def test_run_app_http_unix_socket_connection_error(patched_loop: asyncio.AbstractEventLoop, unix_sockname: str) -> None:
    app = web.Application()

    async def dummy_task():
        await asyncio.sleep(0.2)

    sock = socket.socket(socket.AF_UNIX)
    sock.bind(unix_sockname)
    sock.listen()

    with mock.patch('aiohttp.ClientSession.get', side_effect=ClientConnectorError):
        with pytest.raises(ClientConnectorError):
            await app.run_app(sock, timeout=1, task=dummy_task)

@pytest.mark.skip_if_no_unix_socks
async def test_run_app_http_unix_socket_success(patched_loop: asyncio.AbstractEventLoop, unix_sockname: str) -> None:
    app = web.Application()

    async def dummy_task():
        await asyncio.sleep(0.1)

    sock = socket.socket(socket.AF_UNIX)
    sock.bind(unix_sockname)
    sock.listen()

    async with ClientSession() as sess:
        task, num_connections = await app.run_app(sock, timeout=1, task=dummy_task)
        assert task is not None
        assert num_connections == 0  # No connections should be made yet

    await asyncio.sleep(0.2)  # Allow dummy_task to complete
    assert task.done()  # Ensure the task has completed