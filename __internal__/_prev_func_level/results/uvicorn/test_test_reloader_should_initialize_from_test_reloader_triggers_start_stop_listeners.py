import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_should_start_and_shutdown(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert reloader is not None
        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_should_trigger_startup(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert config.should_reload
        reloader.startup()
        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload])
def test_reloader_should_not_start_if_not_configured(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=False)
        reloader = self._setup_reloader(config)
        assert not config.should_reload
        reloader.shutdown()