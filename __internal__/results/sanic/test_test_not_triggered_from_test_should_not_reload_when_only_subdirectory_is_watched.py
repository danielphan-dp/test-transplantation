import signal
import pytest
from unittest.mock import Mock
from pathlib import Path
from sanic.worker.reloader import Reloader

def test_should_trigger_reload_on_file_change(app_loader, touch_soon):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)

    # Simulate a file change
    touch_soon(reload_dir / "changed_file.py")

    # Run the reloader
    run_reloader(reloader)

    # Assert that the publisher sends a reload signal
    publisher.send.assert_called_once()

def test_should_not_reload_when_no_changes(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    
    # Run the reloader without any changes
    run_reloader(reloader)

    # Assert that the publisher does not send a reload signal
    publisher.send.assert_not_called()