import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_when_python_file_in_included_subdir_is_changed(self, touch_soon) -> None:
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
def test_should_not_reload_when_non_python_file_is_changed(self, touch_soon) -> None:
    non_python_file = Path("app/non_python_file.txt")
    non_python_file.touch()

    with as_cwd(non_python_file.parent):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[],
        )
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, non_python_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_when_multiple_files_are_changed(self, touch_soon) -> None:
    included_dir = Path("app/multiple")
    included_file1 = included_dir / "file1.py"
    included_file2 = included_dir / "file2.py"
    included_dir.mkdir(parents=True, exist_ok=True)
    included_file1.touch()
    included_file2.touch()

    with as_cwd(included_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, included_file1, included_file2)

        reloader.shutdown()