import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_when_python_file_in_included_subdir_is_changed(self, touch_soon) -> None:
    included_sub_dir = Path("app/included")
    included_file = included_sub_dir / "included.py"
    included_sub_dir.mkdir(parents=True, exist_ok=True)
    included_file.touch()

    with as_cwd(included_sub_dir):
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
    sub_dir = Path("app/multiple_changes")
    sub_dir.mkdir(parents=True, exist_ok=True)
    file1 = sub_dir / "file1.py"
    file2 = sub_dir / "file2.py"
    file1.touch()
    file2.touch()

    with as_cwd(sub_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2)

        reloader.shutdown()