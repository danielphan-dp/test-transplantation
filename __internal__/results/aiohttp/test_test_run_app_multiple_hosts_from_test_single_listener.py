import asyncio
import socket
from aiohttp import web, ClientSession, ClientTimeout
import pytest
from unittest import mock

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

def test_run_app_with_extra_test(unused_port_socket) -> None:
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    with mock.patch('aiohttp.web.run_app') as mock_run_app:
        run_app(sock, timeout, task, extra_test=extra_test_function)
        mock_run_app.assert_called_once()

def test_run_app_timeout_handling(unused_port_socket) -> None:
    sock = unused_port_socket
    timeout = 0.1
    task = dummy_task

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout, task)

def test_run_app_multiple_connections(unused_port_socket) -> None:
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    async def connection_test() -> None:
        async with ClientSession() as session:
            for _ in range(5):
                await session.get(f'http://127.0.0.1:{sock.getsockname()[1]}/')

    run_app(sock, timeout, connection_test)