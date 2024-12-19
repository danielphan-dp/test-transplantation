import asyncio
import pytest
from unittest import mock
from aiohttp import web, ClientSession, ClientTimeout, ClientConnectorError

@pytest.mark.parametrize('run_app_kwargs, expected_server_calls, expected_unix_server_calls', mixed_bindings_test_params, ids=mixed_bindings_test_ids)
async def test_run_app_timeout_handling(run_app_kwargs, expected_server_calls, expected_unix_server_calls, patched_loop) -> None:
    app = web.Application()
    
    async def mock_task():
        await asyncio.sleep(0.2)

    async def extra_test(sess: ClientSession) -> None:
        with pytest.raises(asyncio.TimeoutError):
            await sess.get('http://127.0.0.1:8080/', timeout=ClientTimeout(total=0.1))

    run_app_kwargs['task'] = mock_task
    web.run_app(app, print=stopper(patched_loop), **run_app_kwargs, loop=patched_loop)

    assert patched_loop.create_unix_server.mock_calls == expected_unix_server_calls  # type: ignore[attr-defined]
    assert patched_loop.create_server.mock_calls == expected_server_calls

@pytest.mark.parametrize('run_app_kwargs', [{'timeout': 0.1}])
async def test_run_app_connection_error(run_app_kwargs, patched_loop) -> None:
    app = web.Application()

    async def mock_task():
        await asyncio.sleep(0.5)

    run_app_kwargs['task'] = mock_task

    with mock.patch('aiohttp.ClientSession.get', side_effect=ClientConnectorError):
        with pytest.raises(ClientConnectorError):
            web.run_app(app, print=stopper(patched_loop), **run_app_kwargs, loop=patched_loop)

@pytest.mark.parametrize('run_app_kwargs', [{'timeout': 0.1}])
async def test_run_app_successful_response(run_app_kwargs, patched_loop) -> None:
    app = web.Application()

    async def mock_task():
        await asyncio.sleep(0.1)

    async def handler(request: web.Request) -> web.Response:
        return web.Response(text='Success')

    app.router.add_get('/', handler)
    run_app_kwargs['task'] = mock_task

    web.run_app(app, print=stopper(patched_loop), **run_app_kwargs, loop=patched_loop)

    async with ClientSession() as sess:
        async with sess.get('http://127.0.0.1:8080/') as response:
            assert response.status == 200
            text = await response.text()
            assert text == 'Success'