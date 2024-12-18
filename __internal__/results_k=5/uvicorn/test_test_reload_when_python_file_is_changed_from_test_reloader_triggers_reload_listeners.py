import pytest
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_when_multiple_files_are_changed(touch_soon) -> None:
    file1 = Path("test_file1.py")
    file2 = Path("test_file2.py")

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        changes = _reload_tester(touch_soon, reloader, file1, file2)
        assert changes == [file1, file2]

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_when_no_files_are_changed(touch_soon) -> None:
    file = Path("test_file.py")

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        changes = _reload_tester(touch_soon, reloader, file)
        assert changes is None

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_with_invalid_file(touch_soon) -> None:
    invalid_file = Path("invalid_file.py")

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        changes = _reload_tester(touch_soon, reloader, invalid_file)
        assert changes is None

        reloader.shutdown()