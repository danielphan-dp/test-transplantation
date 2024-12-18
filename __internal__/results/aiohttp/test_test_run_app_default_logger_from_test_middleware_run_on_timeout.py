import asyncio
import logging
import socket
from typing import Callable, Coroutine, Optional, Tuple
from unittest import mock
import pytest
from aiohttp import ClientSession, web, ClientTimeout, ClientConnectorError

@pytest.fixture
def unused_port_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    yield sock
    sock.close()

async def dummy_task() -> None:
    await asyncio.sleep(0.1)

async def extra_test_function(session: ClientSession) -> None:
    response = await session.get('http://127.0.0.1:0/')
    assert response.status == 200

def test_run_app_with_timeout_handling(unused_port_socket) -> None:
    sock = unused_port_socket
    timeout = 0.2

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task = dummy_task
        result_task, num_connections = run_app(sock, timeout, task, extra_test_function)

        assert result_task is not None
        assert num_connections >= 0

        with pytest.raises(asyncio.TimeoutError):
            async with ClientSession() as sess:
                await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/', timeout=ClientTimeout(total=0.1))

        mock_server.assert_called_once()

def test_run_app_with_connection_error(unused_port_socket) -> None:
    sock = unused_port_socket
    timeout = 0.2

    async def failing_task() -> None:
        raise ClientConnectorError

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        with pytest.raises(ClientConnectorError):
            run_app(sock, timeout, failing_task)

        mock_server.assert_called_once()