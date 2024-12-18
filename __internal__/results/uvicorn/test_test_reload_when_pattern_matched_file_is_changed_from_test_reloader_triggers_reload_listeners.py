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

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    @pytest.mark.parametrize("reloader_class, expected", [
        (StatReload, True),
        (WatchFilesReload, True),
        (WatchGodReload, False)
    ])
    def test_reloader_initialization(self, reloader_class, expected):
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            assert isinstance(reloader, reloader_class) == expected
            reloader.shutdown()

    @pytest.mark.parametrize("file_name, result", [
        ("main.py", True),
        ("app.js", True),
        ("non_existent_file.py", False)
    ])
    def test_reload_when_file_changes(self, file_name, result, touch_soon):
        file = self.reload_path / file_name

        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.py", "*.js"])
            reloader = self._setup_reloader(config)

            assert bool(self._reload_tester(touch_soon, reloader, file)) == result

            reloader.shutdown()

    def test_reloader_should_not_start_if_not_configured(self):
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=False)
            reloader = self._setup_reloader(config)
            assert not config.should_reload
            reloader.shutdown()