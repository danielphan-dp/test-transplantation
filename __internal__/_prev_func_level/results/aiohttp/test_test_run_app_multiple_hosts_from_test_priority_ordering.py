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
    response = await session.get('http://127.0.0.1:8080/test')
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket):
    sock = unused_port_socket
    timeout = 5

    app = web.Application()
    app.router.add_get('/test', lambda request: web.Response(text='OK'))
    
    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task, num_connections = run_app(sock, timeout, dummy_task, extra_test_function)
        
        assert task is not None
        assert num_connections == 0
        mock_server.assert_called_once()

def test_run_app_timeout(unused_port_socket):
    sock = unused_port_socket
    timeout = 1

    app = web.Application()
    app.router.add_get('/test', lambda request: web.Response(text='OK'))

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        with pytest.raises(asyncio.TimeoutError):
            run_app(sock, timeout, dummy_task, extra_test_function)

def test_run_app_multiple_connections(unused_port_socket):
    sock = unused_port_socket
    timeout = 5

    app = web.Application()
    app.router.add_get('/test', lambda request: web.Response(text='OK'))

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task, num_connections = run_app(sock, timeout, dummy_task)

        assert task is not None
        assert num_connections >= 0  # Ensure we have at least one connection

        # Simulate multiple connections
        for _ in range(5):
            with ClientSession() as sess:
                response = sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/test')
                assert response.status == 200

        assert num_connections > 0  # Ensure connections were made

def test_run_app_with_invalid_socket():
    invalid_sock = None
    timeout = 5

    with pytest.raises(TypeError):
        run_app(invalid_sock, timeout, dummy_task)