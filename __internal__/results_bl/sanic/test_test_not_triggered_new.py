import signal
import time
from unittest.mock import Mock
import pytest
from pathlib import Path
from sanic.worker.reloader import Reloader
from sanic.worker.loader import AppLoader

def test_triggered_reloader(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    def mock_reloader():
        publisher.send("reload")

    reloader = mock_reloader
    run_reloader(reloader)

    publisher.send.assert_called_once_with("reload")

def test_reloader_timeout(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    def mock_reloader():
        time.sleep(2)  # Simulate long-running task

    reloader = mock_reloader
    with pytest.raises(TimeoutError):
        run_reloader(reloader)

def test_reloader_stop_signal(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    def mock_reloader():
        time.sleep(0.5)  # Simulate some work

    reloader = mock_reloader
    run_reloader(reloader)

    # Ensure that the reloader can be stopped
    signal.alarm(0)  # Cancel the alarm
    publisher.send.assert_not_called()  # Ensure it didn't call send after stopping