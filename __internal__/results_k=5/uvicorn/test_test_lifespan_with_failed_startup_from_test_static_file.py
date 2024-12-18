import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

@pytest.mark.parametrize('mode', ('auto', 'on'))
def test_close_method_not_closed(mode):
    config = Config(app=lambda scope, receive, send: None, lifespan=mode)
    lifespan = LifespanOn(config)
    
    lifespan.close()
    assert lifespan.closed

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
    
    assert not lifespan.closed
    lifespan.close()
    assert lifespan.closed

@pytest.mark.parametrize('mode', ('auto', 'on'))
def test_close_method_multiple_calls(mode):
    config = Config(app=lambda scope, receive, send: None, lifespan=mode)
    lifespan = LifespanOn(config)
    
    lifespan.close()
    assert lifespan.closed
    lifespan.close()  # This should not raise an error, but the state should remain closed
    assert lifespan.closed