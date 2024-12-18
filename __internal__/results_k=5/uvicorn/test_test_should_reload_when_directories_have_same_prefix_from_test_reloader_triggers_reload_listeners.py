import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_reload_with_various_reloader_classes(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_file = app_dir / "src" / "main.py"
    non_dotted_file = app_dir / "non_dotted_file.py"
    
    with as_cwd(app_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = reloader_class(config)

        assert self._reload_tester(touch_soon, reloader, app_file)
        assert self._reload_tester(touch_soon, reloader, non_dotted_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_not_reload_when_no_changes(touch_soon, reloader_class) -> None:
    app_dir = Path("app")
    app_file = app_dir / "src" / "main.py"
    
    with as_cwd(app_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = reloader_class(config)

        assert self._reload_tester(touch_soon, reloader, app_file) is None

        reloader.shutdown()