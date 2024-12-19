import re
import signal
import threading
import asyncio
import logging
from pathlib import Path
from time import sleep
from unittest.mock import Mock
import pytest
from sanic.app import Sanic
from sanic.worker.constants import ProcessState, RestartOrder
from sanic.worker.loader import AppLoader
from sanic.worker.process import WorkerProcess
from sanic.worker.reloader import Reloader

def test_run_reloader_with_no_files(app_loader):
    paths = set()

    def check_file(filename, mtimes):
        return False

    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    reloader.check_file = check_file  # type: ignore
    run_reloader(reloader)

    assert len(paths) == 0
    publisher.send.assert_called()
    call_arg = publisher.send.call_args_list[0][0][0]
    assert call_arg.startswith("__ALL_PROCESSES__:")
    assert call_arg.count(",") == 1

def test_run_reloader_with_invalid_file(app_loader):
    paths = set()

    def check_file(filename, mtimes):
        if isinstance(filename, str) and "invalid_file.py" in filename:
            paths.add(str(filename))
            return True
        return False

    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    reloader.check_file = check_file  # type: ignore
    run_reloader(reloader)

    assert len(paths) == 1
    publisher.send.assert_called()
    call_arg = publisher.send.call_args_list[0][0][0]
    assert call_arg.startswith("__ALL_PROCESSES__:")
    assert call_arg.count(",") == 1
    assert str("invalid_file.py") in call_arg

def test_run_reloader_with_multiple_files(app_loader):
    paths = set()

    def check_file(filename, mtimes):
        if isinstance(filename, str) and filename in ["file1.py", "file2.py"]:
            paths.add(str(filename))
            return True
        return False

    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    reloader.check_file = check_file  # type: ignore
    run_reloader(reloader)

    assert len(paths) == 2
    publisher.send.assert_called()
    call_arg = publisher.send.call_args_list[0][0][0]
    assert call_arg.startswith("__ALL_PROCESSES__:")
    assert call_arg.count(",") == 1
    for path in paths:
        assert str(path) in call_arg

def test_run_reloader_timeout(app_loader):
    paths = set()

    def check_file(filename, mtimes):
        return False

    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    reloader.check_file = check_file  # type: ignore

    with pytest.raises(TimeoutError):
        run_reloader(reloader)