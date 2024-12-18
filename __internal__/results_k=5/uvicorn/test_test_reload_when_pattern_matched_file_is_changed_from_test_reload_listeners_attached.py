import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path, reloader_class: type[BaseReload] | None):
        if reloader_class is None:
            pytest.skip("Needed dependency not installed")
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    @pytest.mark.parametrize("reloader_class, expected_should_reload", [
        (StatReload, True),
        (WatchFilesReload, True),
        (WatchGodReload, True)
    ])
    def test_reloader_initialization_should_reload(self, reloader_class, expected_should_reload):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert config.should_reload == expected_should_reload
        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload, WatchGodReload])
    def test_reloader_should_not_reload_when_disabled(self, reloader_class):
        config = Config(app="tests.test_config:asgi_app", reload=False)
        reloader = self._setup_reloader(config)
        assert not config.should_reload
        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload])
    def test_reloader_should_restart_on_file_change(self, reloader_class, touch_soon):
        file = self.reload_path / "app" / "js" / "main.js"
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
            reloader = self._setup_reloader(config)
            assert bool(self._reload_tester(touch_soon, reloader, file))
            reloader.shutdown()

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    def _reload_tester(self, touch_soon, reloader: BaseReload, *files: Path) -> list[Path] | None:
        reloader.restart()
        for file in files:
            touch_soon(file)
        return next(reloader)