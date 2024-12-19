import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError
from uuid import uuid4

@pytest.mark.skipif(not hasattr(socket, 'AF_UNIX'), reason='requires UNIX sockets')
async def test_run_app_with_timeout(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock_path = b"\x00" + uuid4().hex.encode("ascii")
    app = web.Application()

    async def dummy_task():
        await asyncio.sleep(1)

    async def extra_test(sess: ClientSession):
        response = await sess.get(f'http://127.0.0.1:{sock_path.decode("ascii")}/')
        assert response.status == 200

    with mock.patch('aiohttp.web_runner.Server') as mock_server:
        result = await app.run_app(
            sock=socket.socket(socket.AF_UNIX),
            timeout=0.5,
            task=dummy_task,
            extra_test=extra_test
        )
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], asyncio.Task)
        assert isinstance(result[1], int)

    mock_server.assert_called_once()

@pytest.mark.skipif(not hasattr(socket, 'AF_UNIX'), reason='requires UNIX sockets')
async def test_run_app_with_connection_error(patched_loop: asyncio.AbstractEventLoop) -> None:
    sock_path = b"\x00" + uuid4().hex.encode("ascii")
    app = web.Application()

    async def dummy_task():
        await asyncio.sleep(1)

    with mock.patch('aiohttp.ClientSession.get', side_effect=ClientConnectorError) as mock_get:
        with pytest.raises(ClientConnectorError):
            await app.run_app(
                sock=socket.socket(socket.AF_UNIX),
                timeout=0.5,
                task=dummy_task
            )
        mock_get.assert_called()