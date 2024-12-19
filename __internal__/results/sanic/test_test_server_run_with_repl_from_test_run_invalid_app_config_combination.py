import pytest
from unittest.mock import patch
from sanic.cli.app import run
from conftest import get_port

def test_server_run_with_repl_non_interactive(caplog, capsys):
    record = (
        "sanic.error",
        40,
        "Can't start REPL in non-interactive mode. "
        "You can only run with --repl in a TTY.",
    )

    def run_command():
        command = ["fake.server.app", "--repl", f"-p={get_port()}"]
        return capture(command, capsys=capsys)

    with patch("sanic.cli.app.is_atty", return_value=False):
        result = run_command()

    assert record in caplog.record_tuples
    assert "Welcome to the Sanic interactive console" not in result.err
    assert ">>> " not in result.out

def test_server_run_with_repl_interactive(caplog, capsys):
    record = (
        "sanic.error",
        40,
        "Can't start REPL in non-interactive mode. "
        "You can only run with --repl in a TTY.",
    )

    def run_command():
        command = ["fake.server.app", "--repl", f"-p={get_port()}"]
        return capture(command, capsys=capsys)

    with patch("sanic.cli.app.is_atty", return_value=True):
        result = run_command()

    assert record not in caplog.record_tuples
    assert "Welcome to the Sanic interactive console" in result.err
    assert ">>> " in result.out

    run_command()
    assert record in caplog.record_tuples

def test_server_run_with_invalid_port(caplog, capsys):
    invalid_port = -1  # Example of an invalid port
    command = ["fake.server.app", "--repl", f"-p={invalid_port}"]

    with pytest.raises(SystemExit) as exit_exception:
        capture(command, capsys=capsys)

    assert exit_exception.value.code == 1
    assert "Invalid port" in caplog.text

def test_server_run_with_missing_app(caplog, capsys):
    command = ["--repl", f"-p={get_port()}"]

    with pytest.raises(SystemExit) as exit_exception:
        capture(command, capsys=capsys)

    assert exit_exception.value.code == 1
    assert "You must pass the application" in caplog.text