import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path, reloader_class: type[BaseReload] | None):
        if reloader_class is None:
            pytest.skip("Needed dependency not installed")
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reloader_should_initialize_with_different_classes(self, reloader_class, touch_soon):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert isinstance(reloader, reloader_class)
        reloader.shutdown()

    @pytest.mark.parametrize("file_name", ["test_file.py", "test_file.txt", ".hidden_file"])
    def test_reload_with_various_file_types(self, file_name, touch_soon):
        test_file = self.reload_path / file_name
        test_file.touch()  # Create the file

        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)

            assert self._reload_tester(touch_soon, reloader, test_file)
            reloader.shutdown()

    def test_reloader_should_not_start_when_reload_is_false(self, touch_soon):
        config = Config(app="tests.test_config:asgi_app", reload=False)
        reloader = self._setup_reloader(config)
        assert not config.should_reload
        reloader.shutdown()

    def test_reloader_should_handle_empty_sockets(self, touch_soon):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        reloader.shutdown()