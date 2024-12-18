import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload

@pytest.mark.parametrize("reloader_class", [BaseReload, WatchFilesReload])
def test_should_reload_on_file_change(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_dir_file = app_dir / "src" / "main.py"
    root_file = Path("main.py")

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    # Simulate file change
    app_dir_file.touch()
    assert self._reload_tester(touch_soon, reloader, app_dir_file)

    # Ensure root file does not trigger reload
    assert not self._reload_tester(touch_soon, reloader, root_file)

    reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [BaseReload, WatchFilesReload])
def test_should_not_reload_when_no_changes(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_dir_file = app_dir / "src" / "main.py"
    root_file = Path("main.py")

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    # No changes made, should not reload
    assert not self._reload_tester(touch_soon, reloader, app_dir_file)
    assert not self._reload_tester(touch_soon, reloader, root_file)

    reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [BaseReload, WatchFilesReload])
def test_should_reload_multiple_files(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_dir_file = app_dir / "src" / "main.py"
    another_file = app_dir / "src" / "another.py"

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    # Simulate changes in multiple files
    app_dir_file.touch()
    another_file.touch()
    assert self._reload_tester(touch_soon, reloader, app_dir_file, another_file)

    reloader.shutdown()