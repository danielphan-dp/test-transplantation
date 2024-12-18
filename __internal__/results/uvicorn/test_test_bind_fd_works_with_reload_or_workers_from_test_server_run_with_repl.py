import socket
import pytest
from uvicorn.config import Config

@pytest.mark.parametrize("reload, workers, expected_sockname", [
    (True, 1, ""),
    (False, 2, ""),
    (False, 1, ""),
], ids=["--reload=True --workers=1", "--reload=False --workers=2", "--reload=False --workers=1"])
@pytest.mark.skipif(sys.platform == "win32", reason="require unix-like system")
def test_getsockname_with_fd(reload: bool, workers: int, expected_sockname: str):
    fdsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    fd = fdsock.fileno()
    config = Config(app=asgi_app, fd=fd, reload=reload, workers=workers)
    config.load()
    sock = config.bind_socket()
    assert isinstance(sock, socket.socket)
    assert sock.family == socket.AF_UNIX
    assert sock.getsockname() == expected_sockname
    sock.close()
    fdsock.close()

@pytest.mark.parametrize("reload, workers, expected_sockname", [
    (True, 1, ""),
    (False, 2, ""),
], ids=["--reload=True --workers=1", "--reload=False --workers=2"])
@pytest.mark.skipif(sys.platform == "win32", reason="require unix-like system")
def test_getsockname_with_unix_socket(reload: bool, workers: int, expected_sockname: str, short_socket_name: str):
    config = Config(app=asgi_app, uds=short_socket_name, reload=reload, workers=workers)
    config.load()
    sock = config.bind_socket()
    assert isinstance(sock, socket.socket)
    assert sock.family == socket.AF_UNIX
    assert sock.getsockname() == expected_sockname
    sock.close()