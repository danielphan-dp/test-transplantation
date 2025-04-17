import signal
import pytest
from unittest.mock import Mock
from pathlib import Path
from sanic.worker.reloader import Reloader

def test_triggered_reloader(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    # Simulate a file change to trigger the reloader
    reloader.check_file = Mock(return_value=True)
    reloader()

    publisher.send.assert_called_once()

def test_reloader_stops_on_alarm(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    # Set up a signal to stop the reloader
    def stop_reloader():
        reloader.stop()

    signal.signal(signal.SIGALRM, lambda *args: stop_reloader())
    signal.alarm(1)

    reloader()
    assert not reloader.run

def test_reloader_does_not_trigger_without_changes(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    # Simulate no file changes
    reloader.check_file = Mock(return_value=False)
    reloader()

    publisher.send.assert_not_called()