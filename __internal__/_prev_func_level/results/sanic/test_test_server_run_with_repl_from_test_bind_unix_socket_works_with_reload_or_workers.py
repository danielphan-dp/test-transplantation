import socket
import pytest
from unittest.mock import patch
from conftest import get_port

def test_get_port():
    with patch("socket.socket") as mock_socket:
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.getsockname.return_value = ('', 12345)
        
        port = get_port()
        
        assert port == 12345
        mock_socket.assert_called_once()
        mock_socket_instance.bind.assert_called_once_with(('', 0))
        mock_socket_instance.getsockname.assert_called_once() 

def test_get_port_multiple_calls():
    with patch("socket.socket") as mock_socket:
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.getsockname.side_effect = [('', 12345), ('', 54321)]
        
        port1 = get_port()
        port2 = get_port()
        
        assert port1 == 12345
        assert port2 == 54321
        assert mock_socket_instance.bind.call_count == 2

def test_get_port_socket_error():
    with patch("socket.socket") as mock_socket:
        mock_socket.side_effect = socket.error("Socket error")
        
        with pytest.raises(socket.error):
            get_port()