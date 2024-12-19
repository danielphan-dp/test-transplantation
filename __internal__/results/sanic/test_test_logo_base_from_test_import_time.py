import logging
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_app():
    app = Mock()
    return app

@pytest.mark.asyncio
async def test_run_startup_logs(mock_app, run_startup):
    logs = run_startup(mock_app)

    assert logs[0][1] == logging.DEBUG
    assert logs[0][2] == "Starting server"  # Assuming this is a log message you expect

@pytest.mark.asyncio
async def test_run_startup_no_server(mock_app, run_startup):
    mock_app.create_server.return_value = None
    logs = run_startup(mock_app)

    assert logs[0][1] == logging.ERROR
    assert "No server created" in logs[0][2]  # Assuming this is the expected error log

@pytest.mark.asyncio
async def test_run_startup_with_custom_port(mock_app, run_startup):
    mock_app.create_server.return_value = Mock()
    logs = run_startup(mock_app)

    assert logs[0][1] == logging.DEBUG
    assert "Server running on port" in logs[0][2]  # Assuming this is a log message you expect

@pytest.mark.asyncio
async def test_run_startup_exception_handling(mock_app, run_startup):
    mock_app.create_server.side_effect = Exception("Server error")
    logs = run_startup(mock_app)

    assert logs[0][1] == logging.ERROR
    assert "Server error" in logs[0][2]  # Assuming this is the expected error log

@pytest.mark.asyncio
async def test_run_startup_multiple_logs(mock_app, run_startup):
    mock_app.create_server.return_value = Mock()
    logs = run_startup(mock_app)

    assert len(logs) > 1  # Ensure multiple log entries are captured
    assert logs[0][1] == logging.DEBUG
    assert logs[-1][1] == logging.INFO  # Assuming the last log is an info log