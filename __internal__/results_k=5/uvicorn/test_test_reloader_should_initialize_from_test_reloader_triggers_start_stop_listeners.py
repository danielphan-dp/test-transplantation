import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path, reloader_class: type[BaseReload] | None):
        if reloader_class is None:  # pragma: no cover
            pytest.skip("Needed dependency not installed")
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    @pytest.mark.parametrize("reloader_class", [WatchGodReload, WatchFilesReload])
    def test_reloader_should_start_and_shutdown(self, reloader_class) -> None:
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            assert reloader is not None
            reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [WatchGodReload, WatchFilesReload])
    def test_reloader_should_trigger_startup(self, reloader_class) -> None:
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            assert reloader.should_exit.is_set() is False
            reloader.startup()
            assert reloader.should_exit.is_set() is False
            reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [WatchGodReload, WatchFilesReload])
    def test_reloader_should_handle_no_app(self, reloader_class) -> None:
        with as_cwd(self.reload_path):
            config = Config(app=None, reload=True)
            with pytest.raises(ValueError, match="Application must be provided"):
                self._setup_reloader(config)

    @pytest.mark.parametrize("reloader_class", [WatchGodReload, WatchFilesReload])
    def test_reloader_should_not_start_if_disabled(self, reloader_class) -> None:
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=False)
            reloader = self._setup_reloader(config)
            assert reloader is None

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader