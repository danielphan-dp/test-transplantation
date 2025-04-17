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
    response = await session.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket) -> None:
    sock = unused_port_socket
    timeout = 5
    task = dummy_task

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_app(sock, timeout, task, extra_test_function))

    port = sock.getsockname()[1]
    async with ClientSession() as sess:
        with pytest.raises(asyncio.TimeoutError):
            await sess.get(f'http://127.0.0.1:{port}/', timeout=ClientTimeout(total=0.1))