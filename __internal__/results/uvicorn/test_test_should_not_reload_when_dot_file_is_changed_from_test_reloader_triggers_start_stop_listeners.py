import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_reload_when_non_dot_file_is_changed(touch_soon, reloader_class) -> None:
    file = Path("test_file.txt")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = reloader_class(config)

        assert self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_not_reload_when_file_is_deleted(touch_soon, reloader_class) -> None:
    file = Path("test_file_to_delete.txt")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = reloader_class(config)

        file.unlink()
        assert not self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [BaseReload, WatchFilesReload])
def test_should_reload_when_multiple_files_are_changed(touch_soon, reloader_class) -> None:
    file1 = Path("test_file1.txt")
    file2 = Path("test_file2.txt")
    file1.touch()
    file2.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = reloader_class(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2)

        reloader.shutdown()