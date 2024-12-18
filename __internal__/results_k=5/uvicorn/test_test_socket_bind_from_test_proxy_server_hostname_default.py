import pytest
from unittest.mock import MagicMock
from uvicorn import Config
from uvicorn.lifespan import LifespanOff

class TestLifespanOff:
    def test_close_not_closed(self):
        config = Config(app=MagicMock())
        lifespan = LifespanOff(config)
        lifespan.closed = False
        lifespan.close()
        assert lifespan.closed is True

    def test_close_already_closed(self):
        config = Config(app=MagicMock())
        lifespan = LifespanOff(config)
        lifespan.closed = True
        with pytest.raises(AssertionError):
            lifespan.close()