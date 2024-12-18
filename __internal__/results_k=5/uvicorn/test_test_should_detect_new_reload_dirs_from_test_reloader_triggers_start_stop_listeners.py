import logging
import pytest
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_no_changes(touch_soon, caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    app_dir = tmp_path / "app"
    app_file = app_dir / "file.py"
    app_dir.mkdir()
    app_file.touch()

    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        assert self._reload_tester(touch_soon, reloader, app_file) is not None

        assert caplog.records[-1].levelno == logging.INFO
        assert caplog.records[-1].message == "No changes detected; reloader will not restart."

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_multiple_files(touch_soon, caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    app_dir = tmp_path / "app"
    app_file1 = app_dir / "file1.py"
    app_file2 = app_dir / "file2.py"
    app_dir.mkdir()
    app_file1.touch()
    app_file2.touch()

    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        assert self._reload_tester(touch_soon, reloader, app_file1, app_file2) is not None

        app_file1.touch()
        assert self._reload_tester(touch_soon, reloader, app_file1) is not None

        app_file2.touch()
        assert self._reload_tester(touch_soon, reloader, app_file2) is not None

        assert caplog.records[-1].levelno == logging.INFO
        assert "detected changes" in caplog.records[-1].message

        reloader.shutdown()