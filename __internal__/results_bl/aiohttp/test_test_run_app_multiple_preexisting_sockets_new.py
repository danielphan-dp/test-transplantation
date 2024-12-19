import asyncio
import contextlib
import socket
from unittest import mock
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.mark.asyncio
async def test_run_app_with_timeout(patched_loop):
    app = web.Application()

    sock = socket.socket()
    with contextlib.closing(sock):
        sock.bind(("localhost", 0))
        _, port = sock.getsockname()

        async def dummy_task():
            await asyncio.sleep(1)

        printer = mock.Mock()
        with mock.patch('aiohttp.web_runner.Server') as mock_server:
            web.run_app(app, sock=sock, print=printer, loop=patched_loop)

            assert mock_server.call_count == 1

            async with ClientSession() as sess:
                with pytest.raises(asyncio.TimeoutError):
                    await sess.get(f'http://127.0.0.1:{port}/', timeout=ClientTimeout(total=0.1))

            assert f"http://127.0.0.1:{port}" in printer.call_args[0][0]

@pytest.mark.asyncio
async def test_run_app_with_extra_test(patched_loop):
    app = web.Application()

    sock = socket.socket()
    with contextlib.closing(sock):
        sock.bind(("localhost", 0))
        _, port = sock.getsockname()

        async def dummy_task():
            await asyncio.sleep(0.5)

        async def extra_test(sess):
            response = await sess.get(f'http://127.0.0.1:{port}/')
            assert response.status == 200

        printer = mock.Mock()
        with mock.patch('aiohttp.web_runner.Server') as mock_server:
            web.run_app(app, sock=sock, print=printer, loop=patched_loop)

            assert mock_server.call_count == 1

            async with ClientSession() as sess:
                await extra_test(sess)

            assert f"http://127.0.0.1:{port}" in printer.call_args[0][0]