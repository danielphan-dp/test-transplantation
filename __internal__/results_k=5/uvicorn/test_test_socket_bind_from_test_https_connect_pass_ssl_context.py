import pytest
from unittest.mock import MagicMock
from uvicorn import Config

class TestCloseMethod:
    def test_close_method_not_closed(self):
        config = Config(app=MagicMock())
        instance = config.lifespan  # Assuming lifespan is where close is defined
        instance.closed = False
        instance.close()
        assert instance.closed is True

    def test_close_method_already_closed(self):
        config = Config(app=MagicMock())
        instance = config.lifespan
        instance.closed = True
        with pytest.raises(AssertionError):
            instance.close()