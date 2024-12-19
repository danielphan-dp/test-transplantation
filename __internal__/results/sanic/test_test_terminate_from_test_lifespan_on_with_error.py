import os
import signal
from unittest.mock import Mock, patch
import pytest
from sanic.worker.process import terminate

@pytest.mark.parametrize("flags, expected_signal", [
    (0, signal.SIGTERM),
    (1, signal.CTRL_BREAK_EVENT)
])
@patch('sanic.worker.process.os')
def test_terminate_with_various_flags(os_mock: Mock, flags, expected_signal):
    process = Mock()
    process.send_signal = Mock()
    process.terminate = Mock()
    
    global flags
    flags = flags
    
    terminate(process)
    
    if flags:
        process.send_signal.assert_called_once_with(expected_signal)
        process.terminate.assert_not_called()
    else:
        process.terminate.assert_called_once()
        process.send_signal.assert_not_called()