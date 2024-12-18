import pytest
from unittest.mock import Mock
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from time import sleep

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_no_changes(touch_soon) -> None:
    reload_path = Path("path/to/reload")
    file_to_touch = reload_path / "file.txt"
    file_to_touch.touch()

    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*.txt"],
            reload_excludes=["*.py"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file_to_touch) is None

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_multiple_files(touch_soon) -> None:
    reload_path = Path("path/to/reload")
    file1 = reload_path / "file1.txt"
    file2 = reload_path / "file2.txt"
    file1.touch()
    file2.touch()

    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*.txt"],
            reload_excludes=["*.py"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2) is not None

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_non_existent_file(touch_soon) -> None:
    reload_path = Path("path/to/reload")
    non_existent_file = reload_path / "non_existent.txt"

    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*.txt"],
            reload_excludes=["*.py"],
        )
        reloader = self._setup_reloader(config)

        with pytest.raises(FileNotFoundError):
            self._reload_tester(touch_soon, reloader, non_existent_file)

        reloader.shutdown()