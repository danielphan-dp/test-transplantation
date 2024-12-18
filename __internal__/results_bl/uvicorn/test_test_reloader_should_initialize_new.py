import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_should_initialize_with_different_classes(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert isinstance(reloader, BaseReload)
        reloader.shutdown()

def test_reloader_should_not_start_when_reload_is_false() -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=False)
        reloader = self._setup_reloader(config)
        assert not config.should_reload
        reloader.shutdown()

def test_reloader_should_raise_exception_on_invalid_config() -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        config.should_reload = False
        with pytest.raises(AssertionError):
            self._setup_reloader(config)

def test_reloader_should_handle_empty_sockets() -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert reloader.sockets == []
        reloader.shutdown()