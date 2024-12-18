import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def unused_port_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    yield sock
    sock.close()

async def dummy_task() -> None:
    await asyncio.sleep(0.1)

async def extra_test_function(session: ClientSession) -> None:
    response = await session.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 1

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task = dummy_task
        t, num_connections = run_app(sock, timeout, task, extra_test=extra_test_function)

        assert t is not None
        assert num_connections >= 0
        mock_server.assert_called_once()

def test_run_app_timeout(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 0.1

    async def failing_task() -> None:
        await asyncio.sleep(0.5)

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, failing_task)

        mock_server.assert_called_once()