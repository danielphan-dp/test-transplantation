import logging
import pytest
from unittest.mock import patch
from sanic import Sanic
from sanic.server import run

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_run_with_repl_enabled(app, caplog, capsys):
    command = ['fake.server.app', '--repl', f'-p={get_port()}']
    
    with patch("sanic.cli.app.is_atty", return_value=True):
        result = run(app)
    
    assert "Welcome to the Sanic interactive console" in result.err
    assert ">>> " in result.out

def test_run_with_repl_disabled(app, caplog, capsys):
    command = ['fake.server.app', '--repl', f'-p={get_port()}']
    
    with patch("sanic.cli.app.is_atty", return_value=False):
        with pytest.raises(SystemExit) as exit_exception:
            run(app)
    
    assert exit_exception.value.code == 1
    assert ("sanic.error", logging.ERROR, "Can't start REPL in non-interactive mode.") in caplog.record_tuples

def test_run_startup_failure(app, caplog):
    async def failing_app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            raise RuntimeError("Startup failed")

    with pytest.raises(SystemExit) as exit_exception:
        run(failing_app, lifespan="on")
    
    assert exit_exception.value.code == 3

def test_run_with_logging(app, caplog):
    command = ['fake.server.app', '--repl', f'-p={get_port()}']
    
    with caplog.at_level(logging.DEBUG):
        run(app)
    
    assert ("sanic.root", logging.DEBUG, "Server started") in caplog.record_tuples
    assert ("sanic.root", logging.DEBUG, "Server stopped") in caplog.record_tuples

def test_run_with_custom_port(app, caplog):
    custom_port = 9999
    command = ['fake.server.app', '--repl', f'-p={custom_port}']
    
    with patch("sanic.cli.app.get_port", return_value=custom_port):
        result = run(app)
    
    assert f"Running on http://127.0.0.1:{custom_port}" in result.out