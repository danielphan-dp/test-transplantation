import asyncio
import socket
from aiohttp import web, ClientSession, ClientTimeout
import pytest
from unittest import mock

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

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        result_task, num_connections = run_app(sock, timeout, task, extra_test_function)

    assert result_task is not None
    assert num_connections >= 0
    assert mock_server.call_count == 1

def test_run_app_timeout(unused_port_socket):
    sock = unused_port_socket
    timeout = 0.1
    task = dummy_task

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, task)

    assert mock_server.call_count == 1

def test_run_app_no_extra_test(unused_port_socket):
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        result_task, num_connections = run_app(sock, timeout, task)

    assert result_task is not None
    assert num_connections >= 0
    assert mock_server.call_count == 1

def test_run_app_with_multiple_connections(unused_port_socket):
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        for _ in range(10):
            run_app(sock, timeout, task)

    assert mock_server.call_count == 10