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
    await asyncio.sleep(0.1)

async def extra_test_function(session: ClientSession) -> None:
    response = await session.get('http://127.0.0.1:8080/')
    assert response.status == 200

def test_run_app_with_extra_test(unused_port_socket) -> None:
    sock = unused_port_socket
    timeout = 5

    with contextlib.closing(sock):
        sock.listen(1)
        port = sock.getsockname()[1]

        app = web.Application()
        app.router.add_get('/', lambda request: web.Response(text='FOO'))
        app.router.add_get('/stop', lambda request: web.Response(text='STOP'))

        task, num_connections = run_app(sock, timeout, dummy_task, extra_test_function)

        assert num_connections == 0

        async def test_client() -> None:
            async with ClientSession() as session:
                with pytest.raises(asyncio.TimeoutError):
                    await session.get(f'http://127.0.0.1:{port}/', timeout=ClientTimeout(total=0.1))

        asyncio.run(test_client())
        asyncio.run(app.shutdown())