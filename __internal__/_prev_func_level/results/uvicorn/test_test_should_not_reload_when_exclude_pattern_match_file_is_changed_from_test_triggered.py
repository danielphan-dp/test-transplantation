import pytest
from unittest.mock import Mock
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_reload_when_file_is_touched(touch_soon) -> None:
    python_file = Path("app/src/main.py")
    css_file = Path("app/css/main.css")
    js_file = Path("app/js/main.js")

    with as_cwd(Path(".")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*"],
            reload_excludes=["*.js"],
        )
        reloader = _setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, python_file)
        assert self._reload_tester(touch_soon, reloader, css_file)
        assert not self._reload_tester(touch_soon, reloader, js_file)

        # Touch the python file to trigger a reload
        python_file.touch()
        assert self._reload_tester(touch_soon, reloader, python_file)

        # Touch the css file to trigger a reload
        css_file.touch()
        assert self._reload_tester(touch_soon, reloader, css_file)

        # Ensure js file does not trigger a reload
        js_file.touch()
        assert not self._reload_tester(touch_soon, reloader, js_file)

        reloader.shutdown()

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_should_not_reload_when_no_changes(touch_soon) -> None:
    python_file = Path("app/src/main.py")
    css_file = Path("app/css/main.css")

    with as_cwd(Path(".")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*"],
            reload_excludes=["*.js"],
        )
        reloader = _setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, python_file)
        assert not self._reload_tester(touch_soon, reloader, css_file)

        reloader.shutdown()