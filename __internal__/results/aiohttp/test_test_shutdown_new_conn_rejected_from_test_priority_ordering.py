import asyncio
import socket
from aiohttp import ClientSession, ClientTimeout, web
import pytest

class TestRunApp:
    async def stop(self, request: web.Request) -> web.Response:
        return web.Response()

    def run_app(
        self,
        sock: socket.socket,
        timeout: int,
        task: Callable[[], Coroutine[None, None, None]],
        extra_test: Optional[Callable[[ClientSession], Awaitable[None]]] = None,
    ) -> Tuple["asyncio.Task[None]", int]:
        num_connections = -1
        t = test_task = None
        port = sock.getsockname()[1]

        class DictRecordClear(Dict[RequestHandler[web.Request], asyncio.Transport]):
            def clear(self) -> None:
                nonlocal num_connections
                num_connections = len(self)
                super().clear()

        class ServerWithRecordClear(web.Server[web.Request]):
            def __init__(self, *args: Any, **kwargs: Any):
                super().__init__(*args, **kwargs)
                self._connections = DictRecordClear()

        async def test() -> None:
            await asyncio.sleep(0.5)
            async with ClientSession() as sess:
                for _ in range(5):
                    try:
                        with pytest.raises(asyncio.TimeoutError):
                            async with sess.get(f'http://127.0.0.1:{port}/', timeout=ClientTimeout(total=0.1)):
                                pass
                    except ClientConnectorError:
                        await asyncio.sleep(0.5)
                    else:
                        break
                async with sess.get(f'http://127.0.0.1:{port}/stop'):
                    pass
                if extra_test:
                    await extra_test(sess)

        async def run_test(app: web.Application) -> AsyncIterator[None]:
            nonlocal test_task
            test_task = asyncio.create_task(test())
            yield
            await test_task

        async def handler(request: web.Request) -> web.Response:
            nonlocal t
            t = asyncio.create_task(task())
            await t
            return web.Response(text='FOO')

        app = web.Application()
        app.cleanup_ctx.append(run_test)
        app.router.add_get('/', handler)
        app.router.add_get('/stop', self.stop)
        with mock.patch('aiohttp.web_runner.Server', ServerWithRecordClear):
            web.run_app(app, sock=sock, shutdown_timeout=timeout)
        assert test_task is not None
        assert test_task.exception() is None
        assert t is not None
        return (t, num_connections)

    def test_shutdown_new_conn_rejected(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(9)
            finished = True

        async def test(sess: ClientSession) -> None:
            await asyncio.sleep(1)
            with pytest.raises(ClientConnectorError):
                async with ClientSession() as sess:
                    async with sess.get(f"http://127.0.0.1:{port}/"):
                        pass
            assert finished is False

        t, connection_count = self.run_app(sock, 10, task, test)

        assert finished is True
        assert t.done()
        assert connection_count == 0

    def test_run_app_with_extra_test(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        finished = False

        async def task() -> None:
            nonlocal finished
            await asyncio.sleep(5)
            finished = True

        async def extra_test(sess: ClientSession) -> None:
            await asyncio.sleep(1)
            response = await sess.get(f"http://127.0.0.1:{port}/")
            assert response.status == 200

        t, connection_count = self.run_app(sock, 10, task, extra_test)

        assert finished is True
        assert t.done()
        assert connection_count == 0

    def test_run_app_timeout(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]

        async def task() -> None:
            await asyncio.sleep(2)

        async def test(sess: ClientSession) -> None:
            with pytest.raises(asyncio.TimeoutError):
                async with sess.get(f"http://127.0.0.1:{port}/", timeout=ClientTimeout(total=0.1)):
                    pass

        t, connection_count = self.run_app(sock, 10, task, test)

        assert t.done()
        assert connection_count == 0

    def test_run_app_connection_count(self, unused_port_socket: socket.socket) -> None:
        sock = unused_port_socket
        port = sock.getsockname()[1]
        connection_count = 0

        async def task() -> None:
            nonlocal connection_count
            await asyncio.sleep(1)
            connection_count += 1

        async def test(sess: ClientSession) -> None:
            await asyncio.sleep(0.5)
            async with sess.get(f"http://127.0.0.1:{port}/"):
                pass

        t, final_connection_count = self.run_app(sock, 10, task, test)

        assert t.done()
        assert final_connection_count == 1
        assert connection_count == 1