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
def test_reload_tester_edge_cases(touch_soon, caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    app_dir = tmp_path / "app"
    app_file = app_dir / "file.py"
    app_dir.mkdir()
    app_file.touch()
    
    # Test with no files
    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        assert self._reload_tester(touch_soon, reloader) is None

        # Test with a non-existent file
        non_existent_file = app_dir / "non_existent.py"
        assert self._reload_tester(touch_soon, reloader, non_existent_file) is None
        assert caplog.records[-1].levelno == logging.WARNING
        assert caplog.records[-1].message == f"File '{non_existent_file}' does not exist."

        # Test with multiple files
        app_second_file = app_dir / "file2.py"
        app_second_file.touch()
        assert self._reload_tester(touch_soon, reloader, app_file, app_second_file)

        # Test with a directory instead of a file
        assert self._reload_tester(touch_soon, reloader, app_dir)

        reloader.shutdown()