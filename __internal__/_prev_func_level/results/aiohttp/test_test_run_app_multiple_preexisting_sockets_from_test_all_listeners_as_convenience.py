import asyncio
import contextlib
import socket
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.fixture
def unused_port_socket() -> socket.socket:
    sock = socket.socket()
    sock.bind(("localhost", 0))
    yield sock
    sock.close()

async def dummy_task() -> None:
    await asyncio.sleep(1)

async def extra_test_function(session: ClientSession) -> None:
    response = await session.get('http://127.0.0.1:8080/test')
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket) -> None:
    sock = unused_port_socket
    timeout = 5

    app = web.Application()
    app.router.add_get('/test', lambda request: web.Response(text='OK'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopped'))

    task, num_connections = run_app(sock, timeout, dummy_task, extra_test_function)

    assert task is not None
    assert num_connections >= 0

    async def check_timeout() -> None:
        async with ClientSession() as sess:
            with pytest.raises(asyncio.TimeoutError):
                await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/', timeout=ClientTimeout(total=0.1))

    asyncio.run(check_timeout())