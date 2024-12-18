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
def test_should_reload_on_file_touch(touch_soon, caplog, tmp_path):
    app_dir = tmp_path / "app"
    app_file = app_dir / "file.py"
    app_dir.mkdir()
    app_file.touch()

    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        
        assert self._reload_tester(touch_soon, reloader, app_file)

        app_file.touch()  # Simulate touching the file
        assert self._reload_tester(touch_soon, reloader, app_file)
        assert caplog.records[-1].levelno == logging.INFO
        assert caplog.records[-1].message == f"WatchGodReload detected a change in '{app_file.name}'; Reloading."

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_not_reload_on_no_changes(touch_soon, caplog, tmp_path):
    app_dir = tmp_path / "app"
    app_file = app_dir / "file.py"
    app_dir.mkdir()
    app_file.touch()

    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, app_file)

        sleep(0.2)  # Wait to ensure no changes are detected
        assert not self._reload_tester(touch_soon, reloader, app_file)
        assert caplog.records[-1].levelno == logging.DEBUG
        assert caplog.records[-1].message == f"No changes detected for '{app_file.name}'; No reload."

        reloader.shutdown()