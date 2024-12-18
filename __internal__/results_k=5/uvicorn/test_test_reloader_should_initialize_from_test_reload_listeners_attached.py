import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_should_startup_and_shutdown(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert reloader is not None
        assert config.should_reload
        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload])
def test_reloader_should_handle_no_app(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app=None, reload=True)
        with pytest.raises(ValueError, match="Application must be provided"):
            self._setup_reloader(config)

@pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload])
def test_reloader_should_not_start_if_not_reload(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=False)
        reloader = self._setup_reloader(config)
        assert reloader is None

@pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload])
def test_reloader_should_set_reload_delay(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_delay=1)
        reloader = self._setup_reloader(config)
        assert config.reload_delay == 1
        reloader.shutdown()