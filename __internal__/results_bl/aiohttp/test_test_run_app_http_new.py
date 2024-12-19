import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def patched_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

async def mock_task():
    await asyncio.sleep(0.1)

async def extra_test(sess):
    response = await sess.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_extra_test(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)
    
    try:
        result = run_app(sock, timeout=5, task=mock_task, extra_test=extra_test)
        assert isinstance(result, tuple)
        assert isinstance(result[0], asyncio.Task)
        assert isinstance(result[1], int)
    finally:
        sock.close()

def test_run_app_timeout(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)

    async def timeout_task():
        await asyncio.sleep(2)

    with pytest.raises(asyncio.TimeoutError):
        run_app(sock, timeout=1, task=timeout_task)

    sock.close()

def test_run_app_client_connector_error(patched_loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.listen(1)

    async def failing_task():
        raise ClientConnectorError

    with pytest.raises(ClientConnectorError):
        run_app(sock, timeout=5, task=failing_task)

    sock.close()