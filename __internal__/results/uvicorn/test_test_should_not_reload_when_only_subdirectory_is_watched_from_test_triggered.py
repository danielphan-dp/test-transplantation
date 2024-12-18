import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_reload_when_file_is_touched(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_dir_file = app_dir / "src" / "main.py"
    root_file = Path("main.py")

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    # Ensure reloader restarts when the main app file is touched
    assert self._reload_tester(touch_soon, reloader, app_dir_file)

    # Ensure reloader does not restart when a non-watched file is touched
    assert not self._reload_tester(touch_soon, reloader, root_file)

    # Touch the app directory file to trigger reload
    app_dir_file.touch()
    assert self._reload_tester(touch_soon, reloader, app_dir_file)

    reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_not_reload_when_ignored_file_is_touched(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    ignored_file = app_dir / "ignored.py"
    app_dir_file = app_dir / "src" / "main.py"

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_excludes=[str(ignored_file)],
    )
    reloader = self._setup_reloader(config)

    # Ensure reloader does not restart when an ignored file is touched
    assert not self._reload_tester(touch_soon, reloader, ignored_file)

    # Ensure reloader restarts when the main app file is touched
    assert self._reload_tester(touch_soon, reloader, app_dir_file)

    reloader.shutdown()