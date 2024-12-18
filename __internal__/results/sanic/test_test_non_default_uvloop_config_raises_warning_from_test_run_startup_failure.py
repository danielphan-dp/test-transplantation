import pytest
from unittest.mock import patch
from sanic import Sanic
from sanic.server import run

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_run_with_repl(caplog, capsys, app):
    command = ['fake.server.app', '--repl', f'-p={get_port()}']
    
    with patch("sanic.cli.app.is_atty", return_value=True):
        result = run(app)
    
    assert "Welcome to the Sanic interactive console" in result.err
    assert ">>> " in result.out

def test_run_without_repl(caplog, capsys, app):
    command = ['fake.server.app', '-p={get_port()}']
    
    with patch("sanic.cli.app.is_atty", return_value=False):
        result = run(app)
    
    assert "Can't start REPL in non-interactive mode." in caplog.text

def test_run_with_invalid_port(caplog, capsys, app):
    command = ['fake.server.app', '--repl', '-p=invalid_port']
    
    with pytest.raises(SystemExit) as exit_exception:
        run(app)
    
    assert exit_exception.value.code == 1
    assert "Invalid port" in caplog.text

def test_run_startup_failure(caplog, app):
    async def failing_app(scope, receive, send):
        assert scope["type"] == "lifespan"
        message = await receive()
        if message["type"] == "lifespan.startup":
            raise RuntimeError("Startup failed")

    with pytest.raises(SystemExit) as exit_exception:
        run(failing_app, lifespan="on")
    
    assert exit_exception.value.code == 3
    assert "Startup failed" in caplog.text