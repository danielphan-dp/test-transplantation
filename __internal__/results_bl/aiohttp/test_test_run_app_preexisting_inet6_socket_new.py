import asyncio
import contextlib
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.mark.skipif(not HAS_IPV6, reason='IPv6 is not available')
async def test_run_app_with_timeout(patched_loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()

    sock = socket.socket(socket.AF_INET6)
    with contextlib.closing(sock):
        sock.bind(("::1", 0))
        port = sock.getsockname()[1]

        async def dummy_task():
            await asyncio.sleep(1)

        async def extra_test(sess: ClientSession):
            response = await sess.get(f'http://[::1]:{port}/')
            assert response.status == 200

        with mock.patch('aiohttp.web_runner.Server') as mock_server:
            await run_app(sock, timeout=0.5, task=dummy_task, extra_test=extra_test)

        mock_server.assert_called_once()
        assert mock_server.call_args[0][0] == mock.ANY

@pytest.mark.skipif(not HAS_IPV6, reason='IPv6 is not available')
async def test_run_app_with_connection_error(patched_loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()

    sock = socket.socket(socket.AF_INET6)
    with contextlib.closing(sock):
        sock.bind(("::1", 0))
        port = sock.getsockname()[1]

        async def dummy_task():
            await asyncio.sleep(1)

        async def extra_test(sess: ClientSession):
            with pytest.raises(ClientConnectorError):
                await sess.get(f'http://[::1]:{port}/nonexistent')

        with mock.patch('aiohttp.web_runner.Server') as mock_server:
            await run_app(sock, timeout=0.5, task=dummy_task, extra_test=extra_test)

        mock_server.assert_called_once()
        assert mock_server.call_args[0][0] == mock.ANY

@pytest.mark.skipif(not HAS_IPV6, reason='IPv6 is not available')
async def test_run_app_with_no_connections(patched_loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()

    sock = socket.socket(socket.AF_INET6)
    with contextlib.closing(sock):
        sock.bind(("::1", 0))
        port = sock.getsockname()[1]

        async def dummy_task():
            await asyncio.sleep(0.5)

        with mock.patch('aiohttp.web_runner.Server') as mock_server:
            task, num_connections = await run_app(sock, timeout=1, task=dummy_task)

        assert num_connections == 0
        mock_server.assert_called_once()
        assert mock_server.call_args[0][0] == mock.ANY