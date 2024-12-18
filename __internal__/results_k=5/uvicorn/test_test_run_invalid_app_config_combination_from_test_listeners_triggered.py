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
    with pytest.raises(SystemExit) as exit_exception:
        run(["invalid_socket"])
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].message == "Invalid socket type provided."

def test_run_with_multiple_sockets(caplog: pytest.LogCaptureFixture) -> None:
    sockets = [("127.0.0.1", 8000), ("127.0.0.1", 8001)]
    with caplog.at_level(logging.INFO):
        run(sockets)
    assert "Server running on" in caplog.text

def test_run_with_socket_error(caplog: pytest.LogCaptureFixture) -> None:
    sockets = [("127.0.0.1", 9999)]  # Assuming this port is already in use
    with pytest.raises(SystemExit) as exit_exception:
        run(sockets)
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.ERROR
    assert "Address already in use" in caplog.records[-1].message