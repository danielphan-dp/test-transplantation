import asyncio
import socket
from unittest import mock
import pytest
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
    response = await session.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_timeout(unused_port_socket):
    sock = unused_port_socket
    timeout = 1

    with mock.patch('aiohttp.web.run_app') as mock_run_app:
        result = run_app(sock, timeout, dummy_task, extra_test_function)
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2

        task, num_connections = result
        assert isinstance(task, asyncio.Task)
        assert num_connections >= 0

def test_run_app_with_client_connector_error(unused_port_socket):
    sock = unused_port_socket
    timeout = 1

    async def failing_task():
        raise ClientConnectorError

    with mock.patch('aiohttp.web.run_app') as mock_run_app:
        with pytest.raises(ClientConnectorError):
            run_app(sock, timeout, failing_task)

def test_run_app_with_no_connections(unused_port_socket):
    sock = unused_port_socket
    timeout = 1

    async def task_with_no_connections():
        await asyncio.sleep(0.1)

    result = run_app(sock, timeout, task_with_no_connections)
    assert result[1] == 0  # Expecting no connections to be made

def test_run_app_with_extra_test(unused_port_socket):
    sock = unused_port_socket
    timeout = 1

    result = run_app(sock, timeout, dummy_task, extra_test_function)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[1] >= 0  # Ensure connections are counted

def test_run_app_with_timeout_error(unused_port_socket):
    sock = unused_port_socket
    timeout = 0.1

    async def long_running_task():
        await asyncio.sleep(0.5)

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout, long_running_task)