import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_when_multiple_files_are_changed(touch_soon) -> None:
    files = [Path("file1.py"), Path("file2.py"), Path("file3.py")]
    for file in files:
        file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        changes = _reload_tester(touch_soon, reloader, *files)
        assert set(changes) == set(files)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_when_no_files_are_changed(touch_soon) -> None:
    file = Path("unchanged_file.py")
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