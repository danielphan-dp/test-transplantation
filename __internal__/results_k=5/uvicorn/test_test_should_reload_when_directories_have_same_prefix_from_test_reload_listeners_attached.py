import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_should_reload_with_different_reloader_classes(touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file = app_dir / "src" / "main.py"
    
    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, app_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_should_not_reload_when_reload_is_false(touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file = app_dir / "src" / "main.py"
    
    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=False,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, app_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_should_reload_when_file_is_modified(touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file = app_dir / "src" / "main.py"
    
    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        touch_soon(app_file)
        assert self._reload_tester(touch_soon, reloader, app_file)

        reloader.shutdown()