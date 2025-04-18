import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_not_reload_when_no_file_changes(self, touch_soon) -> None:
    file = Path("app/sub/sub.py")
    file.touch()  # Create the file first

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file) is None

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_reload_when_multiple_files_changed(self, touch_soon) -> None:
    file1 = Path("app/sub/file1.py")
    file2 = Path("app/sub/file2.py")
    file1.touch()
    file2.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2)

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_reload_when_file_touched_after_delay(self, touch_soon) -> None:
    file = Path("app/sub/delayed.py")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        sleep(0.2)  # Wait before touching the file
        file.touch()
        assert self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()