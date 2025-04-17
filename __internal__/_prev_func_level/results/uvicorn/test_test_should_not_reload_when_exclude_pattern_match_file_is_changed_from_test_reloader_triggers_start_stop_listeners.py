import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [pytest.param(WatchFilesReload)])
def test_should_reload_when_included_file_is_changed(self, touch_soon) -> None:
    python_file = Path("app/src/main.py")
    included_file = Path("app/css/main.css")

    with as_cwd(Path("app")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*.css"],
            reload_excludes=["*.js"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, included_file)
        assert not self._reload_tester(touch_soon, reloader, python_file)

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [pytest.param(WatchFilesReload)])
def test_should_not_reload_when_no_files_are_touched(self, touch_soon) -> None:
    python_file = Path("app/src/main.py")
    css_file = Path("app/css/main.css")

    with as_cwd(Path("app")):
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