import pytest
from unittest.mock import MagicMock
from uvicorn import Config

class TestCloseMethod:
    def test_close_method_not_closed(self):
        instance = MagicMock()
        instance.closed = False
        instance.close()
        assert instance.closed is True

    def test_close_method_already_closed(self):
        instance = MagicMock()
        instance.closed = True
        with pytest.raises(AssertionError):
            instance.close()