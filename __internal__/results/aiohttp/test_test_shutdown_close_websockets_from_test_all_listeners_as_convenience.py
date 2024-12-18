import asyncio
import socket
import pytest
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    async def task(self) -> None:
        await asyncio.sleep(1)

    async def extra_test(self, session: ClientSession) -> None:
        async with session.get('http://127.0.0.1:8080/') as response:
            assert response.status == 200

    @pytest.mark.asyncio
    async def test_run_app_with_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        timeout = 5
        port = sock.getsockname()[1]

        async def test() -> None:
            await asyncio.sleep(0.5)
            async with ClientSession() as sess:
                with pytest.raises(asyncio.TimeoutError):
                    await sess.get(f'http://127.0.0.1:{port}/', timeout=ClientTimeout(total=0.1))

        app = web.Application()
        app.router.add_get('/', self.stop)
        app.cleanup_ctx.append(self.extra_test)

        web.run_app(app, sock=sock, shutdown_timeout=timeout)

    @pytest.mark.asyncio
    async def test_run_app_with_connection_error(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        timeout = 5
        port = sock.getsockname()[1]

        async def test() -> None:
            await asyncio.sleep(0.5)
            async with ClientSession() as sess:
                with pytest.raises(ClientConnectorError):
                    await sess.get(f'http://127.0.0.1:{port}/nonexistent')

        app = web.Application()
        app.router.add_get('/', self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=timeout)

    @pytest.mark.asyncio
    async def test_run_app_successful_response(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        timeout = 5
        port = sock.getsockname()[1]

        async def test() -> None:
            await asyncio.sleep(0.5)
            async with ClientSession() as sess:
                async with sess.get(f'http://127.0.0.1:{port}/') as response:
                    assert response.status == 200

        app = web.Application()
        app.router.add_get('/', self.stop)

        web.run_app(app, sock=sock, shutdown_timeout=timeout)