import signal
import pytest
from unittest.mock import Mock
from pathlib import Path
from sanic.worker.reloader import Reloader

def test_run_reloader_with_timeout(app_loader):
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

    with pytest.raises(TimeoutError):
        run_reloader(reloader)

    assert len(paths) == 0
    publisher.send.assert_not_called()

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
    publisher.send.assert_not_called()

def test_run_reloader_with_multiple_files(app_loader):
    paths = set()

    def check_file(filename, mtimes):
        if isinstance(filename, Path):
            paths.add(str(filename))
            return True
        return False

    reload_dir = Path(__file__).parent.parent / "fake"
    publisher = Mock()
    reloader = Reloader(publisher, 0.1, {reload_dir}, app_loader)
    reloader.check_file = check_file  # type: ignore
    run_reloader(reloader)

    assert len(paths) > 0
    publisher.send.assert_called()
    call_arg = publisher.send.call_args_list[0][0][0]
    assert call_arg.startswith("__ALL_PROCESSES__:")
    assert call_arg.count(",") == len(paths) - 1
    for path in paths:
        assert str(path) in call_arg