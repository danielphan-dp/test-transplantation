import asyncio
import logging
import pytest
from pytest import LogCaptureFixture
from sanic import Sanic

@pytest.mark.xfail(reason='This test runs fine locally, but fails on CI')
@pytest.mark.parametrize('shutdown_timeout', [0, 1, 5])
def test_stop_app_with_various_timeouts(app, caplog: LogCaptureFixture, shutdown_timeout):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = shutdown_timeout

    @app.get("/")
    async def handler(request):
        await asyncio.sleep(5)

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        connect = asyncio.open_connection("127.0.0.1", app.config.PORT)
        _, writer = await connect
        writer.write(b"GET / HTTP/1.1\r\n\r\n")
        app.stop()

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True)

    assert "Request: GET http:/// stopped. Transport is closed." in caplog.text
    assert app.is_stopped is True

@pytest.mark.xfail(reason='This test runs fine locally, but fails on CI')
def test_stop_app_without_pending_requests(app, caplog: LogCaptureFixture):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True)

    assert "Application stopped." in caplog.text
    assert app.is_stopped is True

@pytest.mark.xfail(reason='This test runs fine locally, but fails on CI')
def test_stop_app_with_no_requests(app, caplog: LogCaptureFixture):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True)

    assert "Application stopped." in caplog.text
    assert app.is_stopped is True