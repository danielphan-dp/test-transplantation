import logging
import pytest
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_handle_no_files_to_reload(touch_soon, caplog, tmp_path):
    app_dir = tmp_path / "app"
    app_dir.mkdir()
    
    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        result = self._reload_tester(touch_soon, reloader)
        assert result is None
        assert caplog.records[-1].levelno == logging.INFO
        assert caplog.records[-1].message == "No files to reload."

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_not_reload_if_no_changes(touch_soon, caplog, tmp_path):
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
        assert caplog.records[-1].levelno == logging.INFO
        assert caplog.records[-1].message == "No changes detected for reload."

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_multiple_files(touch_soon, caplog, tmp_path):
    app_dir = tmp_path / "app"
    app_file_1 = app_dir / "file1.py"
    app_file_2 = app_dir / "file2.py"
    app_dir.mkdir()
    app_file_1.touch()
    app_file_2.touch()
    
    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        assert self._reload_tester(touch_soon, reloader, app_file_1, app_file_2)
        app_file_1.touch()
        assert self._reload_tester(touch_soon, reloader, app_file_1, app_file_2)
        assert caplog.records[-1].levelno == logging.INFO
        assert caplog.records[-1].message == "Reloading due to changes in files."