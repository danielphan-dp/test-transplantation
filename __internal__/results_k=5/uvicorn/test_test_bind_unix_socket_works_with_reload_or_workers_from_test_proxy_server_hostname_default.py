import pytest
from unittest.mock import MagicMock
from uvicorn import Config

class TestCloseMethod:
    @pytest.fixture
    def mock_config(self):
        return MagicMock(spec=Config)

    def test_close_method_not_closed(self, mock_config):
        mock_config.closed = False
        mock_config.close()
        assert mock_config.closed is True

    def test_close_method_already_closed(self, mock_config):
        mock_config.closed = True
        with pytest.raises(AssertionError):
            mock_config.close()