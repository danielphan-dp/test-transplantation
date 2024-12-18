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

        # Initial touch to simulate file change
        assert self._reload_tester(touch_soon, reloader, file) is not None

        # Simulate no changes
        assert self._reload_tester(touch_soon, reloader, file) is None

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_reload_multiple_files(self, touch_soon) -> None:
    file1 = Path("app/sub/file1.py")
    file2 = Path("app/sub/file2.py")
    file1.touch()
    file2.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2) is not None

        # Touch both files to trigger reload
        file1.touch()
        file2.touch()
        assert self._reload_tester(touch_soon, reloader, file1, file2) is not None

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_reload_when_file_is_deleted(self, touch_soon) -> None:
    file = Path("app/sub/sub.py")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file) is not None

        # Delete the file and check if it triggers a reload
        file.unlink()
        assert self._reload_tester(touch_soon, reloader, file) is not None

        reloader.shutdown()