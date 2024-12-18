import pytest
import logging
from uvicorn.main import run

def test_run_with_empty_sockets(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit) as exit_exception:
        run(sockets=[])
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].message == "No sockets provided."

def test_run_with_invalid_socket_type(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit) as exit_exception:
        run(sockets=["invalid_socket"])
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].message == "Invalid socket type provided."

def test_run_with_none_sockets(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit) as exit_exception:
        run(sockets=None)
    assert exit_exception.value.code == 1
    assert caplog.records[-1].name == "uvicorn.error"
    assert caplog.records[-1].levelno == logging.WARNING
    assert caplog.records[-1].message == "No sockets provided."