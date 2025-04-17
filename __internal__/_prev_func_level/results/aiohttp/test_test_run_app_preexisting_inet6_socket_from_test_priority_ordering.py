import asyncio
import contextlib
import socket
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

        async def extra_test(sess: ClientSession) -> None:
            response = await sess.get(f'http://127.0.0.1:{port}/')
            assert response.status == 200

        with pytest.raises(asyncio.TimeoutError):
            await run_app(sock, timeout=0.1, task=dummy_task, extra_test=extra_test)

        printer = mock.Mock(wraps=stopper(patched_loop))
        web.run_app(app, sock=sock, print=printer, loop=patched_loop)

        patched_loop.create_server.assert_called_with(
            mock.ANY, sock=sock, backlog=128, ssl=None
        )
        assert f"http://[::1]:{port}" in printer.call_args[0][0]