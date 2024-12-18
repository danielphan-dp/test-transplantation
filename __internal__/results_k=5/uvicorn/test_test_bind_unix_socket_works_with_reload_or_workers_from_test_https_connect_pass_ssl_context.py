import pytest
from unittest.mock import MagicMock
from uvicorn import Config

class TestCloseMethod:
    def test_close_method_not_closed(self):
        config = Config(app=MagicMock())
        config.closed = False
        config.close()
        assert config.closed is True

    def test_close_method_already_closed(self):
        config = Config(app=MagicMock())
        config.closed = True
        with pytest.raises(AssertionError):
            config.close()