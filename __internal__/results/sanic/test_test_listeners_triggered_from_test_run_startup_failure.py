import logging
import pytest
from unittest.mock import patch
from sanic import Sanic
from sanic.server import run

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_run_with_repl(caplog, app):
    command = ['fake.server.app', '--repl', f'-p={get_port()}']
    
    with patch("sanic.cli.app.is_atty", return_value=True):
        result = run(app, lifespan="on")
    
    assert "Welcome to the Sanic interactive console" in result.err
    assert ">>> " in result.out

def test_run_startup_failure(caplog, app):
    async def failing_app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            raise RuntimeError("Startup failed")

    with pytest.raises(SystemExit) as exit_exception:
        run(failing_app, lifespan="on")
    
    assert exit_exception.value.code == 3

def test_run_logging_messages(caplog, app):
    start_message = (
        'You have set a listener for "before_server_start" in ASGI mode. '
        "It will be executed as early as possible, but not before the ASGI "
        "server is started."
    )
    stop_message = (
        'You have set a listener for "after_server_stop" in ASGI mode. '
        "It will be executed as late as possible, but not after the ASGI "
        "server is stopped."
    )

    with caplog.at_level(logging.DEBUG):
        run(app)

    assert (
        "sanic.root",
        logging.DEBUG,
        start_message,
    ) not in caplog.record_tuples
    assert (
        "sanic.root",
        logging.DEBUG,
        stop_message,
    ) not in caplog.record_tuples

def test_run_with_invalid_port(caplog, app):
    with pytest.raises(SystemExit):
        run(app, port=-1)

    assert "Invalid port number" in caplog.text

def test_run_with_custom_settings(caplog, app):
    app.state.verbosity = 2
    with caplog.at_level(logging.DEBUG):
        run(app)

    assert (
        "sanic.root",
        logging.DEBUG,
        "You have set a listener for 'before_server_start' in ASGI mode."
    ) in caplog.record_tuples
    assert (
        "sanic.root",
        logging.DEBUG,
        "You have set a listener for 'after_server_stop' in ASGI mode."
    ) in caplog.record_tuples