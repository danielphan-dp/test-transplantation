import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils import as_cwd

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path, reloader_class: type[BaseReload] | None):
        if reloader_class is None:
            pytest.skip("Needed dependency not installed")
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reloader_should_not_start_when_reload_false(self, reloader_class, touch_soon):
        config = Config(app="tests.test_config:asgi_app", reload=False)
        reloader = self._setup_reloader(config)
        assert not config.should_reload
        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reloader_should_initialize_with_custom_delay(self, reloader_class, touch_soon):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_delay=1)
        reloader = self._setup_reloader(config)
        assert config.reload_delay == 1
        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reloader_should_handle_multiple_file_changes(self, reloader_class, touch_soon):
        file1 = self.reload_path / "file1.txt"
        file2 = self.reload_path / "file2.txt"
        
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)

            assert self._reload_tester(touch_soon, reloader, file1, file2)

            reloader.shutdown()

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    def _reload_tester(self, touch_soon, reloader: BaseReload, *files: Path):
        reloader.restart()
        for file in files:
            touch_soon(file)
        return next(reloader)