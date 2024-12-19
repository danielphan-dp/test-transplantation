import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def patched_loop(mocker):
    return mocker.patch('asyncio.get_event_loop', return_value=asyncio.new_event_loop())

async def dummy_task():
    await asyncio.sleep(0.1)

async def extra_test_function(session):
    response = await session.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_timeout(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock) as mock_server:
        task, num_connections = run_app(sock, timeout, dummy_task, extra_test_function)
        assert num_connections >= 0
        assert task is not None
        assert task.exception() is None

def test_run_app_with_client_connector_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    async def failing_task():
        raise ClientConnectorError

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock) as mock_server:
        with pytest.raises(ClientConnectorError):
            run_app(sock, timeout, failing_task)

def test_run_app_with_no_extra_test(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock) as mock_server:
        task, num_connections = run_app(sock, timeout, dummy_task)
        assert num_connections >= 0
        assert task is not None
        assert task.exception() is None

def test_run_app_multiple_connections(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    timeout = 1

    async def multiple_connections_task():
        await asyncio.gather(*(dummy_task() for _ in range(10)))

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock) as mock_server:
        task, num_connections = run_app(sock, timeout, multiple_connections_task)
        assert num_connections == 10
        assert task is not None
        assert task.exception() is None