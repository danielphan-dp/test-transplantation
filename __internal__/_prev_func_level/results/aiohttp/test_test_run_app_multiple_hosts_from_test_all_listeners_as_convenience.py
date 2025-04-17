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

    with mock.patch('aiohttp.web_runner.Server'):
        t, num_connections = run_app(sock, timeout, task, extra_test=extra_test_function)

    assert t is not None
    assert num_connections >= 0

def test_run_app_timeout(unused_port_socket):
    sock = unused_port_socket
    timeout = 0.1
    task = dummy_task

    with mock.patch('aiohttp.web_runner.Server'):
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, task)

def test_run_app_multiple_connections(unused_port_socket):
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    with mock.patch('aiohttp.web_runner.Server'):
        t1, num_connections1 = run_app(sock, timeout, task)
        t2, num_connections2 = run_app(sock, timeout, task)

    assert num_connections1 == num_connections2
    assert num_connections1 >= 0
    assert t1 is not None
    assert t2 is not None

def test_run_app_with_invalid_task(unused_port_socket):
    sock = unused_port_socket
    timeout = 5
    invalid_task = None

    with mock.patch('aiohttp.web_runner.Server'):
        with pytest.raises(TypeError):
            run_app(sock, timeout, invalid_task)