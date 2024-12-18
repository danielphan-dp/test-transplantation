import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure, reloader_class):
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, pytest.param(WatchFilesReload, marks=pytest.mark.skipif(True, reason="Skip on M1"))])
    def test_should_reload_when_file_in_root_directory_is_modified(self, touch_soon):
        root_file = self.reload_path / "main.py"
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_dirs=[str(self.reload_path)])
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, root_file)

        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, pytest.param(WatchFilesReload, marks=pytest.mark.skipif(True, reason="Skip on M1"))])
    def test_should_not_reload_when_file_in_ignored_directory_is_modified(self, touch_soon):
        ignored_dir = self.reload_path / "ignored"
        ignored_file = ignored_dir / "ignored_file.py"
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_dirs=[str(self.reload_path)])
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, ignored_file)

        reloader.shutdown()

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    def _reload_tester(self, touch_soon, reloader: BaseReload, *files):
        reloader.restart()
        for file in files:
            touch_soon(file)
        return next(reloader)