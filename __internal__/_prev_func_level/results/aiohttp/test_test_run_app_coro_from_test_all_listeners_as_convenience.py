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

    with mock.patch('aiohttp.web.run_app') as mock_run_app:
        result = run_app(sock, timeout, dummy_task, extra_test_function)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], asyncio.Task)
        assert isinstance(result[1], int)

        mock_run_app.assert_called_once()

def test_run_app_timeout_handling(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 0.1

    async def failing_task() -> None:
        await asyncio.sleep(0.5)

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout, failing_task)

def test_run_app_connection_count(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 1

    async def connection_task() -> None:
        await asyncio.sleep(0.1)

    task, num_connections = run_app(sock, timeout, connection_task)
    assert num_connections == 0

    async def additional_connection_task() -> None:
        await asyncio.sleep(0.1)

    task, num_connections = run_app(sock, timeout, additional_connection_task)
    assert num_connections == 0

def test_run_app_with_client_connector_error(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 1

    async def error_task() -> None:
        raise ClientConnectorError

    with pytest.raises(ClientConnectorError):
        run_app(sock, timeout, error_task)