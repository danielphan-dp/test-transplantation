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

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        task = asyncio.create_task(dummy_task())
        result_task, num_connections = run_app(sock, timeout, task, extra_test_function)

        assert result_task is not None
        assert num_connections >= 0
        assert result_task.exception() is None

        # Test for timeout scenario
        with pytest.raises(asyncio.TimeoutError):
            async with ClientSession() as sess:
                await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/', timeout=0.1)

        # Ensure the server was called
        mock_server.assert_called_once()