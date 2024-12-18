import pytest
from unittest.mock import Mock
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from time import sleep

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [pytest.param(WatchFilesReload)])
def test_reload_tester_edge_cases(touch_soon) -> None:
    empty_file = Path("empty_file.txt")
    non_existent_file = Path("non_existent_file.txt")
    dotted_file = Path(".dotted")
    
    with empty_file.open('w') as f:
        f.write("")

    with as_cwd(Path.cwd()):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=[".dotted", "empty_file.txt"],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, empty_file) is not None
        assert self._reload_tester(touch_soon, reloader, dotted_file) is not None
        
        # Testing with a non-existent file
        with pytest.raises(FileNotFoundError):
            self._reload_tester(touch_soon, reloader, non_existent_file)

        reloader.shutdown()