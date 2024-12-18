import pytest
from uvicorn import Server, Config

def test_close_method_not_closed():
    server = Server(config=Config(app=None))
    server.closed = False
    server.close()
    assert server.closed is True

def test_close_method_already_closed():
    server = Server(config=Config(app=None))
    server.closed = True
    with pytest.raises(AssertionError):
        server.close()