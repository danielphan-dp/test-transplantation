import asyncio
import socket
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError
from unittest import mock

@pytest.mark.skipif(not hasattr(socket, 'AF_UNIX'), reason='requires UNIX sockets')
async def test_run_app_with_timeout(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket(socket.AF_UNIX)
    sock.bind(b"\x00" + uuid4().hex.encode("ascii"))
    sock.listen(1)

    async def task():
        await asyncio.sleep(1)

    async def extra_test(sess: ClientSession) -> None:
        response = await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/')
        assert response.status == 200

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.PropertyMock) as mock_server:
        mock_server.return_value = None
        t, num_connections = run_app(sock, timeout=0.5, task=task, extra_test=extra_test)
        assert num_connections == 0
        assert t is not None
        assert t.exception() is None

    sock.close()

@pytest.mark.skipif(not hasattr(socket, 'AF_UNIX'), reason='requires UNIX sockets')
async def test_run_app_with_connection_error(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket(socket.AF_UNIX)
    sock.bind(b"\x00" + uuid4().hex.encode("ascii"))
    sock.listen(1)

    async def task():
        await asyncio.sleep(1)

    async def extra_test(sess: ClientSession) -> None:
        with pytest.raises(ClientConnectorError):
            await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/nonexistent')

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.PropertyMock) as mock_server:
        mock_server.return_value = None
        t, num_connections = run_app(sock, timeout=0.5, task=task, extra_test=extra_test)
        assert num_connections == 0
        assert t is not None
        assert t.exception() is None

    sock.close()