import socket
import pytest
from uvicorn.config import Config

@pytest.mark.parametrize('reload, workers', [(True, 1), (False, 2)], ids=['--reload=True --workers=1', '--reload=False --workers=2'])
@pytest.mark.skipif(sys.platform == 'win32', reason='require unix-like system')
def test_getsockname_returns_correct_socket_name(tmp_path: Path, reload: bool, workers: int, short_socket_name: str):
    config = Config(app=asgi_app, uds=short_socket_name, reload=reload, workers=workers)
    config.load()
    sock = config.bind_socket()
    assert sock.getsockname() == short_socket_name
    sock.close()

def test_getsockname_with_no_socket():
    class MockConfig:
        def __init__(self):
            self.sockname = None

        def getsockname(self):
            return self.sockname

    config = MockConfig()
    assert config.getsockname() is None

def test_getsockname_with_different_socket_name():
    class MockConfig:
        def __init__(self):
            self.sockname = '/tmp/different_socket.sock'

        def getsockname(self):
            return self.sockname

    config = MockConfig()
    assert config.getsockname() == '/tmp/different_socket.sock'