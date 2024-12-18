import asyncio
import socket
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

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
    task = dummy_task

    app = web.Application()

    async def stop(request: web.Request) -> web.Response:
        return web.Response(text='Stopped')

    app.router.add_get('/stop', stop)
    app.router.add_get('/test', lambda request: web.Response(text='FOO'))

    t, num_connections = run_app(sock, timeout, task, extra_test=extra_test_function)

    assert t is not None
    assert num_connections >= 0

    with pytest.raises(asyncio.TimeoutError):
        async with ClientSession() as sess:
            await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/', timeout=ClientTimeout(total=0.1))

    asyncio.run(t)  # Ensure the task is awaited and completed
    assert t.exception() is None