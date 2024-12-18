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
    app_first_dir = Path("app_first")
    app_first_file = app_first_dir / "src" / "main.py"

    with as_cwd(Path(".")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir), str(app_first_dir)],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, app_file)
        assert self._reload_tester(touch_soon, reloader, app_first_file)

        # Test with a non-existent file
        non_existent_file = Path("non_existent_file.py")
        assert self._reload_tester(touch_soon, reloader, non_existent_file) is None

        # Test with an empty directory
        empty_dir = Path("empty_dir")
        empty_dir.mkdir(exist_ok=True)
        assert self._reload_tester(touch_soon, reloader, empty_dir) is None

        reloader.shutdown()