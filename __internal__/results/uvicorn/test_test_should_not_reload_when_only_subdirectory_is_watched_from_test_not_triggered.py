import pytest
from unittest.mock import Mock
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload

@pytest.mark.parametrize("reloader_class", [BaseReload, WatchFilesReload])
def test_should_reload_when_file_is_touched(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_dir_file = app_dir / "src" / "main.py"
    app_dir_file.touch()
    
    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    assert self._reload_tester(touch_soon, reloader, app_dir_file)

    reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [BaseReload, WatchFilesReload])
def test_should_not_reload_when_file_is_not_touched(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_dir_file = app_dir / "src" / "main.py"
    root_file = Path("main.py")

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    assert not self._reload_tester(touch_soon, reloader, root_file)

    reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [BaseReload, WatchFilesReload])
def test_should_reload_multiple_files(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_dir_file1 = app_dir / "src" / "main.py"
    app_dir_file2 = app_dir / "src" / "utils.py"
    
    app_dir_file1.touch()
    app_dir_file2.touch()

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    assert self._reload_tester(touch_soon, reloader, app_dir_file1, app_dir_file2)

    reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [BaseReload, WatchFilesReload])
def test_should_not_reload_when_ignored_file_is_touched(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    ignored_file = app_dir / "ignored.py"
    ignored_file.touch()

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    assert not self._reload_tester(touch_soon, reloader, ignored_file)

    reloader.shutdown()