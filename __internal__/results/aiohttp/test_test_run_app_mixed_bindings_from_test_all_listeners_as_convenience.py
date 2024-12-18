import asyncio
import socket
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple
import pytest
from unittest import mock
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.mark.parametrize('run_app_kwargs, expected_server_calls, expected_unix_server_calls', mixed_bindings_test_params, ids=mixed_bindings_test_ids)
async def test_run_app_timeout_handling(run_app_kwargs: Dict[str, Any], expected_server_calls: List[mock._Call], expected_unix_server_calls: List[mock._Call], patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket()
    timeout = 1
    task_called = False

    async def mock_task() -> None:
        nonlocal task_called
        task_called = True
        await asyncio.sleep(2)  # Simulate a long-running task

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='Hello, World!'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopped'))

    with mock.patch('aiohttp.web_runner.Server', new_callable=mock.PropertyMock) as mock_server:
        await asyncio.wait_for(web.run_app(app, sock=sock, shutdown_timeout=timeout), timeout=timeout + 0.5)
    
    assert task_called is False  # Ensure the task was not completed due to timeout
    assert patched_loop.create_unix_server.mock_calls == expected_unix_server_calls  # type: ignore[attr-defined]
    assert patched_loop.create_server.mock_calls == expected_server_calls

@pytest.mark.parametrize('run_app_kwargs, expected_server_calls, expected_unix_server_calls', mixed_bindings_test_params, ids=mixed_bindings_test_ids)
async def test_run_app_connection_error(run_app_kwargs: Dict[str, Any], expected_server_calls: List[mock._Call], expected_unix_server_calls: List[mock._Call], patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket()
    timeout = 1

    async def mock_task() -> None:
        await asyncio.sleep(0.1)

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='Hello, World!'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopped'))

    with mock.patch('aiohttp.ClientSession.get', side_effect=ClientConnectorError) as mock_get:
        with pytest.raises(ClientConnectorError):
            await web.run_app(app, sock=sock, shutdown_timeout=timeout)

    assert mock_get.called  # Ensure the connection error was triggered
    assert patched_loop.create_unix_server.mock_calls == expected_unix_server_calls  # type: ignore[attr-defined]
    assert patched_loop.create_server.mock_calls == expected_server_calls

@pytest.mark.parametrize('run_app_kwargs, expected_server_calls, expected_unix_server_calls', mixed_bindings_test_params, ids=mixed_bindings_test_ids)
async def test_run_app_successful_response(run_app_kwargs: Dict[str, Any], expected_server_calls: List[mock._Call], expected_unix_server_calls: List[mock._Call], patched_loop: asyncio.AbstractEventLoop) -> None:
    sock = socket.socket()
    timeout = 1
    response_received = False

    async def mock_task() -> None:
        await asyncio.sleep(0.1)

    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text='Hello, World!'))
    app.router.add_get('/stop', lambda request: web.Response(text='Stopped'))

    async with ClientSession() as sess:
        await web.run_app(app, sock=sock, shutdown_timeout=timeout)
        async with sess.get(f'http://127.0.0.1:{sock.getsockname()[1]}/') as response:
            assert response.status == 200
            text = await response.text()
            assert text == 'Hello, World!'
            response_received = True

    assert response_received  # Ensure the response was successfully received
    assert patched_loop.create_unix_server.mock_calls == expected_unix_server_calls  # type: ignore[attr-defined]
    assert patched_loop.create_server.mock_calls == expected_server_calls