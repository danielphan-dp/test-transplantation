import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

class CustomReload(BaseReload):
    def __init__(self, config):
        super().__init__(config)
        self.step = 0

    def should_restart(self):
        self.step += 1
        if self.step == 1:
            return None
        elif self.step == 2:
            return [Path('foobar.py')]
        else:
            raise StopIteration()

def test_should_restart_initial_state():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config)
    
    assert reloader.should_restart() is None

def test_should_restart_second_call():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config)
    
    reloader.should_restart()  # First call
    result = reloader.should_restart()  # Second call
    
    assert result == [Path('foobar.py')]

def test_should_restart_after_second_call():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config)
    
    reloader.should_restart()  # First call
    reloader.should_restart()  # Second call
    
    with pytest.raises(StopIteration):
        reloader.should_restart()  # Third call should raise StopIteration

def test_should_restart_multiple_calls():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config)
    
    for _ in range(2):
        reloader.should_restart()
    
    with pytest.raises(StopIteration):
        reloader.should_restart()  # Should raise after two calls

def test_should_restart_with_custom_path(tmp_path: Path):
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config)
    
    reloader.should_restart()  # First call
    reloader.should_restart()  # Second call
    
    result = reloader.should_restart()  # Third call
    assert result == [tmp_path / 'foobar.py']  # Check if the path is correct