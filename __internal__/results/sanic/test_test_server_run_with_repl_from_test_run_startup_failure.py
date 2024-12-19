import pytest
from unittest.mock import patch
from conftest import get_port
from sanic.cli.app import capture

def test_server_run_with_repl_interactive_mode(caplog, capsys):
    record = (
        "sanic.error",
        40,
        "Can't start REPL in non-interactive mode. "
        "You can only run with --repl in a TTY.",
    )

    def run():
        command = ["fake.server.app", "--repl", f"-p={get_port()}"]
        return capture(command, capsys=capsys)

    with patch("sanic.cli.app.is_atty", return_value=True):
        result = run()

    assert record not in caplog.record_tuples
    assert "Welcome to the Sanic interactive console" in result.err
    assert ">>> " in result.out

def test_server_run_with_repl_non_interactive_mode(caplog, capsys):
    record = (
        "sanic.error",
        40,
        "Can't start REPL in non-interactive mode. "
        "You can only run with --repl in a TTY.",
    )

    def run():
        command = ["fake.server.app", "--repl", f"-p={get_port()}"]
        return capture(command, capsys=capsys)

    with patch("sanic.cli.app.is_atty", return_value=False):
        run()
        assert record in caplog.record_tuples

def test_server_run_with_invalid_port(caplog, capsys):
    record = (
        "sanic.error",
        40,
        "Invalid port specified.",
    )

    def run():
        command = ["fake.server.app", "--repl", "--port=invalid"]
        return capture(command, capsys=capsys)

    with patch("sanic.cli.app.is_atty", return_value=True):
        run()
        assert record in caplog.record_tuples

def test_server_run_without_repl(caplog, capsys):
    record = (
        "sanic.error",
        40,
        "REPL mode is not enabled.",
    )

    def run():
        command = ["fake.server.app", "-p={get_port()}"]
        return capture(command, capsys=capsys)

    with patch("sanic.cli.app.is_atty", return_value=True):
        result = run()

    assert record not in caplog.record_tuples
    assert "Server started" in result.err
    assert "Listening on" in result.out