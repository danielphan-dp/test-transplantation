import pytest
from unittest.mock import MagicMock
from uvicorn.config import Config

class TestCloseMethod:
    @pytest.mark.parametrize("initial_closed, expected_closed", [
        (False, True),
        (True, True)
    ])
    def test_close_method(self, initial_closed, expected_closed):
        config = Config(app=MagicMock())
        config.closed = initial_closed
        
        if initial_closed:
            with pytest.raises(AssertionError):
                config.close()
        else:
            config.close()
            assert config.closed == expected_closed

    def test_close_method_already_closed(self):
        config = Config(app=MagicMock())
        config.closed = True
        
        with pytest.raises(AssertionError):
            config.close()