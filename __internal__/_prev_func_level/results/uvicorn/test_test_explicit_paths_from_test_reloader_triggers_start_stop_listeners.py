import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_no_changes(touch_soon) -> None:
    file_to_touch = Path("test_file.txt")
    file_to_touch.touch()

    with as_cwd(Path.cwd()):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["test_file.txt"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file_to_touch) is None

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_multiple_files(touch_soon) -> None:
    file1 = Path("file1.txt")
    file2 = Path("file2.txt")
    file1.touch()
    file2.touch()

    with as_cwd(Path.cwd()):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["file1.txt", "file2.txt"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2) is not None

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_tester_with_dotted_file(touch_soon) -> None:
    dotted_file = Path(".dotted_file")
    dotted_file.touch()

    with as_cwd(Path.cwd()):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=[".dotted_file"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, dotted_file) is not None

        reloader.shutdown()