import asyncio
import socket
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError
import pytest
from unittest import mock

@pytest.mark.asyncio
async def test_run_app_with_timeout(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    async def task() -> None:
        await asyncio.sleep(0.5)

    async def extra_test(sess: ClientSession) -> None:
        response = await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/')
        assert response.status == 200
        text = await response.text()
        assert text == 'FOO'

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout, task)

    sock.close()

@pytest.mark.asyncio
async def test_run_app_with_client_connector_error(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    async def task() -> None:
        await asyncio.sleep(0.5)

    async def extra_test(sess: ClientSession) -> None:
        with pytest.raises(ClientConnectorError):
            await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/nonexistent')

    await run_app(sock, timeout, task, extra_test)

    sock.close()