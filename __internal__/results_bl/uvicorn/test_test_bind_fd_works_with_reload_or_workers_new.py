import socket
import pytest
from uvicorn.config import Config

@pytest.mark.parametrize('reload, workers', [(True, 1), (False, 2)], ids=['--reload=True --workers=1', '--reload=False --workers=2'])
@pytest.mark.skipif(sys.platform == 'win32', reason='require unix-like system')
def test_getsockname_returns_correct_value(reload: bool, workers: int):
    fdsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    fd = fdsock.fileno()
    config = Config(app=asgi_app, fd=fd, reload=reload, workers=workers)
    config.load()
    sock = config.bind_socket()
    
    # Test getsockname method
    assert sock.getsockname() == ""
    
    # Close sockets
    sock.close()
    fdsock.close()

def test_getsockname_with_non_unix_socket():
    fdsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd = fdsock.fileno()
    config = Config(app=asgi_app, fd=fd, reload=False, workers=1)
    config.load()
    sock = config.bind_socket()
    
    # Test getsockname method
    assert sock.getsockname() != ""
    
    # Close sockets
    sock.close()
    fdsock.close()