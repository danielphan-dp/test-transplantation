import signal
import pytest
from unittest.mock import Mock
from pathlib import Path
from sanic.worker.reloader import Reloader
from sanic.worker.loader import AppLoader

def test_run_reloader_stops_after_timeout(app_loader):
    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    
    def mock_reloader():
        pass
    
    reloader.stop = Mock()
    signal.signal(signal.SIGALRM, lambda *_: reloader.stop())
    signal.alarm(1)
    
    run_reloader(mock_reloader)
    
    reloader.stop.assert_called_once()

def test_run_reloader_calls_publisher_on_change(app_loader):
    paths = set()

    def check_file(filename, mtimes):
        if (isinstance(filename, Path) and (filename.name == "server.py")) or (
            isinstance(filename, str) and "sanic/app.py" in filename
        ):
            paths.add(str(filename))
            return True
        return False

    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    reloader.check_file = check_file  # type: ignore
    
    def mock_reloader():
        pass
    
    run_reloader(reloader)

    assert len(paths) == 2
    publisher.send.assert_called()
    call_arg = publisher.send.call_args_list[0][0][0]
    assert call_arg.startswith("__ALL_PROCESSES__:")
    assert call_arg.count(",") == 1
    for path in paths:
        assert str(path) in call_arg

def test_run_reloader_does_not_call_publisher_when_no_changes(app_loader):
    publisher = Mock()
    reload_dir = Path(__file__).parent.parent / "fake"
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    
    def mock_reloader():
        pass
    
    reloader.check_file = lambda filename, mtimes: False  # No files to check
    run_reloader(reloader)

    publisher.send.assert_not_called()