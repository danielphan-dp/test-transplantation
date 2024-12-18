import pytest
from unittest.mock import Mock
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_when_python_file_in_included_dir_is_changed(self, touch_soon) -> None:
    included_dir = Path("app/included")
    included_file = included_dir / "included.py"
    included_dir.mkdir(parents=True, exist_ok=True)
    included_file.touch()

    with as_cwd(included_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, included_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_not_reload_when_file_is_deleted(self, touch_soon) -> None:
    temp_file = Path("temp_file.py")
    temp_file.touch()

    with as_cwd(temp_file.parent):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[],
        )
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, temp_file)

        temp_file.unlink()
        assert not self._reload_tester(touch_soon, reloader, temp_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_when_multiple_files_are_touched(self, touch_soon) -> None:
    dir_path = Path("app/multiple")
    file1 = dir_path / "file1.py"
    file2 = dir_path / "file2.py"
    dir_path.mkdir(parents=True, exist_ok=True)
    file1.touch()
    file2.touch()

    with as_cwd(dir_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2)

        reloader.shutdown()