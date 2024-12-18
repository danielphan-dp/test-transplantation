import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_no_changes(touch_soon) -> None:
    reload_path = Path("path/to/reload")
    non_dotted_file = reload_path / "non_dotted_file.txt"
    non_dotted_file.touch()

    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=["*.txt"],
        )
        reloader = _setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, non_dotted_file) is None

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
            reload_excludes=["*.py"],
        )
        reloader = _setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2) is not None

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_dotted_files(touch_soon) -> None:
    reload_path = Path("path/to/reload")
    dotted_file = reload_path / ".dotted_file"
    dotted_file.touch()

    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=["*.py"],
        )
        reloader = _setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, dotted_file) is None

        reloader.shutdown()