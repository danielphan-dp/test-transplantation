import pytest
from unittest.mock import Mock
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from time import sleep

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_no_file_changes(touch_soon) -> None:
    reload_path = Path("path/to/reload")
    file_to_touch = reload_path / "main.py"
    file_to_touch.touch()

    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["main.py"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file_to_touch) is None

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_multiple_file_changes(touch_soon) -> None:
    reload_path = Path("path/to/reload")
    files_to_touch = [
        reload_path / ".dotted",
        reload_path / "ext" / "ext.jpg",
        reload_path / "main.py"
    ]

    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=[".dotted", "ext/ext.jpg", "main.py"],
        )
        reloader = self._setup_reloader(config)

        for file in files_to_touch:
            file.touch()
            assert self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_file_not_found(touch_soon) -> None:
    reload_path = Path("path/to/reload")
    non_existent_file = reload_path / "non_existent.py"

    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["non_existent.py"],
        )
        reloader = self._setup_reloader(config)

        with pytest.raises(FileNotFoundError):
            self._reload_tester(touch_soon, reloader, non_existent_file)

        reloader.shutdown()