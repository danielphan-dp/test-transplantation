import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [pytest.param(WatchFilesReload), WatchGodReload])
def test_reload_tester_edge_cases(touch_soon, reloader_class) -> None:
    empty_file = Path("empty_file.txt")
    non_existent_file = Path("non_existent_file.txt")
    dotted_file = Path(".dotted")
    
    with as_cwd(Path.cwd()):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=[".dotted", "empty_file.txt"],
        )
        reloader = self._setup_reloader(config)

        # Test with an empty file
        empty_file.touch()
        assert self._reload_tester(touch_soon, reloader, empty_file)

        # Test with a non-existent file
        assert self._reload_tester(touch_soon, reloader, non_existent_file) is None

        # Test with a dotted file
        assert self._reload_tester(touch_soon, reloader, dotted_file)

        reloader.shutdown()