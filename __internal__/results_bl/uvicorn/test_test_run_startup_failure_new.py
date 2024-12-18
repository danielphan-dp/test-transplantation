import pytest
from uvicorn import run

def test_run_invalid_sockets(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(ValueError) as excinfo:
        run(sockets="invalid_sockets")
    assert "Invalid sockets" in str(excinfo.value)

def test_run_empty_sockets(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(ValueError) as excinfo:
        run(sockets=[])
    assert "No sockets provided" in str(excinfo.value)

def test_run_none_sockets(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(ValueError) as excinfo:
        run(sockets=None)
    assert "No sockets provided" in str(excinfo.value)

def test_run_successful_startup(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})

    try:
        run(app, lifespan="on")
    except SystemExit as exit_exception:
        assert exit_exception.value.code == 0

def test_run_startup_timeout(caplog: pytest.LogCaptureFixture) -> None:
    async def app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            await asyncio.sleep(5)  # Simulate a long startup

    with pytest.raises(SystemExit) as exit_exception:
        run(app, lifespan="on", timeout=1)
    assert exit_exception.value.code == 3