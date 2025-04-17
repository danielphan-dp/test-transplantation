import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

@pytest.mark.parametrize('mode', ('auto', 'on'))
def test_close_method_not_closed(mode):
    config = Config(app=lambda scope, receive, send: None, lifespan=mode)
    lifespan = LifespanOn(config)
    
    lifespan.close()
    assert lifespan.closed is True

@pytest.mark.parametrize('mode', ('auto', 'on'))
def test_close_method_already_closed(mode):
    config = Config(app=lambda scope, receive, send: None, lifespan=mode)
    lifespan = LifespanOn(config)
    
    lifespan.close()
    with pytest.raises(AssertionError):
        lifespan.close()  # Should raise an assertion error since it's already closed

@pytest.mark.parametrize('mode', ('auto', 'on'))
def test_close_method_state(mode):
    config = Config(app=lambda scope, receive, send: None, lifespan=mode)
    lifespan = LifespanOn(config)
    
    lifespan.close()
    assert lifespan.closed is True
    assert lifespan.should_exit is True  # Assuming should_exit is set to True on close