import signal
import time
import pytest
from unittest.mock import Mock
from pathlib import Path
from sanic.worker.reloader import Reloader

def test_run_reloader_stops_after_timeout(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    
    def mock_reloader():
        time.sleep(0.5)  # Simulate some work being done

    reloader.__call__ = mock_reloader  # Override the call method
    run_reloader(reloader)

    assert publisher.send.called
    call_arg = publisher.send.call_args_list[0][0][0]
    assert call_arg.startswith("__ALL_PROCESSES__:")
    assert call_arg.count(",") == 1

def test_run_reloader_does_not_stop_if_not_called(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    def stop_reloader():
        reloader.stop()

    signal.signal(signal.SIGALRM, stop_reloader)
    signal.alarm(1)
    
    # Simulate not calling the reloader
    time.sleep(2)  # Wait longer than the alarm to ensure it doesn't stop

    assert not publisher.send.called

def test_run_reloader_with_no_files(app_loader):
    reload_dir = Path(__file__).parent.parent / "empty_fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    run_reloader(reloader)

    assert publisher.send.called
    call_arg = publisher.send.call_args_list[0][0][0]
    assert call_arg.startswith("__ALL_PROCESSES__:")
    assert call_arg.count(",") == 1
    assert "unknown" in call_arg  # Expecting 'unknown' since no files were found

def test_run_reloader_with_multiple_files(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    def check_file(filename, mtimes):
        return True  # Simulate that all files are valid for reloading

    reloader.check_file = check_file  # Override the check_file method
    run_reloader(reloader)

    assert publisher.send.called
    call_arg = publisher.send.call_args_list[0][0][0]
    assert call_arg.startswith("__ALL_PROCESSES__:")
    assert call_arg.count(",") > 1  # Expecting multiple files to be reloaded