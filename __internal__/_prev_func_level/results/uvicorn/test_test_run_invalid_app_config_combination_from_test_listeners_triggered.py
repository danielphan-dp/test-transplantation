import pytest
import logging
from uvicorn.main import run

def test_run_with_empty_sockets(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit) as exit_exception:
        run([])
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].message == "No sockets provided."

def test_run_with_invalid_socket_type(caplog: pytest.LogCaptureFixture) -> None:
    invalid_socket = "invalid_socket"
    with pytest.raises(SystemExit) as exit_exception:
        run([invalid_socket])
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].message == "Invalid socket type provided."

def test_run_with_multiple_sockets(caplog: pytest.LogCaptureFixture) -> None:
    sockets = [("127.0.0.1", 8000), ("127.0.0.1", 8001)]
    with pytest.raises(SystemExit) as exit_exception:
        run(sockets)
    assert exit_exception.value.code == 0
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.INFO
    assert "Started server" in caplog.records[-1].message

def test_run_with_socket_error(caplog: pytest.LogCaptureFixture) -> None:
    sockets = [("invalid_host", 8000)]
    with pytest.raises(SystemExit) as exit_exception:
        run(sockets)
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.ERROR
    assert "Error starting server" in caplog.records[-1].message