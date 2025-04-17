import pytest
import logging
import asyncio
from uvicorn import run

@pytest.mark.asyncio
async def test_run_with_valid_sockets(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})

    with caplog.at_level(logging.DEBUG):
        run(app, lifespan="on")

    assert "lifespan.startup complete" in caplog.text

@pytest.mark.asyncio
async def test_run_with_invalid_sockets(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            raise RuntimeError("Invalid socket configuration")

    with pytest.raises(SystemExit) as exit_exception:
        run(app, lifespan="on")
    assert exit_exception.value.code == 3
    assert "Invalid socket configuration" in caplog.text

@pytest.mark.asyncio
async def test_run_with_no_sockets(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit) as exit_exception:
        run(sockets=None)
    assert exit_exception.value.code == 1
    assert "No sockets provided" in caplog.text

@pytest.mark.asyncio
async def test_run_with_multiple_sockets(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})

    sockets = [asyncio.open_unix_connection('/tmp/socket1'), asyncio.open_unix_connection('/tmp/socket2')]
    with caplog.at_level(logging.DEBUG):
        run(app, sockets=sockets, lifespan="on")

    assert "lifespan.startup complete" in caplog.text