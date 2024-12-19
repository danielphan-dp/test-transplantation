import logging
import pytest
from unittest.mock import Mock
from sanic.application.logo import BASE_LOGO
from sanic.application.motd import MOTD

@pytest.fixture
def mock_app():
    app = Mock()
    app.create_server.return_value = Mock()
    return app

def test_run_startup_logs_debug(mock_app, run_startup):
    logs = run_startup(mock_app)
    assert logs[0][1] == logging.DEBUG
    assert logs[0][2] == BASE_LOGO

def test_run_startup_no_logs(mock_app, caplog):
    mock_app.create_server.return_value = None
    logs = run_startup(mock_app)
    assert len(logs) == 0

def test_run_startup_with_custom_log(mock_app, caplog):
    mock_app.create_server.return_value = Mock()
    with caplog.at_level(logging.INFO):
        logs = run_startup(mock_app)
    assert logs[0][1] == logging.INFO

def test_run_startup_server_error(mock_app, caplog):
    mock_app.create_server.side_effect = Exception("Server error")
    with pytest.raises(Exception):
        run_startup(mock_app)
    assert "Server error" in caplog.text

def test_run_startup_multiple_logs(mock_app, run_startup):
    logs = run_startup(mock_app)
    assert len(logs) > 1
    assert all(log[1] == logging.DEBUG for log in logs)