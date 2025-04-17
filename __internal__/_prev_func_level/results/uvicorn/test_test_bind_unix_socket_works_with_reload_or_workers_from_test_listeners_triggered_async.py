import socket
import pytest
from pathlib import Path
from uvicorn.config import Config

@pytest.mark.parametrize("short_socket_name", ["my.sock", "/tmp/my.sock", "/var/run/my.sock"])
@pytest.mark.parametrize("reload, workers", [(True, 1), (False, 2)], ids=["--reload=True --workers=1", "--reload=False --workers=2"])
@pytest.mark.skipif(sys.platform == "win32", reason="require unix-like system")
def test_getsockname_returns_correct_socket_name(tmp_path: Path, reload: bool, workers: int, short_socket_name: str):
    config = Config(app=asgi_app, uds=short_socket_name, reload=reload, workers=workers)
    config.load()
    sock = config.bind_socket()
    
    assert isinstance(sock, socket.socket)
    assert sock.family == socket.AF_UNIX
    assert sock.getsockname() == short_socket_name
    
    # Additional assertions to check the getsockname method directly
    assert sock.getsockname() == config.getsockname()
    
    sock.close()