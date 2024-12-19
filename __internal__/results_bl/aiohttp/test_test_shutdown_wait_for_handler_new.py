import asyncio
import socket
from unittest import mock
import pytest
from aiohttp import ClientSession, ClientTimeout, ClientConnectorError, web

class TestRunApp:
    @pytest.fixture
    def unused_port_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        yield sock
        sock.close()

    async def task_with_error(self):
        raise ValueError("This is a test error")

    async def task_with_delay(self):
        await asyncio.sleep(1)

    def test_run_app_with_error(self, unused_port_socket):
        sock = unused_port_socket
        with pytest.raises(ValueError):
            self.run_app(sock, 3, self.task_with_error)

    def test_run_app_with_delay(self, unused_port_socket):
        sock = unused_port_socket
        finished = False

        async def task():
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        t, connection_count = self.run_app(sock, 3, task)

        assert finished is True
        assert t.done()
        assert not t.cancelled()
        assert connection_count == 0

    def test_run_app_timeout(self, unused_port_socket):
        sock = unused_port_socket
        finished = False

        async def task():
            nonlocal finished
            await asyncio.sleep(5)
            finished = True

        t, connection_count = self.run_app(sock, 1, task)

        assert finished is False
        assert t.done()
        assert t.cancelled()
        assert connection_count >= 0

    def test_run_app_extra_test(self, unused_port_socket):
        sock = unused_port_socket
        finished = False

        async def task():
            nonlocal finished
            await asyncio.sleep(2)
            finished = True

        async def extra_test(sess):
            async with sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/') as response:
                assert response.status == 200

        t, connection_count = self.run_app(sock, 3, task, extra_test)

        assert finished is True
        assert t.done()
        assert not t.cancelled()
        assert connection_count == 0