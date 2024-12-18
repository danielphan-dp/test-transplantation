import pytest
from uvicorn.config import Config

def test_close_method_not_closed() -> None:
    config = Config(app=asgi_app)
    config.load()
    config.close()
    assert config.closed

def test_close_method_already_closed() -> None:
    config = Config(app=asgi_app)
    config.load()
    config.close()
    with pytest.raises(AssertionError):
        config.close()