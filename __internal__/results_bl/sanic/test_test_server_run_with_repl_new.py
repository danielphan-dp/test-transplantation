import socket
import pytest
from unittest.mock import patch

def test_get_port_valid():
    port = get_port()
    assert isinstance(port, int)
    assert 0 < port < 65536

def test_get_port_multiple_calls():
    ports = {get_port() for _ in range(10)}
    assert len(ports) > 1

def test_get_port_no_bind():
    with patch("socket.socket.bind") as mock_bind:
        mock_bind.side_effect = OSError("Bind failed")
        with pytest.raises(OSError):
            get_port()