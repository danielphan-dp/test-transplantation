import asyncio
import socket
from aiohttp import web, ClientSession, ClientTimeout
import pytest

@pytest.fixture
def unused_port_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    yield sock
    sock.close()

async def dummy_task():
    await asyncio.sleep(1)

async def extra_test_function(session: ClientSession):
    response = await session.get('http://127.0.0.1:8080/test')
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket):
    sock = unused_port_socket
    timeout = 5

    app = web.Application()
    app.router.add_get('/test', lambda request: web.Response(text='OK'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopped'))

    task = asyncio.create_task(dummy_task())

    with pytest.raises(asyncio.TimeoutError):
        web.run_app(app, sock=sock, shutdown_timeout=timeout)

    assert task is not None
    assert not task.cancelled()

    async with ClientSession() as session:
        await extra_test_function(session)