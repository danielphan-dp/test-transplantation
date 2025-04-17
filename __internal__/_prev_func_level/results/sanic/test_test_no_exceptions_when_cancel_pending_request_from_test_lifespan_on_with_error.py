import asyncio
import logging
import pytest
from pytest import LogCaptureFixture
from sanic import Sanic

@pytest.mark.xfail(reason='This test runs fine locally, but fails on CI')
def test_stop_method_should_not_raise_exceptions(app, caplog: LogCaptureFixture, port):
    @app.get("/")
    async def handler(request):
        await asyncio.sleep(5)

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        connect = asyncio.open_connection("127.0.0.1", port)
        _, writer = await connect
        writer.write(b"GET / HTTP/1.1\r\n\r\n")
        app.stop()

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True, port=port)

    assert "Request: GET http:/// stopped. Transport is closed." in caplog.text

@pytest.mark.xfail(reason='This test runs fine locally, but fails on CI')
def test_stop_method_with_no_active_requests(app, caplog: LogCaptureFixture):
    with caplog.at_level(logging.INFO):
        app.stop()

    assert "Transport is closed." not in caplog.text

@pytest.mark.xfail(reason='This test runs fine locally, but fails on CI')
def test_stop_method_multiple_calls(app, caplog: LogCaptureFixture):
    @app.get("/")
    async def handler(request):
        await asyncio.sleep(5)

    app.run(single_process=True, access_log=True)

    app.stop()
    with caplog.at_level(logging.INFO):
        app.stop()

    assert "Transport is closed." not in caplog.text

@pytest.mark.xfail(reason='This test runs fine locally, but fails on CI')
def test_stop_method_with_active_requests(app, caplog: LogCaptureFixture, port):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    @app.get("/")
    async def handler(request):
        await asyncio.sleep(5)

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        connect = asyncio.open_connection("127.0.0.1", port)
        _, writer = await connect
        writer.write(b"GET / HTTP/1.1\r\n\r\n")
        await asyncio.sleep(0.5)  # Allow some time before stopping
        app.stop()

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True, port=port)

    assert "Request: GET http:/// stopped. Transport is closed." in caplog.text