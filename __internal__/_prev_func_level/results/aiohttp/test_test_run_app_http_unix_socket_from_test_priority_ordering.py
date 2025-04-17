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
        task = dummy_task
        run_app(sock, timeout, task, extra_test=extra_test_function)

        mock_run_app.assert_called_once()
        assert mock_run_app.call_args[0][0].router.routes[0].method == 'GET'
        assert mock_run_app.call_args[0][0].router.routes[0].path == '/'

def test_run_app_timeout_handling(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 0.1

    async def long_running_task() -> None:
        await asyncio.sleep(0.5)

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout, long_running_task)

def test_run_app_connection_count(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 1

    async def connection_task() -> None:
        await asyncio.sleep(0.1)

    task = connection_task
    _, num_connections = run_app(sock, timeout, task)

    assert num_connections == 0  # Expecting no connections after the task completes

def test_run_app_client_connector_error_handling(unused_port_socket: socket.socket) -> None:
    sock = unused_port_socket
    timeout = 1

    async def failing_task() -> None:
        raise ClientConnectorError

    with pytest.raises(ClientConnectorError):
        run_app(sock, timeout, failing_task)