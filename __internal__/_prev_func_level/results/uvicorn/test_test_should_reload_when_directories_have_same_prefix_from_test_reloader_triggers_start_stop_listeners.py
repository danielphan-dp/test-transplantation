import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_reload_with_various_reloader_classes(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_file = app_dir / "src" / "main.py"
    app_first_dir = Path("app_first")
    app_first_file = app_first_dir / "src" / "main.py"

    with as_cwd(Path(".")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir), str(app_first_dir)],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, app_file)
        assert self._reload_tester(touch_soon, reloader, app_first_file)

        # Test with no changes to ensure no reload occurs
        assert reloader.should_restart() is None

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_not_reload_when_no_changes(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_file = app_dir / "src" / "main.py"

    with as_cwd(Path(".")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        # Simulate no changes
        assert reloader.should_restart() is None

        reloader.shutdown()