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

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        t, num_connections = run_app(sock, timeout, task, extra_test=extra_test_function)

    assert t is not None
    assert num_connections >= 0

def test_run_app_timeout_handling(unused_port_socket):
    sock = unused_port_socket
    timeout = 0.1
    task = dummy_task

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, task)

def test_run_app_no_connections(unused_port_socket):
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        t, num_connections = run_app(sock, timeout, task)

    assert num_connections == 0

def test_run_app_with_client_timeout(unused_port_socket):
    sock = unused_port_socket
    timeout = 0.1
    task = dummy_task

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, task)