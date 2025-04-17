import asyncio
import socket
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
async def unused_port_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    yield sock
    sock.close()

async def dummy_task():
    await asyncio.sleep(0.1)

async def extra_test_function(session: ClientSession):
    response = await session.get('http://127.0.0.1:8080/')
    assert response.status == 200

@pytest.mark.asyncio
async def test_run_app_with_extra_test(unused_port_socket):
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    t, num_connections = await run_app(sock, timeout, task, extra_test_function)

    assert t is not None
    assert num_connections >= 0

@pytest.mark.asyncio
async def test_run_app_timeout_handling(unused_port_socket):
    sock = unused_port_socket
    timeout = 1
    task = dummy_task

    with pytest.raises(asyncio.TimeoutError):
        await run_app(sock, timeout, task, extra_test_function)

@pytest.mark.asyncio
async def test_run_app_connection_limit(unused_port_socket):
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    t, num_connections = await run_app(sock, timeout, task)

    assert num_connections == 0  # Assuming no connections were made during the test

@pytest.mark.asyncio
async def test_run_app_with_client_connector_error(unused_port_socket):
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    async def faulty_extra_test(session: ClientSession):
        with pytest.raises(ClientConnectorError):
            await session.get('http://127.0.0.1:9999/')  # Invalid port to trigger error

    await run_app(sock, timeout, task, faulty_extra_test)