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
        result = run(app, command)
    
    assert "Welcome to the Sanic interactive console" in result.err
    assert ">>> " in result.out

def test_run_invalid_app_config_combination(caplog, app):
    with pytest.raises(SystemExit) as exit_exception:
        run(app, reload=True)
    
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].message == (
        "You must pass the application as an import string to enable "
        "'reload' or 'workers'."
    )

def test_run_without_repl(caplog, app):
    command = ['fake.server.app', '-p={get_port()}']
    
    with caplog.at_level(logging.DEBUG):
        run(app, command)
    
    assert ("sanic.root", logging.DEBUG, "Server started") in caplog.record_tuples

def test_run_with_invalid_port(caplog, app):
    command = ['fake.server.app', '--repl', '-p=invalid_port']
    
    with pytest.raises(SystemExit) as exit_exception:
        run(app, command)
    
    assert exit_exception.value.code == 1
    assert "Invalid port" in caplog.text

def test_run_with_logging(caplog, app):
    command = ['fake.server.app', '--repl', f'-p={get_port()}']
    
    with caplog.at_level(logging.INFO):
        run(app, command)
    
    assert ("sanic.root", logging.INFO, "Server is running") in caplog.record_tuples