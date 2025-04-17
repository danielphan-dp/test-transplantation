import asyncio
import socket
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

def test_run_app_with_extra_test(unused_port_socket):
    sock = unused_port_socket
    timeout = 5

    task = dummy_task

    t, num_connections = run_app(sock, timeout, task, extra_test=extra_test_function)

    assert t is not None
    assert num_connections >= 0

def test_run_app_with_timeout(unused_port_socket):
    sock = unused_port_socket
    timeout = 0.1

    task = dummy_task

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout, task)

def test_run_app_with_client_connector_error(unused_port_socket):
    sock = unused_port_socket
    timeout = 5

    async def failing_task():
        raise ClientConnectorError

    with pytest.raises(ClientConnectorError):
        run_app(sock, timeout, failing_task)