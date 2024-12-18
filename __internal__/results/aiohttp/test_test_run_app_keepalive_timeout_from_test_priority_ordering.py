import asyncio
import socket
import pytest
from unittest import mock
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def unused_port_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    yield sock
    sock.close()

async def dummy_task():
    await asyncio.sleep(0.1)

async def extra_test_function(session: ClientSession):
    response = await session.get('http://127.0.0.1:8080/test')
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket, monkeypatch):
    sock = unused_port_socket
    timeout = 5

    with mock.patch('aiohttp.web.run_app') as mock_run_app:
        mock_run_app.return_value = None

        result_task, num_connections = run_app(sock, timeout, dummy_task, extra_test_function)

        assert result_task is not None
        assert num_connections >= 0
        mock_run_app.assert_called_once()

def test_run_app_timeout_handling(unused_port_socket):
    sock = unused_port_socket
    timeout = 1

    async def failing_task():
        await asyncio.sleep(2)

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout, failing_task)

def test_run_app_connection_count(unused_port_socket):
    sock = unused_port_socket
    timeout = 5

    async def connection_task():
        await asyncio.sleep(0.1)

    result_task, num_connections = run_app(sock, timeout, connection_task)

    assert num_connections == 0  # Assuming no connections were made during the test

def test_run_app_client_connector_error_handling(unused_port_socket):
    sock = unused_port_socket
    timeout = 5

    async def error_task():
        raise ClientConnectorError

    with pytest.raises(ClientConnectorError):
        run_app(sock, timeout, error_task)