import pytest
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [pytest.param(WatchFilesReload), WatchGodReload])
def test_should_reload_when_file_is_touched(self, touch_soon, reloader_class) -> None:
    python_file = self.reload_path / "app" / "src" / "main.py"
    css_file = self.reload_path / "app" / "css" / "main.css"
    js_file = self.reload_path / "app" / "js" / "main.js"

    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*"],
            reload_excludes=["*.js"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, python_file)
        assert self._reload_tester(touch_soon, reloader, css_file)

        # Touch the js file and check it does not trigger a reload
        js_file.touch()
        assert not self._reload_tester(touch_soon, reloader, js_file)

        # Test with a non-existent file
        non_existent_file = self.reload_path / "app" / "non_existent_file.py"
        assert not self._reload_tester(touch_soon, reloader, non_existent_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [pytest.param(WatchFilesReload), WatchGodReload])
def test_should_not_reload_when_no_files_are_touched(self, touch_soon, reloader_class) -> None:
    python_file = self.reload_path / "app" / "src" / "main.py"
    css_file = self.reload_path / "app" / "css" / "main.css"

    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*"],
            reload_excludes=["*.js"],
        )
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, python_file)
        assert not self._reload_tester(touch_soon, reloader, css_file)

        reloader.shutdown()