import logging
import pytest
from pathlib import Path
from time import sleep
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_not_trigger_on_no_changes(touch_soon, caplog, tmp_path):
    app_dir = tmp_path / "app"
    app_file = app_dir / "file.py"
    app_dir.mkdir()
    app_file.touch()

    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        assert self._reload_tester(touch_soon, reloader, app_file)

        # Simulate no changes
        assert reloader.should_restart() is None
        assert caplog.records[-1].levelno == logging.DEBUG
        assert caplog.records[-1].message == "No changes detected, reloader will not restart."

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_handle_multiple_file_changes(touch_soon, caplog, tmp_path):
    app_dir = tmp_path / "app"
    app_file1 = app_dir / "file1.py"
    app_file2 = app_dir / "file2.py"
    app_dir.mkdir()
    app_file1.touch()
    app_file2.touch()

    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        assert self._reload_tester(touch_soon, reloader, app_file1)
        assert self._reload_tester(touch_soon, reloader, app_file2)

        app_file1.touch()
        app_file2.touch()
        assert reloader.should_restart() is not None

        assert caplog.records[-1].levelno == logging.INFO
        assert caplog.records[-1].message == "WatchGodReload detected changes in files; restarting."

        reloader.shutdown()