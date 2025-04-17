import socket
import pytest
from pathlib import Path
from uvicorn.config import Config

@pytest.mark.parametrize("short_socket_name", ["my.sock", "/tmp/my.sock", "/tmp/long_socket_name.sock"])
@pytest.mark.parametrize("reload, workers", [(True, 1), (False, 2)], ids=["--reload=True --workers=1", "--reload=False --workers=2"])
@pytest.mark.skipif(sys.platform == "win32", reason="require unix-like system")
def test_getsockname_with_various_socket_names(tmp_path: Path, reload: bool, workers: int, short_socket_name: str):
    config = Config(app=asgi_app, uds=short_socket_name, reload=reload, workers=workers)
    config.load()
    sock = config.bind_socket()
    assert isinstance(sock, socket.socket)
    assert sock.family == socket.AF_UNIX
    assert sock.getsockname() == short_socket_name
    sock.close()

@pytest.mark.parametrize("invalid_socket_name", ["", None, "/invalid/path/to/socket.sock"])
@pytest.mark.parametrize("reload, workers", [(True, 1), (False, 2)], ids=["--reload=True --workers=1", "--reload=False --workers=2"])
@pytest.mark.skipif(sys.platform == "win32", reason="require unix-like system")
def test_getsockname_with_invalid_socket_names(tmp_path: Path, reload: bool, workers: int, invalid_socket_name: str):
    config = Config(app=asgi_app, uds=invalid_socket_name, reload=reload, workers=workers)
    config.load()
    with pytest.raises(OSError):
        sock = config.bind_socket()