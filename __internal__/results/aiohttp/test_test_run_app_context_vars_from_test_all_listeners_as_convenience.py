import asyncio
import socket
from aiohttp import web, ClientSession, ClientTimeout
import pytest

@pytest.fixture
def unused_port_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    yield sock
    sock.close()

async def dummy_task() -> None:
    await asyncio.sleep(0.1)

async def extra_test_function(session: ClientSession) -> None:
    response = await session.get('http://127.0.0.1:8080/test')
    assert response.status == 200

async def stop_handler(request: web.Request) -> web.Response:
    return web.Response(text='Stopped')

def test_run_app_with_extra_test(unused_port_socket) -> None:
    sock = unused_port_socket
    port = sock.getsockname()[1]
    
    app = web.Application()
    app.router.add_get('/test', stop_handler)
    app.router.add_get('/stop', stop_handler)

    task, num_connections = run_app(sock, timeout=5, task=dummy_task, extra_test=extra_test_function)

    assert task is not None
    assert num_connections >= 0

    async def shutdown_app() -> None:
        async with ClientSession() as session:
            await session.get(f'http://127.0.0.1:{port}/stop')

    asyncio.run(shutdown_app())