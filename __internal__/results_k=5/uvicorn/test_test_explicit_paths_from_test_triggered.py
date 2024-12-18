import pytest
from unittest.mock import Mock
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [pytest.param(WatchFilesReload)])
def test_reload_tester_edge_cases(touch_soon) -> None:
    empty_file = Path("empty_file.txt")
    non_existent_file = Path("non_existent_file.txt")
    dotted_file = Path(".dotted")
    
    with as_cwd(Path.cwd()):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=[".dotted", "empty_file.txt"],
        )
        reloader = WatchFilesReload(config, Mock(), [])
        
        # Test with an empty file
        empty_file.touch()
        assert self._reload_tester(touch_soon, reloader, empty_file)
        empty_file.unlink()

        # Test with a non-existent file
        assert self._reload_tester(touch_soon, reloader, non_existent_file) is None

        # Test with a dotted file
        assert self._reload_tester(touch_soon, reloader, dotted_file)

        reloader.shutdown()