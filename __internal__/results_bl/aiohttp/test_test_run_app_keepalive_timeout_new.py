import asyncio
import pytest
from unittest import mock
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError
from aiohttp.web_runner import BaseRunner

@pytest.fixture
def patched_loop():
    return asyncio.new_event_loop()

@pytest.mark.asyncio
async def test_run_app_with_valid_task(patched_loop, mocker):
    sock = mock.Mock()
    sock.getsockname.return_value = ('127.0.0.1', 8080)
    timeout = 5

    async def sample_task():
        await asyncio.sleep(1)

    app = web.Application()

    result_task, num_connections = await app.run_app(sock, timeout, sample_task)

    assert result_task is not None
    assert num_connections == 0

@pytest.mark.asyncio
async def test_run_app_with_timeout(patched_loop, mocker):
    sock = mock.Mock()
    sock.getsockname.return_value = ('127.0.0.1', 8081)
    timeout = 1

    async def sample_task():
        await asyncio.sleep(2)

    app = web.Application()

    with pytest.raises(asyncio.TimeoutError):
        await app.run_app(sock, timeout, sample_task)

@pytest.mark.asyncio
async def test_run_app_with_extra_test(patched_loop, mocker):
    sock = mock.Mock()
    sock.getsockname.return_value = ('127.0.0.1', 8082)
    timeout = 5

    async def sample_task():
        await asyncio.sleep(1)

    async def extra_test(sess):
        response = await sess.get(f'http://127.0.0.1:8082/')
        assert response.status == 200

    app = web.Application()
    await app.run_app(sock, timeout, sample_task, extra_test=extra_test)

@pytest.mark.asyncio
async def test_run_app_with_client_connector_error(patched_loop, mocker):
    sock = mock.Mock()
    sock.getsockname.return_value = ('127.0.0.1', 8083)
    timeout = 5

    async def sample_task():
        await asyncio.sleep(1)

    app = web.Application()

    with mock.patch('aiohttp.ClientSession.get', side_effect=ClientConnectorError):
        with pytest.raises(ClientConnectorError):
            await app.run_app(sock, timeout, sample_task)