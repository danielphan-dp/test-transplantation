import pytest
from unittest.mock import MagicMock
from uvicorn.config import Config
from uvicorn import Server

@pytest.mark.parametrize("server_closed", [True, False], ids=["server_closed=True", "server_closed=False"])
def test_close_method(server_closed):
    server = Server(config=MagicMock())
    server.closed = server_closed

    if server_closed:
        with pytest.raises(AssertionError):
            server.close()
    else:
        server.close()
        assert server.closed is True