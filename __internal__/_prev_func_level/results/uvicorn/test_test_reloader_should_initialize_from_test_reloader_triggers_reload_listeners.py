import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload, WatchGodReload])
def test_reloader_should_start_and_shutdown(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert reloader is not None
        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload, WatchGodReload])
def test_reloader_should_trigger_on_file_change(reloader_class, touch_soon) -> None:
    file = self.reload_path / "test_file.py"
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        touch_soon(file)
        reloader.restart()
        assert reloader.should_restart() is not None
        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload, WatchGodReload])
def test_reloader_should_not_start_without_reload_flag(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=False)
        reloader = self._setup_reloader(config)
        assert reloader is None

@pytest.mark.parametrize('reloader_class', [WatchFilesReload, WatchGodReload])
def test_reloader_should_handle_exceptions(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        try:
            raise RuntimeError("Test exception")
        except RuntimeError:
            assert reloader is not None
            reloader.shutdown()