import pytest
import logging
from uvicorn import run

def test_run_with_valid_sockets(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})

    with caplog.at_level(logging.INFO):
        run(app, lifespan="on", sockets=[{"type": "tcp", "host": "127.0.0.1", "port": 8000}])
    
    assert "Lifespan startup complete" in caplog.text

def test_run_with_invalid_sockets(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            raise RuntimeError("Invalid socket configuration")

    with pytest.raises(SystemExit) as exit_exception:
        run(app, lifespan="on", sockets=[{"type": "tcp", "host": "invalid_host", "port": 8000}])
    
    assert exit_exception.value.code == 3
    assert "Invalid socket configuration" in caplog.text

def test_run_with_no_sockets(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})

    with caplog.at_level(logging.WARNING):
        run(app, lifespan="on", sockets=None)
    
    assert "No sockets provided" in caplog.text

def test_run_with_multiple_sockets(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})

    with caplog.at_level(logging.INFO):
        run(app, lifespan="on", sockets=[
            {"type": "tcp", "host": "127.0.0.1", "port": 8000},
            {"type": "tcp", "host": "127.0.0.1", "port": 8001}
        ])
    
    assert "Lifespan startup complete" in caplog.text