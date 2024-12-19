import asyncio
import pytest
from unittest import mock
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.mark.asyncio
async def test_run_app_with_timeout(patched_loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()
    task = None
    timeout_duration = 0.1

    async def long_running_task() -> None:
        await asyncio.sleep(1)

    async def on_startup(app: web.Application) -> None:
        nonlocal task
        loop = asyncio.get_event_loop()
        task = loop.create_task(long_running_task())

    app.on_startup.append(on_startup)

    sock = mock.Mock()
    sock.getsockname.return_value = ('127.0.0.1', 8080)

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(run_app(sock, timeout_duration, long_running_task), timeout=timeout_duration)

    assert task is not None
    assert task.cancelled()

@pytest.mark.asyncio
async def test_run_app_with_extra_test(patched_loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()
    task = None

    async def on_startup(app: web.Application) -> None:
        nonlocal task
        loop = asyncio.get_event_loop()
        task = loop.create_task(asyncio.sleep(1000))

    async def extra_test(sess: ClientSession) -> None:
        response = await sess.get('http://127.0.0.1:8080/')
        assert response.status == 200

    app.on_startup.append(on_startup)

    sock = mock.Mock()
    sock.getsockname.return_value = ('127.0.0.1', 8080)

    await run_app(sock, 5, asyncio.sleep(0), extra_test)

    assert task is not None
    assert not task.cancelled()