import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class, result", [(BaseReload, False), (WatchFilesReload, True)])
def test_reload_when_file_is_touched(reloader_class, result, touch_soon) -> None:
    file = Path("test_file.js")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = reloader_class(config)

        assert bool(_reload_tester(touch_soon, reloader, file)) == result

        file.touch()  # Simulate file change
        assert bool(_reload_tester(touch_soon, reloader, file)) == result

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [WatchFilesReload])
def test_reload_no_changes(reloader_class, touch_soon) -> None:
    file = Path("test_file_no_change.js")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = reloader_class(config)

        assert next(reloader) is None  # No changes should not trigger a reload

        reloader.shutdown()