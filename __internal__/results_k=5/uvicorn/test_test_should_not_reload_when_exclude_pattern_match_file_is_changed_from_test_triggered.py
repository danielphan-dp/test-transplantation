import pytest
from unittest.mock import Mock
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils import as_cwd

@pytest.mark.parametrize("reloader_class", [pytest.param(WatchFilesReload)])
def test_should_reload_when_included_file_is_changed(touch_soon) -> None:
    python_file = Path("app/src/main.py")
    included_file = Path("app/css/main.css")

    with as_cwd(Path(".")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=["*.css"],
            reload_excludes=["*.js"],
        )
        reloader = _setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, included_file)
        assert not self._reload_tester(touch_soon, reloader, python_file)

        reloader.shutdown()

def test_should_not_reload_when_no_files_are_touched(touch_soon) -> None:
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

def test_should_reload_when_multiple_files_are_touched(touch_soon) -> None:
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

        reloader.shutdown()