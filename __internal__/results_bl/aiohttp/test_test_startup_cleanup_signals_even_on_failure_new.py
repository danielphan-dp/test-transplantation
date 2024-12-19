import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def patched_loop(mocker: pytest_mock.MockerFixture):
    return mocker.patch('asyncio.get_event_loop', return_value=asyncio.new_event_loop())

async def mock_task():
    await asyncio.sleep(0.1)

async def extra_test(sess: ClientSession):
    response = await sess.get('http://127.0.0.1:8080/test')
    assert response.status == 200

def test_run_app_with_extra_test(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    timeout = 1
    app = web.Application()
    
    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        task, num_connections = run_app(sock, timeout, mock_task, extra_test)
    
    assert num_connections >= 0
    assert task is not None

def test_run_app_with_timeout_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    timeout = 0.1
    app = web.Application()
    
    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, mock_task)

def test_run_app_with_client_connector_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    timeout = 1
    app = web.Application()
    
    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        with mock.patch('aiohttp.ClientSession.get', side_effect=ClientConnectorError):
            task, num_connections = run_app(sock, timeout, mock_task)
    
    assert num_connections == -1
    assert task is not None

def test_run_app_with_no_connections(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    timeout = 1
    app = web.Application()
    
    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.Mock):
        task, num_connections = run_app(sock, timeout, mock_task)
    
    assert num_connections == 0
    assert task is not None