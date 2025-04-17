import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from time import sleep

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_when_multiple_files_are_changed(touch_soon) -> None:
    files = [Path("file1.py"), Path("file2.py")]
    for file in files:
        file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        changes = _reload_tester(touch_soon, reloader, *files)
        assert changes == files

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_when_no_files_are_changed(touch_soon) -> None:
    file = Path("main.py")
    file.touch()

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