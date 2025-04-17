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
    await asyncio.sleep(1)

async def extra_test_function(session: ClientSession) -> None:
    response = await session.get('http://127.0.0.1:8080/some_endpoint')
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 5

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task = asyncio.create_task(dummy_task())
        result_task, num_connections = run_app(sock, timeout, task, extra_test_function)

        assert result_task is not None
        assert num_connections >= 0
        assert result_task.exception() is None

        mock_server.assert_called_once()

def test_run_app_timeout_handling(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 1

    async def timeout_task() -> None:
        await asyncio.sleep(2)

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, timeout_task)

        mock_server.assert_called_once()