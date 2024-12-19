import asyncio
import pytest
from unittest import mock
from aiohttp import web, ClientSession, ClientTimeout
from aiohttp.web_runner import run_app
from aiohttp.test_utils import get_unused_port_socket

@pytest.fixture
def unused_port_socket():
    sock = get_unused_port_socket()
    yield sock
    sock.close()

async def dummy_task():
    await asyncio.sleep(0.1)

async def extra_test_function(sess):
    response = await sess.get('http://127.0.0.1:{}/'.format(unused_port_socket.getsockname()[1]))
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket):
    sock = unused_port_socket
    timeout = 1
    task = dummy_task

    result_task, num_connections = run_app(sock, timeout, task, extra_test=extra_test_function)

    assert result_task is not None
    assert num_connections >= 0

def test_run_app_with_timeout_error(unused_port_socket):
    sock = unused_port_socket
    timeout = 0.1
    task = dummy_task

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout, task)

def test_run_app_with_invalid_socket():
    invalid_sock = None
    timeout = 1
    task = dummy_task

    with pytest.raises(TypeError):
        run_app(invalid_sock, timeout, task)

def test_run_app_with_no_task(unused_port_socket):
    sock = unused_port_socket
    timeout = 1

    with pytest.raises(ValueError):
        run_app(sock, timeout, None)