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
        result = run(app, reload=True)

    assert "Welcome to the Sanic interactive console" in result.err
    assert ">>> " in result.out

def test_run_with_invalid_app_config(app, caplog):
    with pytest.raises(SystemExit) as exit_exception:
        run(app, reload=True)
    
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].message == (
        "You must pass the application as an import string to enable "
        "'reload' or 'workers'."
    )

def test_run_without_repl(app, caplog):
    command = ['fake.server.app', '-p={get_port()}']
    
    with caplog.at_level(logging.DEBUG):
        run(app)

    assert ("sanic.root", logging.DEBUG, "Server started") in caplog.record_tuples
    assert ("sanic.root", logging.DEBUG, "Server stopped") in caplog.record_tuples

def test_run_with_logging(app, caplog):
    command = ['fake.server.app', '--repl', f'-p={get_port()}']
    
    with caplog.at_level(logging.DEBUG):
        run(app)

    assert ("sanic.root", logging.DEBUG, "Server started") in caplog.record_tuples
    assert ("sanic.root", logging.DEBUG, "Server stopped") in caplog.record_tuples

def test_run_with_invalid_port(app, caplog):
    command = ['fake.server.app', '--repl', '-p=invalid_port']
    
    with pytest.raises(SystemExit) as exit_exception:
        run(app)

    assert exit_exception.value.code == 1
    assert "Invalid port" in caplog.text