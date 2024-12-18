import asyncio
import socket
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple
import pytest
from aiohttp import ClientSession, ClientTimeout, web

@pytest.mark.parametrize('run_app_kwargs, expected_server_calls, expected_unix_server_calls', mixed_bindings_test_params, ids=mixed_bindings_test_ids)
async def test_run_app_timeout_handling(run_app_kwargs: Dict[str, Any], expected_server_calls: List[mock._Call], expected_unix_server_calls: List[mock._Call], patched_loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()
    
    async def mock_task():
        await asyncio.sleep(1)

    async def extra_test(sess: ClientSession) -> None:
        with pytest.raises(asyncio.TimeoutError):
            await sess.get('http://127.0.0.1:{}/'.format(run_app_kwargs['port']), timeout=ClientTimeout(total=0.1))

    web.run_app(app, print=stopper(patched_loop), **run_app_kwargs, loop=patched_loop)

    assert patched_loop.create_unix_server.mock_calls == expected_unix_server_calls  # type: ignore[attr-defined]
    assert patched_loop.create_server.mock_calls == expected_server_calls

@pytest.mark.parametrize('run_app_kwargs', [{'sock': socket.socket(), 'timeout': 5, 'task': mock_task}])
async def test_run_app_connection_count(run_app_kwargs: Dict[str, Any]) -> None:
    sock = run_app_kwargs['sock']
    timeout = run_app_kwargs['timeout']
    task = run_app_kwargs['task']
    
    num_connections = 0

    async def on_request(request: web.Request) -> web.Response:
        nonlocal num_connections
        num_connections += 1
        return web.Response(text='Connection Count: {}'.format(num_connections))

    app = web.Application()
    app.router.add_get('/', on_request)
    app.router.add_get('/stop', lambda request: web.Response(text='Stopping'))

    await asyncio.sleep(0.1)  # Allow server to start

    async with ClientSession() as sess:
        await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/')
        await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/stop')

    assert num_connections == 1

@pytest.mark.parametrize('run_app_kwargs', [{'sock': socket.socket(), 'timeout': 5, 'task': mock_task}])
async def test_run_app_with_extra_test(run_app_kwargs: Dict[str, Any]) -> None:
    sock = run_app_kwargs['sock']
    timeout = run_app_kwargs['timeout']
    task = run_app_kwargs['task']

    async def extra_test(sess: ClientSession) -> None:
        response = await sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/')
        assert response.status == 200

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='Hello World'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopping'))

    web.run_app(app, sock=sock, shutdown_timeout=timeout)

    async with ClientSession() as sess:
        await extra_test(sess)